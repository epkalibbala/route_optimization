import pandas as pd
import requests
import gmaps
from datetime import datetime
import googlemaps

apikey = 'ApiKey'

address_list = ["Yumbe, Uganda", "Arua, Uganda", "Nebbi, Uganda",
                "Adjumani, Uganda", "Gulu, Uganda", "Kitgum, Uganda", "Oyam, Uganda", "Lira, Uganda",
                "Moroto, Uganda", "Kiryadongo, Uganda", "Soroti, Uganda", "Kapchorwa, Uganda", "Nakasongola, Uganda",
                "Masindi, Uganda", "Pallisa, Uganda", "Hoima, Uganda", "Mbale, Uganda", "Kamuli, Uganda",
                "Mbale, Uganda",
                "Kayunga, Uganda", "Luwero, Uganda", "Tororo, Uganda", "Busia, Uganda", "Bugiri, Uganda",
                "Iganga, Uganda",
                "Jinja, Uganda", "Mukono, Uganda", "Kampala, Uganda", "Luwero, Uganda", "Masaka, Uganda",
                "Lyantonde, Uganda",
                "Mbarara, Uganda", "Mubende, Uganda", "Kyenjojo, Uganda", "Kagadi, Uganda", "Fortportal, Uganda",
                "Kasese, Uganda",
                "Ibanda, Uganda", "Bushenyi, Uganda", "Runkungiri, Uganda", "Ntungamo, Uganda", "Kisoro, Uganda",
                "Kabale, Uganda",
                ]

results = []
locations_latitude = []
locations_longitude = []
formatted_address = []
for location_string in address_list:
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s' %
                     (location_string, apikey))
    result = r.json()['results']
    print(result)
    location = result[0]['geometry']['location']
    locations_longitude.append(location['lng'])
    locations_latitude.append(location['lat'])
    formatted_address.append(result[0]['formatted_address'])
    results.append(result)

df = pd.DataFrame({'address': address_list, 'latitude': locations_latitude, 'longitude': locations_longitude,
                   'formatted_address': formatted_address})  #
# df.to_csv(r'C:/Users/emmanuelk/Desktop/excel/route optimization/address points.csv', index=False)
print(df)

origin = (3.469802, 31.248329)  # Yumbe
destination = (2.772404, 32.288073)  # Gulu
waypoints = [(3.030330, 30.907304), (2.477817, 31.085102), (3.378381, 31.782228),
             ]

now = datetime.now()

# configure api
gmaps.configure(api_key=apikey)

# Create the map
fig = gmaps.figure()
# create the layer
layer = gmaps.directions.Directions(origin, destination, waypoints=waypoints, optimize_waypoints=True,
                                    mode='car', api_key=apikey, departure_time=now)
# Add the layer
fig.add_layer(layer)
print(fig)

origin_dir = '0.940076, 30.812564'
destination_dir = '0.347596, 32.582520'
# waypoints_dir = ['''3.378381,  31.782228|2.477817,  31.085102|3.030330,  30.907304|3.288485,  32.878950|
# 2.277628,  32.446724|2.258083,  32.887407|2.528223,  34.657998|2.017991,  32.083745|1.713181,  33.606386|1.397297,  34.448938|
# 1.311898,  32.463708|1.687313,  31.713846|1.170697,  33.709857|0.354866, 32.752014|1.078444,  34.181006|0.944785,  33.126717|
# 1.078444,  34.181006|0.701371,  32.902909|0.840409,  32.497668|0.678227, 34.186567|0.470669,  34.091980|0.567136,  33.746185|
# 0.604583,  33.471983|0.447857,  33.202612|1.427355, 31.348445''']
waypoints_dir = ['''-0.3380637,31.717877|-0.407504, 31.156720|-0.607160, 30.654502|0.553901, 31.388467|
0.609292, 30.640123|0.654626, 30.280117|0.169899, 30.078078|-0.116716, 30.499121|-0.542377, 30.196452|
-0.791139, 29.924903|-0.875076, 30.265695|-1.283431, 29.690475|-1.241956, 29.985616''']

now = datetime.now()

#### Setting u the API key to connect to Google maps API

# Perform request to use the Google Maps API web service
gmaps = googlemaps.Client(key=apikey)

for i in waypoints_dir:
    directions = gmaps.directions(origin=origin_dir, waypoints=i, destination=destination_dir,
                                  mode='driving', optimize_waypoints=True, departure_time=now)

origin_district = []
destination_district = []
est = []
distance = []
location_values_start = []

for i in range(0, 13):
    origin_district.append(directions[0]['legs'][i]['start_address'])
    destination_district.append(directions[0]['legs'][i]['end_address'])
    est.append(directions[0]['legs'][i]['duration']['text'])
    distance.append(directions[0]['legs'][i]['distance']['text'])
    location_values_start.append(directions[0]['legs'][i]['start_location'])
    print(directions[0]['legs'][i]['distance']['text'])
    print(directions[0]['legs'][i]['duration']['text'])
    print(directions[0]['legs'][i]['start_address'])
    print(directions[0]['legs'][i]['end_address'])
    print(directions[0]['legs'][i]['start_location'])

df_two = pd.DataFrame({'Origin': origin_district, 'Destination': destination_district, 'ET': est,
                       'Distance': distance, 'Origin address points': location_values_start})  #
df_three = pd.read_csv(r'C:/Users/emmanuelk/Desktop/excel/route optimization/distance.csv')
result = pd.concat([df_three, df_two], ignore_index=True)
result.to_csv(r'C:/Users/emmanuelk/Desktop/excel/route optimization/Route estimates.csv', index=False)

# origin_dirII = '1.078444,  34.181006'
# destination_dirII = '2.772404,  32.288073'
# waypoints_dirII = ['''
# 0.604583,  33.471983|0.447857,  33.202612|0.354866,  32.752014|0.347596,  32.582520|0.840409,  32.497668|-0.446369,  31.901795|
# -0.407504,  31.156720|-0.607160,  30.654502|0.553901,  31.388467|0.609292,  30.640123|0.940076,  30.812564|0.654626,  30.280117|
# 0.169899,  30.078078|-0.116716,  30.499121|-0.542377,  30.196452|-0.791139,  29.924903|-0.875076,  30.265695|-1.283431,  29.690475|
# -1.241956,  29.985616''']
#
# nowII = datetime.now()
#
# #### Setting u the API key to connect to Google maps API
#
# # Perform request to use the Google Maps API web service
# gmapsII = googlemaps.Client(key=apikey)
#
# for i in waypoints_dir:
#     directionsII = gmapsII.directions(origin=origin_dir, waypoints=i, destination=destination_dir,
#                                   mode='driving', optimize_waypoints=True, departure_time=now)
#
# for i in range(0, 5):
#     print(directionsII[0]['legs'][i]['distance']['text'])
#     print(directionsII[0]['legs'][i]['duration']['text'])
#     print(directionsII[0]['legs'][i]['start_address'])
#     print(directionsII[0]['legs'][i]['end_address'])


start_address = []
end_address = []
distance = []
journey_time = []

for i in range(0, (len(df) - 1)):
    distance.append(directions[0]['legs'][i]['distance']['text'])
    journey_time.append(directions[0]['legs'][i]['duration']['text'])
    start_address.append(directions[0]['legs'][i]['start_address'])
    end_address.append(directions[0]['legs'][i]['end_address'])

df_distance = pd.DataFrame({'start_address': start_address, 'end_address': end_address,
                            'distance': distance, 'journey_time': journey_time},
                           columns=['start_address', 'end_address', 'distance', 'journey_time'])

print(df_distance)
