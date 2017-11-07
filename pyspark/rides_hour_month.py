#Rides per month per hour
month_hour_query_2015 = """
    select 
        month(starttime) as month, 
        hour(starttime) as hour,
        Count(*) as numRides 
    from citibike 
    where year(starttime) = 2015 
    group by month(starttime),hour(starttime)"""

df_month_hour_rides_2015 = sqlContext.sql(month_hour_query_2015)
#df_month_hour_rides_2015.printSchema()
#df_month_hour_rides_2015.select('month','hour','numRides').show();

pdf_month_hour_rides_2015 = df_month_hour_rides_2015.select('numRides').toPandas()
temp_list_2015 = pdf_month_hour_rides_2015.as_matrix().reshape(12,24)

#print (temp_list_2015)

month_hour_query_2015 = """
    select 
        month(starttime) as month, 
        hour(starttime) as hour,
        Count(*) as numRides 
    from citibike 
    where year(starttime) = 2016 
    group by month(starttime),hour(starttime)"""

df_month_hour_rides_2016 = sqlContext.sql(month_hour_query_2016)
#df_month_hour_rides_2016.printSchema()
#df_month_hour_rides_2016.select('month','hour','numRides').show();


pdf_month_hour_rides_2016 = df_month_hour_rides_2016.select('numRides').toPandas()
temp_list_2016 = pdf_month_hour_rides_2016.as_matrix().reshape(12,24)

plt.figure(figsize=(20,8))

plt.subplot(1, 2, 1)
sns.heatmap(temp_list_2015, cmap='magma', label='2015', vmax=150000, vmin=500)
plt.title('YEAR 2015', size=10)

plt.subplot(1, 2, 2)
sns.heatmap(temp_list_2016, cmap='magma', label='2016', vmax=150000, vmin=500)
plt.title('YEAR 2016', size=10)

plt.tight_layout()
plt.show()