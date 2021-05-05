# Restaurant Suggester
[web app] https://share.streamlit.io/alexhzheng/restaraunt-suggester/main.py     
We use Yelp API to suggest restaurants based on user inputs.  
User inputs location, cuisine, price, open_now, radius, and sort_by parameters.  
Location must be entered or else not possible to search for restaurants.  
Cuisine is type of food user is interested in (Ex: Chinese)  
Price is a rating from $ to $$$$ where $ is 1 and $$$$ is 4. Users can input any number to limit price range.  
Open now is whether or not the restaurant is open now or closed. Users can choose to filter out closed restaurants.  
Radius limits how far out to check for restaurants.  
Sort_by lists the restaurant based on what the user prefers: best match, rating, review_count, distance, or default.
We used dijstraks algorithm to give shortest path of restaurants to visit given user inputted stops

Assumptions:
User must input location and number of stops.
If user leaves other parameters blank, the default parameter will be used.


