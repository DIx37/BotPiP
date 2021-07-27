from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='rir7m')
location = geolocator.geocode("Москва, поселение Воскресенское, д.30")
print(location.address)
print(location.latitude, location.longitude)
print(location.raw)