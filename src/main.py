import json
import os
import sys

import googlemaps

GMAPS_API_KEY_ENV_VAR_NAME = 'GOOGLEMAPS_API_KEY'


def main(argv):
    gmaps = googlemaps.Client(key=_load_gmaps_api_key())

    search_term = argv[1]

    places_found = gmaps.places(search_term)['results']
    if len(places_found) != 1:
        raise ValueError(f'Found {len(places_found)} results for "{search_term}", expected 1')

    place = places_found[0]
    print(f'Review Score {place["rating"]} ({place["user_ratings_total"]} user ratings)')


def _load_gmaps_api_key():
    gmaps_api_key = os.getenv(GMAPS_API_KEY_ENV_VAR_NAME)
    if gmaps_api_key is not None:
        return gmaps_api_key

    with open('creds.json') as creds_file:
        creds = json.load(creds_file)
        return creds[GMAPS_API_KEY_ENV_VAR_NAME]


if __name__  == '__main__':
    main(sys.argv)