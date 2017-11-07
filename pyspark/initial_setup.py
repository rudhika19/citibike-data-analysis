import pyspark
#sc = pyspark.SparkContext('local[*]')

from datetime import datetime
from pyspark.sql.functions import col, udf,from_unixtime
from pyspark.sql.types import DateType
from pyspark.sql import SQLContext
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.types import StringType

import matplotlib.pyplot as plt

sqlContext = SQLContext(sc)
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("final_merged_data_2015_2016.csv")
