import json
import os
import sys

import googlemaps
from yelpapi import YelpAPI

GMAPS_API_KEY_ENV_VAR_NAME = 'GOOGLEMAPS_API_KEY'
YELP_API_KEY_ENV_VAR_NAME = 'YELP_API_KEY'


def main(argv):
    gmaps_client = googlemaps.Client(key=_load_api_key(GMAPS_API_KEY_ENV_VAR_NAME))

    search_term = argv[1]

    places_found = gmaps_client.places(search_term)['results']
    if len(places_found) != 1:
        raise ValueError(f'Found {len(places_found)} results for "{search_term}", expected 1')

    place = places_found[0]
    print(f'Google Review Score {place["rating"]} ({place["user_ratings_total"]} user ratings)')

    with YelpAPI(_load_api_key(YELP_API_KEY_ENV_VAR_NAME)) as yelp_api:
        yelp_business_found = yelp_api.search_query(location='Chicago', term=search_term, limit=1)['businesses'][0]
        print(f'Yelp (Rounded) Review Score {yelp_business_found["rating"]} ({yelp_business_found["review_count"]} '
              f'user ratings)')


def _load_api_key(env_var_name):
    api_key = os.getenv(env_var_name)
    if api_key is not None:
        return api_key

    with open('creds.json') as creds_file:
        creds = json.load(creds_file)
        return creds[env_var_name]


if __name__  == '__main__':
    main(sys.argv)