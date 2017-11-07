#time series
time_series_query = """select year(starttime) as year, month(starttime) as month, count(*) as rides
                from citibike
                group by year(starttime), month(starttime)
                order by year, month
            """
df_time_series = sqlContext.sql(time_series_query)
df_time_series.registerTempTable("citibike_time_series")

time_series_query_2015 = """select * from citibike_time_series where year = 2015"""

df_time_series_2015 = sqlContext.sql(time_series_query_2015)
# df_time_series_2015.printSchema()
# df_time_series_2015.select("year","month","rides").show()

time_series_query_2016 = """select * from citibike_time_series where year = 2016"""
df_time_series_2016 = sqlContext.sql(time_series_query_2016)
# df_time_series_2016.printSchema()
# df_time_series_2016.select("year","month","rides").show()

numrides_list_2015 = df_time_series_2015.select('rides').toPandas()
numrides_list_2015 = numrides_list_2015.as_matrix()

numrides_list_2016 = df_time_series_2016.select('rides').toPandas()
numrides_list_2016 = numrides_list_2016.as_matrix()

month_list = range(1, 13)

LABELS = ["Jan", "Feb", "Mar", "Apr", "May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
plt.plot(month_list,numrides_list_2015)
plt.plot(month_list,numrides_list_2016)
plt.legend(['2015', '2016'], loc='lower right')
plt.xticks(month_list, LABELS, rotation=0)
plt.show()