# Importing required libraries

import pyspark
sc = pyspark.SparkContext('local[*]')
from datetime import datetime
from pyspark.sql.functions import col, udf,from_unixtime
from pyspark.sql.types import DateType
from pyspark.sql import SQLContext
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.types import StringType


# Defining sql context
sqlContext = SQLContext(sc)
# Reading citibike data
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("merged_data_2015_arjun.csv")
df.registerTempTable("citibike")
# Preparing a new column - Day of the week 
df = df.withColumn("dayOfWeek",from_unixtime(unix_timestamp(df.starttime,'MM-dd-yyyy'), 'EEEEE'))
# Converting dates into datetime format 
df = df.select('*', from_unixtime(unix_timestamp('starttime', 'MM-dd-yyyy')).alias('starttimedate'))
df = df.select('*', from_unixtime(unix_timestamp('stoptime', 'MM-dd-yyyy')).alias('stoptimedate'))
df.registerTempTable("newCitiBike")


# Reading weather data
df_weather =  sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("weather3.csv")
df_weather.registerTempTable("weathertable")

# creating new column for average temperature for the day
query_weather = "select *, (TMAX + TMIN)/2 as TAVG from weathertable where STATION_NAME = 'NY CITY CENTRAL PARK NY US'"
weathertable = sqlContext.sql(query_weather)

# Converting date into datetime format
weathertable = weathertable.withColumn("DATE", weathertable["DATE"].cast(StringType()))
weathertable = weathertable.select('*', from_unixtime(unix_timestamp('DATE', 'yyyyMMdd')).alias('COMBINEDATE'))
weathertable.printSchema()

weathertable.registerTempTable("finalweather")
weathertable.take(10)
weathertable.select("COMBINEDATE").collect()


# Aggregating number of rides for each day
query_aggregate = "select count(*) as rides,date(starttimedate) from newCitiBike group by date(starttimedate) order by date(starttimedate)"
aggregate = sqlContext.sql(query_aggregate)
aggregate.registerTempTable("dayrides")
aggregate.select('starttimedate').collect()


# Reading holiday data from csv file
df_holiday = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load("holiday2.csv")
# converting date to date time format
df_holiday_final = df_holiday.select('*', from_unixtime(unix_timestamp('Date_Holiday', 'yyyyMMdd')).alias('holidaydate'))
df_holiday_final.registerTempTable("holiday")

# joining holiday data with aggregated ridership data
query_holiday = "select * from dayrides inner join holiday on date(starttimedate) = date(holidaydate)"
df_merge_holiday = sqlContext.sql(query_holiday)

# selecting columns needed for the model
df_rides_holidays = df_merge_holiday.select("rides","starttimedate","Holiday")
df_rides_holidays.registerTempTable("dayrides")

# Joining weather data and ridership table created above to give as input to the model
query_combine2 = "select *,date(starttimedate) as date2 from dayrides inner join finalweather on date(starttimedate) = date(COMBINEDATE) "
combined = sqlContext.sql(query_combine2)
combined.printSchema()

# Selecting features and label for model. Rides is the label and rest are the features
combined_keep = [combined.rides, combined.PRCP, combined.SNOW, combined.TMAX, combined.TMIN, combined.TAVG, combined.Holidays]
final_combined = combined.select(combined_keep)
final_combined.printSchema()
combined.select("date2").collect()

# Using vector assembler in pyspark to define feature columns
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["TAVG", "TMIN","TMAX","SNOW","PRCP","Holidays"],
    outputCol="features")

transformed = assembler.transform(final_combined)

from pyspark.mllib.regression import LabeledPoint
from pyspark.sql.functions import col

a = transformed.select(col("rides").alias("label"), col("features"))ng 

# splitting training and testing data
training_data, testing_data = a.randomSplit([0.8, 0.2])


# Using Random Forest Regressor from mllib pysaprk
from pyspark.ml.regression import RandomForestRegressor
# Defining model
rf = RandomForestRegressor()

# Fitting data into model
model = rf.fit(training_data)

# Getting predictions from model
predictions = model.transform(testing_data)
print predictions.take(10)


