# Customers over months
df.registerTempTable("citibike")
customer_increase_query = """select MONTH(starttime) as month, YEAR(starttime) as year, count(*) as customer_count 
            from citibike 
            where usertype = 'Customer'
            group by MONTH(starttime), YEAR(starttime)
            order by year, month"""

df_customer_increase_query = sqlContext.sql(customer_increase_query)
df_customer_increase_query.select("month","year","customer_count").show()

#Visualization
customer_count_list = df_customer_increase_query.select("customer_count").rdd.flatMap(lambda x: x).collect()
LABELS = ["Jan'15", "Feb'15", "Mar'15", "Apr'15", "May'15","Jun'15","Jul'15","Aug'15","Sep'15","Oct'15","Nov'15","Dec'15","Jan'16", "Feb'16", "Mar'16", "Apr'16", "May'16","Jun'16","Jul'16","Aug'16","Sep'16","Oct'16","Nov'16","Dec'16"]
N = len(customer_count_list)
x = range(N)
width = 0.8
plt.bar(x, customer_count_list, width, color="blue")
plt.ylabel('Customers')
plt.xlabel('Month and Year')
plt.xticks(x, LABELS, rotation=75)

plt.show()