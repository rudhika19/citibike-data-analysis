# ui.R
library(data.table)
library(lubridate)
library(plotly)
library(shinydashboard)
library(leaflet)

dashboardPage(
  dashboardHeader(title = "CitiBike"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("When?", tabName = "when"),
      menuItem("Where?", tabName = "where"),
      menuItem("Top 25", tabName = "top25")
    )
  ),
  dashboardBody(
    
    
    tabItems(
      # First tab content
      tabItem(tabName = "when",
              fluidPage(
                titlePanel("When?"),
                sidebarLayout(position = "right",
                              sidebarPanel(
                                
                                selectInput("gender", 
                                            label = "Gender",
                                            choices = c("Male", "Female"),
                                            selected = "Male"),
                                
                                selectInput("birth_year", 
                                            label = "Birth Year",
                                            choices = array(1900:2000),
                                            selected = "1993"),
                                
                                submitButton("Submit")
                              ),
                              
                              mainPanel(
                                plotlyOutput("myplotwhen")
                              )
                )
              )
      ),
      
      # Second tab content
      tabItem(tabName = "where",
              fluidPage(
                titlePanel("Most Concentrated Areas"),
                
                sidebarLayout(position = "right",
                              sidebarPanel(
                                
                                selectInput("gender_1", 
                                            label = "Gender",
                                            choices = c("Male", "Female"),
                                            selected = "Male"),
                                
                                sliderInput("age",
                                            label = "Age",
                                            min = 17,
                                            max = 98,
                                            value = c(23,30)),
                                
                                selectInput("day", 
                                            label = "Day of the week",
                                            choices = c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"),
                                            selected = "Sunday"),
                                
                                sliderInput("time", 
                                            label = "Time of the day",
                                            min = 0,
                                            max = 23,
                                            value = c(16,20)),
                                
                                selectInput("number_of_stations", 
                                            label = "Number of Top Stations",
                                            choices = c(1:25),
                                            selected = "10"),
                                
                                submitButton("Submit")
                              ),
                              
                              mainPanel(
                                leafletOutput("myplotwhere")
                              )
                )
              )
      ),
      
      tabItem(tabName = "top25",
              fluidPage(
                titlePanel("Top 25 Pairs"),
                
                sidebarLayout(position = "right",
                              sidebarPanel(
                                
                                selectInput("month", 
                                            label = "Month",
                                            choices = array(1:12),
                                            selected = 12),
                                
                                selectInput("day_of_week", 
                                            label = "Day of the week",
                                            choices = c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"),
                                            selected = "Sunday"),
                                
                                sliderInput("time_top25", 
                                            label = "Time of the day",
                                            min = 0,
                                            max = 23,
                                            value = c(16,20)),
                                
                                submitButton("Submit")
                              ),
                              
                              mainPanel(
                                plotlyOutput("myplot_top25")
                              )
                )
              )
              )
    )
  )
)