import requests 
import json

api_key = 'rLYJfRRm94AcvuHNw-KQaBEheO9Fsf5UAbMxtPsWnVUmK4VXmyGIM6md4kAf5yto1gC34h0TQcL26b35lkJ1PKYVeX5AQ0Z1MJSL8wU8lUzX6XhSPD7oXLw2g1t_YHYx'
headers = {'Authorization': 'Bearer %s' % api_key}

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

    radius = input("Search within meters: ").strip()
    sort_byinput = input("Enter 1: best match, 2: rating, 3: review count, 4: distance: ").strip()
    if sort_byinput == 1:
        sort_by = "best_match"
    elif sort_byinput == 2:
        sort_by = "rating"
    elif sort_byinput == 3:
        sort_by = "review_count"
    elif sort_byinput == 4:
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


# uncomment these for actual project
# inputs = get_inputs()
# params = filter_out_empty_inputs(inputs)


# Making a get request to the API
test_params = {'term': "chinese", 'location': "new york"}

req = requests.get(url, params=test_params, headers=headers)

# proceed only if the status code is 200
# while req.status_code != 200:
    # inputs = get_inputs()
    # params = filter_out_empty_inputs(inputs)  

data = json.loads(req.text)
businesses = data['businesses']

# prints out name and address of each restaurant
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