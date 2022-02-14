from lorettorbital.orbital import Station
from pprint import pprint
from datetime import datetime, timedelta



# coordinates of the patriot Park
lon, lat, alt = 30.2966, 59.9146, 130 # Azimuth spb

# if you want to use your current coordinates (determined by the ip address)
#lon, lat, alt = getCoords()

# m --> km
alt /= 1000

# start time in UTC
start = datetime.utcnow()

station = Station("testStation", lon, lat, alt, timeZone=3, trackFormat="l2s")

pprint(station.getStation(), indent=4)


print("\n")
station.getSchedule(start, 24*7, printTable=True)

