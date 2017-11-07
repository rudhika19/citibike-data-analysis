# server.R

library(data.table)
library(lubridate)
library(plotly)
library(shinydashboard)
library(leaflet)
library(dplyr)

shinyServer(
  function(input, output) {
    
    df <- fread("/Users/kchak/Desktop/merged_data.csv");
    df$stoptime<- ymd_hms(df$stoptime)
    df$starttime<- ymd_hms(df$starttime)
    df$ride_year = as.integer(format(as.POSIXct(Sys.Date(),format="%Y-%m-%d %H:%M:%S"),"%Y"))
    df$ride_hour = as.integer(format(as.POSIXct(df$starttime,format="%Y-%m-%d %H:%M:%S"),"%H"))
    df$ride_month = as.integer(format(as.POSIXct(df$starttime,format="%Y-%m-%d %H:%M:%S"),"%m"))
    
    
    output$myplotwhen <- renderPlotly({
      new_data = filter(df,
                        df$gender == input$gender & 
                        df$birth_year == input$birth_year
      )
      
      plot_ly(
        x = weekdays(new_data$starttime),
        y = new_data$ride_hour,
        z = new_data$tripduration,
        type = "heatmap"
      )
    });
    
    output$myplotwhere <- renderLeaflet({
      
      
      new_data = filter(df,
                        df$gender == input$gender_1 &
                          df$birth_year >=  df$ride_year - input$age[2] &
                          df$birth_year <=  df$ride_year - input$age[1] &
                          weekdays(df$starttime) == input$day &
                          df$ride_hour >= input$time[1] &
                          df$ride_hour <= input$time[2] 
      )
      
      m <- leaflet(new_data[1:input$number_of_stations,]) %>% 
        addTiles()
      
      m %>% addMarkers(~start_station_longitude, 
                       ~start_station_latitude, popup=new_data$start_station_name)
    });
    
    output$myplot_top25 <- renderPlotly({
      
      new_data = filter(df,
                        
                        df$ride_month == input$month &
                          weekdays(df$starttime) == input$day_of_week &
                          df$ride_hour >= input$time_top25[1] &
                          df$ride_hour <= input$time_top25[2]
      )
      
      final_df = data.frame ( table ( new_data$start_station_name, new_data$end_station_name ) )
      final_df=final_df[order(-final_df$Freq),]
      final_df = final_df[1:25,]
      colnames(final_df)[1] <- "start_station_name"
      colnames(final_df)[2] <- "end_station_name"
      colnames(final_df)[3] <- "count"
      
      plot_ly(final_df,
              x = ~start_station_name,
              y = ~end_station_name,
              z = ~count, 
              type = "heatmap"
      )
      
    })
  }
)