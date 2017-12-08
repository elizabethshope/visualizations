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

killed <- aggregate(nkill ~ iyear + country_txt, data = terrorism, FUN = sum)
injured <- aggregate(nwound ~ iyear + country_txt, data = terrorism, FUN = sum)
killed_injured <- merge(x = killed, y = injured, by = c("iyear", "country_txt"), all = TRUE)
killed_injured[is.na(killed_injured)] <- 0
write.csv(killed_injured, "terrorism_killed_injured.csv", row.names = FALSE)
