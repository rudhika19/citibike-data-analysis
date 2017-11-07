#rides per day of the week per month
df.registerTempTable("citibike")
month_week_query_2015 = """
    select 
        MONTH(starttime) as month,
        dayOfWeek,
        count(*) as numRides 
    from citibike
    where YEAR(starttime) = 2015
    group by 
        month(starttime),
        dayOfWeek"""

#sqlContext.sql(month_day_query).show()
df_month_week_rides_2015 = sqlContext.sql(month_week_query_2015)
#df_month_week_rides_2015.select('month','dayOfWeek','numRides').show();

month_week_right_list_2015 = df_month_week_rides_2015.select('numRides').toPandas()
month_week_right_list_2015 = month_week_right_list_2015.as_matrix().reshape(12,7)


#rides per day of the week per month
df.registerTempTable("citibike")
month_week_query_2016 = """
    select 
        MONTH(starttime) as month,
        dayOfWeek,
        count(*) as numRides 
    from citibike
    where YEAR(starttime) = 2016
    group by 
        month(starttime),
        dayOfWeek"""

#sqlContext.sql(month_day_query).show()
df_month_week_rides_2016 = sqlContext.sql(month_week_query_2016)
#df_month_week_rides_2016.select('month','dayOfWeek','numRides').show();

month_week_right_list_2016 = df_month_week_rides_2016.select('numRides').toPandas()
month_week_right_list_2016 = month_week_right_list_2016.as_matrix().reshape(12,7)

#print(month_week_right_list_2015)
#print(month_week_right_list_2016)

plt.figure(figsize=(20,8))
plt.subplot(1, 2, 1)
sns.heatmap(month_week_right_list_2015, cmap='magma', label='2015', vmax=250000, vmin=20000)
plt.title('YEAR 2015', size=10)

plt.subplot(1, 2, 2)
sns.heatmap(month_week_right_list_2016, cmap='magma', label='2016', vmax=250000, vmin=20000)
plt.title('YEAR 2016', size=10)

plt.tight_layout()
plt.show()