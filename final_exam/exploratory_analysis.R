# Libraries
library(ggplot2)
library(stringr)

# Read in data
data <- "../../../Downloads/TerrorismDATA_Real_1970_2016.csv"
terrorism <- read.csv(data, header=TRUE, skip=2)

# Create df for counts over time
counts <- c(unclass(table(terrorism$iyear)))
counts_df <- data.frame(count = counts)
counts_df$year <- rownames(counts_df)
counts_df$year <- as.integer(counts_df$year)
rownames(counts_df) <- NULL

# Plot counts over time
ggplot(counts_df, aes(x = year, y = count)) +
  geom_bar(stat='identity', alpha = 0.5, fill = "red") +
  labs(x = "Year", y = "Count", title = "Terrorism Incidents per Year (1970 - 2016)") +
  theme(axis.text.x = element_text(size=12),
        axis.text.y = element_text(size=12),
        title = element_text(size=16))
# NOTE: There are no attacks recorded in the database for 1993

# Counts by month
counts_by_month_df <- data.frame(table(terrorism$imonth[terrorism$imonth != 0]))
colnames(counts_by_month_df) <- c("Month", "Count")

# Plot incidents by month to check if uniformly distributed in months
ggplot(counts_by_month_df, aes(x = Month, y = Count)) +
  geom_bar(stat = 'identity', alpha = 0.5, fill = "red") + 
  labs(title = "Terrorism Incidents by Month of Year") +
  theme(axis.text.x = element_text(size=12),
        axis.text.y = element_text(size=12),
        title = element_text(size=16))

# Create terrorism for counts by year & region
counts_by_region_df <- data.frame(table(terrorism$region_txt, terrorism$iyear))
colnames(counts_by_region_df) <- c("Region", "Year", "Count")
counts_by_region_df$Year <- as.integer(as.character(counts_by_region_df$Year))

# Plot counts by region & time
ggplot(counts_by_region_df, aes(x = Year, y = Count, fill = Region)) +
  geom_area() +
  labs(title = "Terrorism Incidents by Region and Year (1970-2016)") +
  theme(axis.text.x = element_text(size=12),
        axis.text.y = element_text(size=12),
        legend.text = element_text(size=12),
        title = element_text(size=16))

# Create df of percentages of attack types for each year
counts_by_attacktype_df <- data.frame(table(terrorism$attacktype1_txt, terrorism$iyear))
colnames(counts_by_attacktype_df) <- c("AttackType", "Year", "Count")
counts_by_attacktype_df$Year <- as.integer(as.character(counts_by_attacktype_df$Year))
counts_by_attacktype_df <- counts_by_attacktype_df[order(counts_by_attacktype_df$AttackType),]
counts_by_attacktype_df$TotalAttacks <- rep(counts_df$count, 9) 
counts_by_attacktype_df$Percent <- counts_by_attacktype_df$Count/counts_by_attacktype_df$TotalAttacks*100
counts_by_attacktype_df <- counts_by_attacktype_df[order(counts_by_attacktype_df$Year),]

# Plot counts by region & time
ggplot(counts_by_attacktype_df, aes(x = Year, y = Percent, color = AttackType, group = AttackType)) +
  geom_point() +
  geom_line() +
  labs(title = "Percent of Terrorism Incidents by Attack Type and Year (1970-2016)",
       color = "Attack Type") +
  theme(axis.text.x = element_text(size=12),
        axis.text.y = element_text(size=12),
        legend.text = element_text(size=12),
        title = element_text(size=16))

# Extract deadliest terrorist attacks (with 100+ people killed)
deadliest <- terrorism[order(-terrorism$nkill),]
deadliest <- deadliest[deadliest$nkill >= 100,]
deadliest <- deadliest[!is.na(deadliest$nkill),]

# Plot deadliest attacks by region
ggplot(deadliest, aes(x = region_txt, y = nkill)) +
  geom_jitter(width=0.2, aes(color = region_txt)) +
  ylim(0,1501) +
  scale_x_discrete(labels = function(x) str_wrap(x, width = 8)) +
  labs(x = "Region", y = "Number of People Killed",
       title = "Number of People Killed in Deadliest Incidents by Region",
       color = "Region") +
  theme(axis.text.x = element_text(size=10),
        axis.text.y = element_text(size=10),
        legend.text = element_text(size=12),
        title = element_text(size=15))




## EXTRA DATA STUFF
# Read in data
data <- "../../../Downloads/TerrorismDATA_Real_1970_2016.csv"
terrorism <- read.csv(data, header=TRUE, skip=2)

date_concat <- function(month, day, year) {
  paste(month, day, year, sep = "/")
}

iraq <- terrorism[terrorism$country_txt == "Iraq" & terrorism$iyear %in% c(1976, 1996, 2006, 2016) & terrorism$iday != 0,]
iraq <- iraq[c("eventid", "iyear", "imonth", "iday", "provstate", "city", "latitude", "longitude", "summary", "attacktype1_txt", "targtype1_txt", "nkill")]
iraq$date <- mapply(date_concat, iraq$imonth, iraq$iday, iraq$iyear)
write.csv(iraq, "iraq.csv", row.names = FALSE)

mean.killed <- aggregate(nkill ~ iyear, data = terrorism, FUN = mean)
mean.killed <- rbind(mean.killed, c(1993, 2.051272))
mean.killed <- mean.killed[order(mean.killed$iyear),]
write.csv(mean.killed, "terrorism_mean_killed.csv", row.names = FALSE)

num.killed <- aggregate(nkill ~ iyear, data = terrorism, FUN = sum)
num.killed <- rbind(num.killed, c(1993, 10162))
num.killed <- num.killed[order(num.killed$iyear),]
write.csv(num.killed, "terrorism_num_killed.csv", row.names = FALSE)

attacks.region.year <- data.frame(table(terrorism$iyear, terrorism$region_txt))
colnames(attacks.region.year) <- c("Year", "Region", "Count")
write.csv(attacks.region.year, "terrorism_attacks_region_year.csv", row.names = FALSE)

terrorism_2016 <- terrorism[terrorism$iyear == 2016,]
terrorism_2016 <- terrorism_2016[c("eventid", "iyear", "imonth", "iday", "provstate",
                                   "city", "country_txt", "latitude", "longitude", "summary", 
                                   "attacktype1_txt", "targtype1_txt", "nkill")]
write.csv(terrorism_2016, "terrorism_2016.csv", row.names = FALSE)

terrorism_2016_summaries <- terrorism[terrorism$iyear == 2016,]
terrorism_2016_summaries <- terrorism_2016_summaries[c("region_txt", "summary")]
write.csv(terrorism_2016_summaries, "terrorism_2016_summaries.csv", row.names=FALSE)

successes_failures <- aggregate(success ~ iyear, data = terrorism, FUN = length)
successes <- aggregate(success ~ iyear, data = terrorism, FUN = sum)
colnames(successes_failures) <- c("year", "attacks_tot")
successes_failures$attacks_success <- successes$success
successes_failures$attacks_failures <- successes_failures$attacks_tot - successes_failures$attacks_success
successes_failures$fail_percent <- successes_failures$attacks_failures/successes_failures$attacks_tot*100
write.csv(successes_failures, "terrorism_failures.csv", row.names=FALSE)
  
suicide_portion <- aggregate(suicide ~ iyear, data = terrorism, FUN = mean)
suicide_count <- aggregate(suicide ~ iyear, data = terrorism, FUN = sum)
names(suicide_count) <- c("year", "suicide_count")
suicide_count$suicide_portion <- suicide_portion$suicide
write.csv(suicide_count, "terrorism_suicides.csv", row.names = FALSE)
