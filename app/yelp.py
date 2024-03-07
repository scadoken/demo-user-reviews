import argparse
import json
import os
import pprint
import requests
import sys
import urllib
from dotenv import load_dotenv
from urllib.parse import quote
from typing import NamedTuple, Optional


class YelpConfig(NamedTuple):
    """Named tuple for Yelp API configuration."""
    client_id: str
    api_key: str
    api_host: str
    search_path: str
    business_path: str
    url: str
    headers: dict



# environment vars
def get_config() -> YelpConfig:
    """Get Yelp API configuration from environment variables."""
    load_dotenv() 
    CLIENT_ID = os.getenv('YELP_CLIENT_ID')
    API_KEY = os.getenv('YELP_API_KEY')
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    return YelpConfig(
        CLIENT_ID,
        API_KEY,
        API_HOST,
        SEARCH_PATH,
        BUSINESS_PATH,
        url,
        headers,
    )


class Yelp:
    """Yelp API client using v3 of the API."""
    
    def __init__(
            self,
            default_search_limit: int = 10,
            config: Optional[YelpConfig] = None,
        ) -> None:
        
        self.config = config
        
        # default vars
        self.default_search_limit = default_search_limit


    def get_businesses(self, search_term:str, location:str, search_limit:int=0) -> dict:
        """send a GET request to the API.

        Args:
            search_term (str): The term to search for (i.e. 'restaurants' or 'plumber').
            location (str): The location to search (i.e. 'San Francisco, CA').
            search_limit (str): The max limit of results to return (i.e. 10).

        Returns:
            dict: The JSON response from the request.

        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = {
            'term': search_term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': search_limit or self.default_search_limit
        }

        print(u'Querying {0} ...'.format(self.config.url))

        response = requests.request('GET', self.config.url, headers=self.config.headers, params=url_params)

        return response.json()
    

class Business:

    def __init__(self):
        pass


    def get_engagement_metrics(self):
        # https://docs.developer.yelp.com/reference/v3_get_businesses_engagement
        pass


    def get_popularity_scores(self):
        # https://docs.developer.yelp.com/reference/v3_businesses_insights
        pass


    def get_reviews(self):
        # https://docs.developer.yelp.com/reference/v3_business_reviews
        pass


    def get_review_highlights(self):
        # https://docs.developer.yelp.com/reference/v3_business_review_highlights
        pass

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-q', '--term', dest='term', default='plumber', type=str, help='Search term (default: plumber)')
#     parser.add_argument('-l', '--location', dest='location', default='Santa Ana, CA', type=str, help='Search location (default: Santa Ana, CA)')
#     parser.add_argument('-s', '--search_limit', dest='search_limit', default=10, type=int, help='Search limit (default: 10)')
#     input_values = parser.parse_args()
    
#     config = get_config()
#     yelp = Yelp(config=config)
#     response = yelp.get_businesses(input_values.term, input_values.location, input_values.search_limit)
#     print(json.dumps(response, indent=2))

