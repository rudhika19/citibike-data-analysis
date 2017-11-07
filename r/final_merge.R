#Clear environment
rm(list = ls())
setwd("/Users/kchak/Google Drive/NYU/Spring 2017/Programming for Big Data/project/original_csv/")

library(data.table)
library(dplyr)
library(lubridate)
library(plotly)

#load all files
filenames <- list.files(pattern="*.csv")
files <- lapply(filenames, fread) # fread is the fast reading function from the data.table package

#bind all files and create new dataframe
merged_data <- rbindlist(files)

rm(files)

#rename the columns
names(merged_data) <- gsub(" ", "_", names(merged_data))
glimpse(merged_data)

merged_data$tripduration = as.integer(merged_data$tripduration)
merged_data$start_station_id = as.integer(merged_data$start_station_id)
merged_data$end_station_id = as.integer(merged_data$end_station_id)
merged_data$bikeid = as.integer(merged_data$bikeid)
merged_data$birth_year = as.integer(merged_data$birth_year)
#merged_data$gender = as.integer(merged_data$gender)

merged_data$start_station_latitude = as.numeric(merged_data$start_station_latitude)
merged_data$start_station_longitude = as.numeric(merged_data$start_station_longitude)
merged_data$end_station_latitude = as.numeric(merged_data$end_station_latitude)
merged_data$end_station_longitude = as.numeric(merged_data$end_station_longitude)

merged_data$gender[merged_data$gender == 1 ] = 'Male'
merged_data$gender[merged_data$gender == 2 ] = 'Female'
merged_data$gender[merged_data$gender == 0 ] = 'Unknown'

merged_data$starttime = as.character(parse_date_time(x = merged_data$starttime,
                orders = c("m/d/y H:M", "m/d/y H:M:S", "y-m-d H:M:S"),
                locale = "eng"))

merged_data$stoptime = as.character(parse_date_time(x = merged_data$stoptime,
                                            orders = c("m/d/y H:M", "m/d/y H:M:S", "y-m-d H:M:S"),
                                            locale = "eng"))

merged_data$birth_year[is.na(merged_data$birth_year)] <- mean(merged_data$birth_year, na.rm = TRUE)
merged_data$birth_year = as.integer(merged_data$birth_year)

glimpse(merged_data)

#write to the file
fwrite(merged_data, file = "merged_data.csv")
