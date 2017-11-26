# Load libraries
library(ggplot2)
library(ggthemes)
library(scales)

# Read in bikeshare data
bikeshare <- read.csv("../../../Downloads/2016-Q3-cabi-trips-history-data/2016-Q3-Trips-History-Data-2.csv", as.is = TRUE)

# Remove some columns
bikeshare <- bikeshare[c("Duration..ms.", "Start.date", "Start.station", "End.station", "Member.Type")]

# Get rid of start time of ride -- just have start date
dt_split <- data.frame(do.call('rbind', strsplit(as.character(bikeshare$Start.date),' ',fixed=TRUE)))
bikeshare$Start.date <- dt_split$X1 
rm(dt_split)

# Convert date strings to dates
bikeshare$Start.date <- as.Date(bikeshare$Start.date,format='%m/%d/%Y')

# Add trip duration in mins
bikeshare$DurationMins <- bikeshare$Duration..ms./60000

# Create data frame of number of registered vs. casual trips each day
reg_v_casual <- data.frame(table(bikeshare$Member.Type, bikeshare$Start.date))
colnames(reg_v_casual) <- c("MemberType", "Date", "TripCount")
reg_v_casual$DayOfWeek <- sapply(as.Date(reg_v_casual$Date), weekdays, TRUE)

# Determine mean trip length for registered vs. casual users
mean(bikeshare$DurationMins[bikeshare$Member.Type == "Registered"])
mean(bikeshare$DurationMins[bikeshare$Member.Type == "Casual"])

# Create data frame of mean durations given date and membership type
mean_durations <- aggregate(DurationMins ~ Start.date + Member.Type, data = bikeshare, mean)

# Create data frame of start station counts by membership type
start_station_counts <- as.data.frame(table(bikeshare$Member.Type, bikeshare$Start.station))
colnames(start_station_counts) <- c("MemberType", "StartStation", "TripCount")
start_station_counts <- start_station_counts[order(start_station_counts[,1], -start_station_counts[,3]),]
rownames(start_station_counts) <- NULL

start_station_wide <- tidyr::spread(start_station_counts, key=MemberType, value=TripCount)

labeled_stations <- c(as.character(start_station_counts$StartStation[start_station_counts$MemberType == "Registered"])[1:5], as.character(start_station_counts$StartStation[start_station_counts$MemberType == "Casual"])[1:5])

start_station_wide$Labels <- ifelse(start_station_wide$StartStation %in% labeled_stations, as.character(start_station_wide$StartStation), NA)
start_station_wide$Category <- ifelse(start_station_wide$StartStation %in% labeled_stations[1:5], "TopReg", ifelse(start_station_wide$StartStation %in% labeled_stations[6:10], "TopCas", "NA"))

  
# Create ggplots
ggplot(reg_v_casual, aes(x=as.Date(Date), y=TripCount, group=MemberType, color=MemberType)) +
  geom_point() +
  geom_line() +
  labs(x = "Date", y = "Trips per Day", title = "Daily Bikeshare Trip Count for Registered vs. Casual Riders\nSeptember 2016",
       color = "Member Type") +
  scale_x_date(labels = date_format("%a\n%b %d")) +
  scale_color_manual(values=c("#EC342E", "#FCDB31")) +
  theme_solarized_2(light=FALSE) +
  theme(plot.title = element_text(hjust=0.5))

ggsave("daily_counts.png", width = 7.5, height = 4.25, units = "in", dpi=500)

ggplot(mean_durations, aes(x=Start.date, y=DurationMins, color=Member.Type)) +
  geom_point() +
  geom_line() +
  facet_wrap(~Member.Type, ncol=1, scales="free_y") +
  labs(x = "Date", y = "Duration (Mins)", title = "Daily Average Trip Durations for Registered vs. Casual Riders\nSeptember 2016",
       color = "Member Type") +
  scale_x_date(labels = date_format("%a\n%b %d")) +
  scale_color_manual(values=c("#EC342E", "#FCDB31")) +
  theme_solarized_2(light=FALSE) +
  theme(plot.title = element_text(hjust=0.5))

ggsave("daily_durations.png", width = 7.5, height = 4.25, units = "in", dpi=500)

cols <- c("TopCas" = "#EC342E", "TopReg" = "#FCDB31", "NA" = "#DBCBA9")

ggplot(start_station_wide, aes(x = Casual, y = Registered, color=Category)) +
  geom_point(size=1) +
  geom_text(aes(label=Labels), na.rm=TRUE, hjust = 0, vjust=0, 
            nudge_x = 0.2, nudge_y = 0.2, angle=30, size=3) +
  xlim(0,5500) +
  ylim(0,7500) +
  labs(x = "Casual Trips from Station", y = "Registered Trips from Station",
       title = "Registered vs. Casual Trips from Stations\nSeptember 2016",
       color = "Top Start\nStations") +
  scale_color_manual(values=cols, breaks=c("TopCas", "TopReg", "NA"), 
                     labels = c("Top Casual\nStation", "Top Registered\nStation", "Station")) +
  theme_solarized_2(light=FALSE) +
  theme(plot.title = element_text(hjust=0.5),
        legend.key.height=unit(2,"line"))

ggsave("station_starts.png", width = 7.5, height = 6, units = "in", dpi=500)