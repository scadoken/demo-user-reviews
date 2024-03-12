import os
from dotenv import load_dotenv
from typing import NamedTuple
from dataclasses import dataclass

# TODO switch to dataclass
class YelpConfig:
    """class for managing yelp config parameters."""
    
    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv('YELP_CLIENT_ID')
        self.api_key = os.getenv('YELP_API_KEY')
        self.api_host = 'https://api.yelp.com'
        self.headers = {
            'Authorization': 'Bearer %s' % self.api_key,
        }
