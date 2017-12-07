# Libraries
library(leaflet)
library(htmlwidgets)
library(htmltools)

# Read in data
terrorism_2016 <- read.csv("terrorism_2016.csv", header=TRUE)

# Create a location that is either city + state if in the US or city + country if outside the US
loc_maker <- function(country, city, state) {
  if (country == "United States") {
    return(paste0(city, ", ", state))
  }
  else {
    return(paste0(city, ", ", country))
  }
}

terrorism_2016$location <- mapply(loc_maker, terrorism_2016$country_txt, terrorism_2016$city, terrorism_2016$provstate)

# Make popups for the map
popup <- paste0("<br><strong>Location: </strong>", 
                terrorism_2016$location,
                "<br><strong>Date: </strong>", 
                terrorism_2016$imonth, "/", terrorism_2016$iday, "/", terrorism_2016$iyear,
                "<br><strong>Number of People Killed: </strong>", 
                terrorism_2016$nkill,
                "<br><strong>Incident Summary: </strong>", 
                terrorism_2016$summary)

# Create map
m <- leaflet(terrorism_2016) %>% 
  addProviderTiles(providers$CartoDB.Positron) %>% 
  setView(lng = 0.0, lat = 42.3601, zoom = 2) %>% addMarkers(
    popup = popup,
    clusterOptions = markerClusterOptions()
  )

# Save map
saveWidget(m, '2016_terrorism_map.html', selfcontained = TRUE)
