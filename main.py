import json
import os

import functions_framework
import googlemaps
from yelpapi import YelpAPI

GMAPS_API_KEY_ENV_VAR_NAME = 'GOOGLEMAPS_API_KEY'
YELP_API_KEY_ENV_VAR_NAME = 'YELP_API_KEY'


@functions_framework.http
def get_rating_info(request):
    search_term = request.args['restaurant_name']

    gmaps_client = googlemaps.Client(key=_load_api_key(GMAPS_API_KEY_ENV_VAR_NAME))

    # force a Chicago lat/lng - the Places API uses IP geolocation by default, which is problematic when we go  through
    # a service like Google Cloud
    gmaps_places = gmaps_client.places(query=search_term, location='41.8757, -87.6243')['results']
    if len(gmaps_places) != 1:
        print(f'Warning - found more than one gmaps place for "{search_term}", may be inaccurate')

    gmaps_place = gmaps_places[0]
    print(f'Google Review Score {gmaps_place["rating"]} ({gmaps_place["user_ratings_total"]} user ratings)')

    with YelpAPI(_load_api_key(YELP_API_KEY_ENV_VAR_NAME)) as yelp_api:
        yelp_business = yelp_api.search_query(location='Chicago', term=search_term, limit=1)['businesses'][0]
        print(f'Yelp (Rounded) Review Score {yelp_business["rating"]} ({yelp_business["review_count"]} '
              f'user ratings)')

    return {
        'google_rating': gmaps_place['rating'],
        'google_num_ratings': gmaps_place['user_ratings_total'],
        'yelp_rating': yelp_business['rating'],
        'yelp_num_ratings': yelp_business['review_count'],
    }


def _load_api_key(env_var_name):
    api_key = os.getenv(env_var_name)
    if api_key is not None:
        return api_key

    with open('creds.json') as creds_file:
        creds = json.load(creds_file)
        return creds[env_var_name]
