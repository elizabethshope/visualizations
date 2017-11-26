# Elizabeth Shope
# Leaflet R Cancer and Refineries Map Plot

# Get libraries
library(rgdal)
library(noncensus)
library(sp)
library(leaflet)
library(htmlwidgets)

# Load US map (from https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html)
us.map <- readOGR(dsn = ".", layer = "cb_2016_us_county_20m", stringsAsFactors = FALSE)

# Load petroleum refinery and power plant data
refineries <- readOGR(dsn = ".", layer = "Petroleum_Refineries_2017", stringsAsFactors = FALSE)
power_plants <- readOGR(dsn = ".", layer = "PowerPlants_US_201707", stringsAsFactors = FALSE)

# Turn petroleum refinery & power plant data into simplified data frames
refineries_df <- data.frame(cbind(refineries$Corp, refineries$Site, refineries$State, refineries$Latitude, refineries$Longitude))
colnames(refineries_df) <- c("corp", "site", "state", "lat", "lng")

power_plants_df <- data.frame(cbind(power_plants$Plant_Name, power_plants$Utility_Na, power_plants$sector_nam, 
                         power_plants$City, power_plants$StateName, power_plants$PrimSource, 
                         power_plants$Total_MW, power_plants$Latitude, power_plants$Longitude))
colnames(power_plants_df) <- c("name", "utility_name", "sector", "city", "state", "source", "mw", "lat", "lng")

# Remove refineries outside continental US
refineries_df <- refineries_df[!refineries_df$state %in% c("Hawaii", "Alaska"),]

# Convert lats and lngs & mw to floats
refineries_df$lat <- as.numeric(as.character(refineries_df$lat))
refineries_df$lng <- as.numeric(as.character(refineries_df$lng))
power_plants_df$lat <- as.numeric(as.character(power_plants_df$lat))
power_plants_df$lng <- as.numeric(as.character(power_plants_df$lng))
power_plants_df$mw <- as.numeric(as.character(power_plants_df$mw))

# Extract data about coal power plants
# Remove power plants outside of continental US
# Remove power plants under 1000 MW
coal_power_plants <- power_plants_df[power_plants_df$source == "coal" &
                                       !power_plants_df$state %in% c("Hawaii", "Alaska") &
                                       power_plants_df$mw >= 1000,]

# Remove Alaska(2), Hawaii(15), Puerto Rico (72), Guam (66), Virgin Islands (78), American Samoa (60)
#  Mariana Islands (69), Micronesia (64), Marshall Islands (68), Palau (70), Minor Islands (74)
us.map <- us.map[!us.map$STATEFP %in% c("02", "15", "72", "66", "78", "60", "69",
                                        "64", "68", "70", "74"),]

# Make sure other outling islands are removed.
us.map <- us.map[!us.map$STATEFP %in% c("81", "84", "86", "87", "89", "71", "76",
                                        "95", "79"),]

# Load zip code and county data from noncensus library
data(zip_codes)
data(counties)

# Load data sets
# Note: Cancer data originally from https://www.statecancerprofiles.cancer.gov/incidencerates/index.php
nh_lymphoma <- read.csv("nh_lymphoma.csv", header = TRUE)
CancerRates <- read.csv('CancerCountyFIPS.csv')

# Make all the column names lowercase
names(nh_lymphoma) <- tolower(names(nh_lymphoma))
names(CancerRates) <- tolower(names(CancerRates))

# Rename columns to make for a clean df merge later
colnames(nh_lymphoma) <- c("location", "GEOID", "rate")
colnames(CancerRates) <- c("location", "GEOID", "rate")

# Add leading zeos to any FIPS/GEOID code that's less than 5 digits long to get a good match
nh_lymphoma$GEOID <- formatC(nh_lymphoma$GEOID, width = 5, format = "d", flag = "0")
CancerRates$GEOID <- formatC(CancerRates$GEOID, width = 5, format = "d", flag = "0")

# Convert column called location to two columns: State and County
nh_lymphoma <- separate(nh_lymphoma, location, into = c("county", "state"), sep = ", ")
CancerRates <- separate(CancerRates, location, into = c("county", "state"), sep = ", ")

# Fix issues of missing states (e.g. DC and Puerto Rico)
missing_state <- which(is.na(nh_lymphoma$state))
for (i in 1:length(missing_state)) {
  nh_lymphoma[missing_state[i],"state"] = nh_lymphoma[missing_state[i],"county"]
  nh_lymphoma[missing_state[i],"county"] = gsub("\\s*\\([^\\)]+\\)", "", nh_lymphoma[missing_state[i],"county"])
}

missing_state <- which(is.na(CancerRates$state))
for (i in 1:length(missing_state)) {
  CancerRates[missing_state[i],"state"] = CancerRates[missing_state[i],"county"]
  CancerRates[missing_state[i],"county"] = gsub("\\s*\\([^\\)]+\\)", "", CancerRates[missing_state[i],"county"])
}

# Remove the (...) from the state values
nh_lymphoma[] <- lapply(nh_lymphoma, function(x) gsub("\\s*\\([^\\)]+\\)", "", x))
CancerRates[] <- lapply(CancerRates, function(x) gsub("\\s*\\([^\\)]+\\)", "", x))

# Remove the space# from the end of some of the values in the rate column of CancerRates
CancerRates[] <- lapply(CancerRates, function(x) gsub("\\#", "", x))

# Convert full state names to abbreviations for a clean df merge later.
nh_lymphoma$state <- state.abb[match(nh_lymphoma$state,state.name)]
CancerRates$state <- state.abb[match(CancerRates$state,state.name)]

# Convert cancer rates to numeric value
nh_lymphoma$rate <- as.numeric(as.character(nh_lymphoma$rate))
CancerRates$rate <- as.numeric(as.character(CancerRates$rate))

# Merge spatial df with downloaded data (using merge function from sp library)
nh_lymphoma_map <- merge(us.map, nh_lymphoma, by=c("GEOID"))
cancermap <- merge(us.map, CancerRates, by=c("GEOID"))

### CREATE POP-UPS ### 
# Make popup for non-hodgkin lymphoma
popup_nh_lymphoma <- paste0("<strong>County: </strong>", 
                           nh_lymphoma_map$county, 
                           "<br><strong>State: </strong>", 
                           nh_lymphoma_map$state, 
                           "<br><strong>Non-Hodgkin Lymphoma Rate (Age Adjusted)
                           <br>    Out of 100,000: </strong>", 
                           nh_lymphoma_map$rate)

# Make popup for overall cancer rate
popup_cancer <- paste0("<strong>County: </strong>", 
                       cancermap$county, 
                       "<br><strong>State: </strong>", 
                       cancermap$state, 
                       "<br><strong>Cancer Rate (Age Adjusted)
                       <br>    Out of 100,000: </strong>", 
                       cancermap$rate)

# Make popup for coal power plants
popup_coal <- paste0("<i><strong>Coal Power Plant</strong></i>",
                     "<br><strong>City, State: </strong>", 
                     coal_power_plants$city, ", ", coal_power_plants$state,
                     "<br><strong>Facility Name: </strong>", 
                     coal_power_plants$name,  
                     "<br><strong>Utility Name: </strong>", 
                     coal_power_plants$utility_name,
                     "<br><strong>Power Generation: </strong>", 
                     coal_power_plants$mw, " MW")

# Make popup for petroleum refineries
popup_refineries <- paste0("<i><strong>Petroleum Refinery</strong></i>",
                           "<br><strong>Location: </strong>", 
                           refineries_df$site, ", ", refineries_df$state,
                           "<br><strong>Owner: </strong>", 
                           refineries_df$corp)

# Set color palette
pal <- colorQuantile("YlOrRd", NULL, n = 9)

# Set icons
# coalplant_icons <- awesomeIcons(
#   icon = 'industry',
#   iconColor = 'black',
#   library = 'fa'#,
#   #markerColor = "lightgray"
# )

# refinery_icons <- awesomeIcons(
#   icon = 'tint',
#   iconColor = 'black',
#   library = 'fa'
# )
coalplant_icons <- icons(
  iconUrl = "power_plant.svg",
  iconWidth = 30, iconHeight = 30
)

refinery_icons <- icons(
  iconUrl = "oil_barrel.svg",
  iconWidth = 30, iconHeight = 30
)

# Create map
gmap <- leaflet() %>%
  addTiles() %>%
  setView(lng = -97, lat = 38.5, zoom = 4) %>% 
  addPolygons(data = nh_lymphoma_map, 
              fillColor = ~pal(rate), 
              fillOpacity = 0.8, 
              color = "#BDBDC3", 
              weight = 1,
              popup = popup_nh_lymphoma,
              group="Lymphoma Rate/100,000 by Counties") %>%
  addPolygons(data = cancermap, 
              fillColor = ~pal(rate), 
              fillOpacity = 0.8, 
              color = "#BDBDC3", 
              weight = 1,
              popup = popup_cancer,
              group="Cancer Rate/100,000 by Counties") %>%
  addMarkers(data=refineries_df,lat=~lat, lng=~lng, popup=popup_refineries, 
                    icon=~refinery_icons, group = "Petroleum Refineries") %>% 
  addMarkers(data=coal_power_plants,lat=~lat, lng=~lng, popup=popup_coal, 
                    icon=~coalplant_icons, group = "Coal Power Plants Over 1000 MW") %>% 
  addLayersControl(
    baseGroups = c("Lymphoma Rate/100,000 by Counties", "Cancer Rate/100,000 by Counties"),
    overlayGroups = c("Petroleum Refineries", "Coal Power Plants Over 1000 MW"),
    options = layersControlOptions(collapsed = FALSE))

gmap
saveWidget(gmap, 'cancer_powerplant_refinery_map.html', selfcontained = TRUE)
