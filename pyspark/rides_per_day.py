#per day rides
df.registerTempTable("citibike")
per_day_rides = """
                select 
                    DATE(starttime) as date,
                    count(*) as COUNT
                from citibike 
                group by 
                    DATE(starttime)
                order by date
          """

df_per_day_rides = sqlContext.sql(per_day_rides)
#df_per_day_rides.select("date","COUNT").show()

each_day_rides_list = df_per_day_rides.select("COUNT").rdd.flatMap(lambda x: x).collect()

N = len(each_day_rides_list)
x = range(N)
width = 1/1.5
plt.bar(x, each_day_rides, width, color="blue")
plt.ylabel('Number of Rides')
plt.xlabel('Date')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') 
plt.show()