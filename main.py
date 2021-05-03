import requests 
import json
from Graph import Graph
from Dijkstra import Dijkstra

# google maps api
google_api_key = 'AIzaSyAMCpVfZHHTNOIwNTzJWUjYUC9QZayE65k'

# yelp api
yelp_api_key = 'rLYJfRRm94AcvuHNw-KQaBEheO9Fsf5UAbMxtPsWnVUmK4VXmyGIM6md4kAf5yto1gC34h0TQcL26b35lkJ1PKYVeX5AQ0Z1MJSL8wU8lUzX6XhSPD7oXLw2g1t_YHYx'
headers = {'Authorization': 'Bearer %s' % yelp_api_key}

url='https://api.yelp.com/v3/businesses/search'


# search based on cuisine(term), location, price, time, rating, radius, sort_by
def get_inputs():
    print("Enter parameters for search(enter (enter key) to leave parameter empty)")
    print("MUST ENTER LOCATION")
    location = input("Enter a location: ").strip()
    while location == '':
        location = input("Enter a location: ").strip()

    cuisine = input("Enter a cuisine: ").strip()
    budget = input("Enter price(1 is cheapest, 4 is most expensive): ").strip()
    open_param = input("Enter yes or no for open now: ").strip()
    if open_param == "yes":
        open_now = True
    elif open_param == "no":
        open_now = False
    else:
        open_now = ""

    radius = input("Search within x meters: ").strip()
    sort_byinput = input("Enter 1: best match, 2: rating, 3: review count, 4: distance: ").strip()
    if sort_byinput == '1':
        sort_by = "best_match"
    elif sort_byinput == '2':
        sort_by = "rating"
    elif sort_byinput == '3':
        sort_by = "review_count"
    elif sort_byinput == '4':
        sort_by = "distance"
    else:
        sort_by = ""

    return {'term': cuisine, 'location': location, 'budget': budget, "open_now": open_now, "radius": radius, "sort_by": sort_by}


#param dictionary for search query
def filter_out_empty_inputs(inputs):
    for k,v in inputs.items():
        if v != '':
            inputs[k] = v
    return inputs

def get_list_keys(dict):
    keys = []
    for key in dict.keys():
        keys.append(key)
    return keys

def get_list_values(dict):
    values = []
    for value in dict.values():
        values.append(value)
    return values

# uncomment these for actual project
inputs = get_inputs()
params = filter_out_empty_inputs(inputs)

# Making a get request to the API
# test_params = {'term': "chinese", 'location': "new york", 'radius': 10000}
stops = int(input("How many restaurants to visit: "))

req = requests.get(url, params=params, headers=headers)

# proceed only if the status code is 200
while req.status_code != 200:
    inputs = get_inputs()
    params = filter_out_empty_inputs(inputs)  



data = json.loads(req.text)
businesses = data['businesses']

# prints out name and address of each restaurant
print("List of restaurants")
for business in businesses:
    print("Name:", business['name'])
    print("Address:", " ".join(business["location"]["display_address"]), "\n")

# dictionary with all the latitude/longitude of restaurants
# use for graphing algorithm
coordinates = {}
region = data['region']
coordinates['Starting Location'] = region['center']
for business in businesses:
    coordinates[business['name']] = business['coordinates']

# key-value pair test
# for k,v in coordinates.items():
#     print("name:", k)
#     print("coordinates", v)
#     print()

# getting distances between every restaurants
size_of_list = len(coordinates)
names_list = get_list_keys(coordinates)
coordinates_list = get_list_values(coordinates)
distances = {}
for i in range(size_of_list):
    source = str(coordinates_list[i]['latitude']) + ',' + str(coordinates_list[i]['longitude'])
    distances[names_list[i]] = {}
    for j in range(size_of_list):
        if i != j:
            dest = str(coordinates_list[j]['latitude']) + ',' + str(coordinates_list[j]['longitude'])
            r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?' + 'origins=' + str(source) +
                            '&destinations=' + str(dest) +
                            '&key=' + google_api_key)
            x = r.json()
            time_number = x['rows'][0]['elements'][0]['duration']['text'][0]
            distances[names_list[i]][names_list[j]] = time_number

        else:
            distances[names_list[i]][names_list[j]] = 0


# key-value pair test for distances
# for k,v in distances.items():
#     print("\nStart:", k)
#     for key in v:
#         print(key + ":", v[key])



