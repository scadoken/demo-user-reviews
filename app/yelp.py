
import requests

from urllib.parse import quote
from typing import NamedTuple, Optional
from dataclasses import dataclass

from config import YelpConfig


class Address(NamedTuple):
    street: str
    street2: Optional[str]
    city: str
    state: str
    zip: str


@dataclass
class Business:
    """Class for keeping track of yelp business info"""
    id: str
    name: str
    address: Address
    phone: str
    reviews: Optional[list]


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


class Yelp:
    """Yelp API client using v3 of the API."""
    
    def __init__(
            self,
            default_search_limit: int = 10,
        ) -> None:
        
        # default vars
        self.default_search_limit = default_search_limit
        self.config = YelpConfig()


    def get_request(self, api:str, params:Optional[dict]=None) -> dict:
        """send a GET request to the API.

        Args:
            url (str): The URL to send the request to.
            headers (dict): The headers to include in the request.
            params (dict): The parameters to include in the request.

        Returns:
            dict: The JSON response from the request.

        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url = '{0}{1}'.format(self.config.api_host, quote(api.encode('utf8')))
        response = requests.request('GET', url, headers=self.config.headers, params=params)
        response.raise_for_status()
        return response.json()
    

    def get_businesses(self, search_term:str, location:str, search_limit:int=0) -> dict:

        api = '/v3/businesses/search'

        url_params = {
            'term': search_term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': search_limit or self.default_search_limit
        }

        response = self.get_request(api, params=url_params)

        return response
    

    def get_business_reviews(self, business_id:str, review_limit:int=0) -> dict:

        api = f'/v3/businesses/{business_id}/reviews'

        url_params = {
            'limit': review_limit or self.default_search_limit
        }

        response = self.get_request(api, params=url_params)

        return response

    

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

