# Elizabeth Shope
# Data Visualization Portfolio Project

# Load libraries
library(ggplot2)
library(ggthemes)
library(stringr)

# Read in data
cancer <- read.table('BYSITE.TXT', header=TRUE, sep = "|")

# Look at unique values of YEAR
unique(cancer$YEAR)

# Remove the rows with year 2010-2014 
cancer <- cancer[cancer$YEAR != "2010-2014",]

# Look at column names
colnames(cancer)

# Get rid of the non-age-adjusted rates & CI values
cancer <- cancer[,c("YEAR", "RACE", "SEX", "SITE", "EVENT_TYPE", "COUNT", "POPULATION", "AGE_ADJUSTED_RATE")]

# Check the structure / data types
str(cancer)

# Make year, count and age-adjusted rate numeric (instead of factors)
cancer$COUNT <- as.numeric(as.character(t(cancer$COUNT)))
cancer$YEAR <- as.numeric(as.character(t(cancer$YEAR)))
cancer$AGE_ADJUSTED_RATE <- as.numeric(as.character(t(cancer$AGE_ADJUSTED_RATE)))

# Make some aggregated data subsets
cancer_agg_sites_races <- cancer[cancer$RACE == "All Races" & cancer$SITE == "All Cancer Sites Combined"
                                 & cancer$SEX != "Male and Female",]

cancer_agg_sites_2014 <- cancer[cancer$YEAR == 2014 & cancer$SITE == "All Cancer Sites Combined"
                                & cancer$SEX != "Male and Female" & cancer$RACE != "All Races",]

cancer_agg_races_2014 <- cancer[cancer$RACE == "All Races" & cancer$YEAR == 2014 & 
                                  cancer$SEX != "Male and Female" & 
                                  cancer$SITE != "All Cancer Sites Combined" &
                                  cancer$SITE != "All Sites (comparable to ICD-O-2)" &
                                  cancer$SITE != "Female Breast, <i>in situ</i>",]

cancer_agg_races_2014 <- cancer_agg_races_2014[order(-cancer_agg_races_2014$AGE_ADJUSTED_RATE),]

# Determine which cancers have the highest incidence rates for any sex
cancer_rates <- aggregate(AGE_ADJUSTED_RATE ~ SITE, data=cancer_agg_races_2014, FUN = max)
cancer_rates <- cancer_rates[order(-cancer_rates$AGE_ADJUSTED_RATE),]
top_cancer_places = cancer_rates[1:20, 1]

cancer_agg_races_2014 <- cancer_agg_races_2014[cancer_agg_races_2014$SITE %in% top_cancer_places,]

cancer_agg_races_2014 <- droplevels(cancer_agg_races_2014)

# Plot 1
ggplot(cancer_agg_sites_races, 
       aes(x = YEAR, y = AGE_ADJUSTED_RATE, group = EVENT_TYPE, color = EVENT_TYPE)) + 
  geom_point() + 
  geom_line() +
  labs(x = "Year", y = "Age Adjusted Rate\nper 100,000 People", 
       title = "Cancer Rates by Year and Gender",
       color = "Event") +
  facet_wrap(~SEX) +
  theme_economist() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 12),
        axis.text.y = element_text(size = 12),
        axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        legend.title = element_text(size = 12))
ggsave('cancer-by-year-gender.png', width = 7.5, height = 4.25, units = "in",
       dpi = 500)

# Plot 2
ggplot(cancer_agg_sites_2014, 
       aes(x=forcats::fct_rev(reorder(RACE,RACE)), y = AGE_ADJUSTED_RATE, group = EVENT_TYPE, fill = EVENT_TYPE)) + 
  geom_bar(stat = "identity", position = "dodge") + 
  labs(x = "Race", y = "Age Adjusted Rate per 100,000 People", 
       title = "2014 Cancer Rates by Gender and Race",
       fill = "Event") +
  facet_wrap(~SEX) +
  theme_economist() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 12),
        axis.text.y = element_text(size = 12),
        axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        legend.title = element_text(size = 12)) +
  coord_flip() +
  scale_x_discrete(labels = function(x) str_wrap(x, width = 20))

ggsave('cancer-by-gender-race.png', width = 7.5, height = 4.25, units = "in",
       dpi = 500)

# Plot 3
ggplot(cancer_agg_races_2014, 
       aes(x=forcats::fct_rev(reorder(SITE,SITE)), 
           y = AGE_ADJUSTED_RATE, group = EVENT_TYPE, fill = EVENT_TYPE)) + 
  geom_bar(stat = "identity", position = "dodge") + 
  labs(x = "Leading Site", y = "Age Adjusted Rate per 100,000 People", 
       title = "2014 Cancer Rates\nby Gender and Leading Site\n(20 Cancers with Highest Incidence Rates)",
       fill = "Event") +
  facet_wrap(~SEX) +
  theme_economist() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 12),
        axis.text.y = element_text(size = 12),
        axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        legend.title = element_text(size = 12)) +
  coord_flip()

ggsave('cancer-by-gender-site.png', width = 7.5, height = 8.75, units = "in",
       dpi = 500)