import requests 
import json
import streamlit as st
from Graph import Graph
from Dijkstra import Dijkstra

# google maps api
google_api_key = 'AIzaSyAMCpVfZHHTNOIwNTzJWUjYUC9QZayE65k'

# yelp api
yelp_api_key = 'rLYJfRRm94AcvuHNw-KQaBEheO9Fsf5UAbMxtPsWnVUmK4VXmyGIM6md4kAf5yto1gC34h0TQcL26b35lkJ1PKYVeX5AQ0Z1MJSL8wU8lUzX6XhSPD7oXLw2g1t_YHYx'
headers = {'Authorization': 'Bearer %s' % yelp_api_key}

url='https://api.yelp.com/v3/businesses/search'

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


# code for streamlit web app
st.title("Restaurant Suggester")
with st.form(key='my_form'):
    location = st.text_input(label='Enter Location(Ex: philadelphia) (MUST ENTER): ').strip()
    cuisine = st.text_input(label='Enter Cuisine(skip to use default): ').strip()
    budget_param = st.text_input(label='Enter price(1 is cheapest, 4 is most expensive)(skip to use default): ').strip()
    open_param = st.text_input(label='Enter yes or no for open now(skip to use default): ').strip()
    radius = st.text_input(label='Search within x meters(skip to use default): ').strip()
    sort_byinput = st.text_input(label='Enter 1: best match, 2: rating, 3: review count, 4: distance(skip to use default): ').strip()
    stops_input = st.text_input(label='How many restaurants to go to(MUST ENTER) (MAX AMOUNT IS 10): ').strip()
    submit_button = st.form_submit_button(label='Submit')
# set budget
if budget_param == '1':
    budget = 1
elif budget_param == '2':
    budget = 2
elif budget_param == '3':
    budget = 3
elif budget_param == '4':
    budget = 4
else:
    budget = ''

# set open now
if open_param == "yes":
        open_now = True
elif open_param == "no":
    open_now = False
else:
    open_now = ""

# set sort_by 
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


inputs = {'term': cuisine, 'location': location, 'budget': budget, "open_now": open_now, "radius": radius, "sort_by": sort_by}

# filter out empty inputs
params = {}
for k,v in inputs.items():
        if v != '':
            params[k] = v
print(params)

# uncomment these for actual project
# inputs = get_inputs()
# params = filter_out_empty_inputs(inputs)

# Making a get request to the API
# test_params = {'term': "chinese", 'location': "new york", 'radius': 10000}
# stops = int(input("How many restaurants to visit: ").strip())

req = requests.get(url, params=params, headers=headers)
print(req.status_code)

# proceed only if the status code is 200
# while req.status_code != 200:
#     inputs = get_inputs()
#     params = filter_out_empty_inputs(inputs)  


if req.status_code == 200:
    # set stops
    st.header("List of Restaurants")
    data = json.loads(req.text)
    businesses = data['businesses']
    counter = 0

    # prints out name and address of each restaurant
    for business in businesses:
        st.write(str(counter)+": Name:", business['name'])
        st.write("Address:", " ".join(business["location"]["display_address"]), "\n")
        counter += 1
    
    stops = int(stops_input)
    st.header("Restaurant Stop Order:")
    with st.spinner("Running Graph Algorithm. DON'T CHANGE INPUTS"):
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
        # create graph
        graph = Graph(len(names_list))
        for x in range(len(names_list)): 
            for y in range(len(names_list)):
                if not x == y:
                    graph.addEdge(x, y, distances[names_list[x]][names_list[y]])

        #create dijkstra
        dijkstra = Dijkstra()

        #desired number of restaurants (NEED TO IMPLEMENT ASKING USER FOR NUMBER)--using 5 for test


        currentStartingLocation = 0

        visited = []
        visited.append(currentStartingLocation)
        for x in range(stops) :
            shortestList = []
            for y in range(graph.getSize()) :
                shortestList.append(dijkstra.shortestPath(graph, currentStartingLocation, y)[1])
            for z in visited:
                shortestList[z] = 100000000
            closest = min(shortestList)
            indexOfClosest = shortestList.index(closest)
            if x == 0:
                st.write("First stop: " + names_list[indexOfClosest])
            else:
                st.write("Next stop: " + names_list[indexOfClosest])
            currentStartingLocation = indexOfClosest
            visited.append(indexOfClosest)

else: 
    st.warning('Some inputs are wrong. Try Again.')

