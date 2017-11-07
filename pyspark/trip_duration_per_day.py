#trip duration per day
df.registerTempTable("citibike")
trip_duration_per_day = """
                select 
                    DATE(starttime) as date,
                    SUM(tripduration) as total_duration
                from citibike 
                group by 
                    DATE(starttime)
                order by date
            """

df_trip_duration_per_day = sqlContext.sql(trip_duration_per_day)
df_trip_duration_per_day.select("date","total_duration").show()

trip_duration_list = df_trip_duration_per_day.select("total_duration").rdd.flatMap(lambda x: x).collect()
N = len(trip_duration_list)
x = range(N)
width = 1/1.5
plt.bar(x, trip_duration_list, width, color="blue")
plt.ylabel('Trip Duration')
plt.xlabel('Date')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') 
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelleft='off') 
plt.show()