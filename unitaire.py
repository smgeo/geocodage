from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="tastament")
location = geolocator.geocode("casablanca maroc ")
print(location)
print((location.latitude, location.longitude))