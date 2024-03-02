import unittest
from typing import NamedTuple
from app.yelp import Yelp, YelpConfig, get_config
from unittest.mock import patch

def test_YelpConfig():
    config = YelpConfig(
        client_id='CLIENT_ID',
        api_key='API_KEY',
        api_host='API_HOST',
        search_path='SEARCH_PATH',
        business_path='BUSINESS_PATH'
    )
    
    assert config.client_id == 'CLIENT_ID'
    assert config.api_key == 'API_KEY'
    assert config.api_host == 'API_HOST'
    assert config.search_path == 'SEARCH_PATH'
    assert config.business_path == 'BUSINESS_PATH'
    assert issubclass(YelpConfig, tuple)
    assert isinstance(config, tuple)
    assert hasattr(config, '_asdict')
    assert hasattr(config, '_fields')


class TestGetConfig(unittest.TestCase):
    @patch('os.getenv')
    def test_get_config(self, mock_getenv):
        mock_getenv.side_effect = ['client_id', 'api_key']

        expected_config = YelpConfig('client_id', 'api_key', 'https://api.yelp.com', '/v3/businesses/search', '/v3/businesses/')
        actual_config = get_config()

        self.assertEqual(actual_config, expected_config)


class TestYelp(unittest.TestCase):

    def setUp(self):
        config = YelpConfig(
            client_id='CLIENT_ID',
            api_key='API_KEY',
            api_host='API_HOST',
            search_path='SEARCH_PATH',
            business_path='BUSINESS_PATH'
        )
        self.config = config
        self.yelp = Yelp(config=self.config)


    def test_initialize_no_config(self):
        self.yelp = Yelp()
        assert self.yelp.default_search_limit == 10


    def test_initialize_with_config(self):
        
        self.yelp = Yelp(config=self.config)
        assert self.yelp.config == self.config


    @patch('yelp.requests.request')
    def test_get_businesses(self, mock_request):
        
        mock_response = {
            'businesses': [
                {'name': 'Restaurant 1', 'location': 'Location 1'},
                {'name': 'Restaurant 2', 'location': 'Location 2'}
            ]
        }
        mock_request.return_value.json.return_value = mock_response

        search_term = 'restaurant'
        location = 'New York'
        search_limit = 5

        result = self.yelp.get_businesses(search_term, location, search_limit)

        mock_request.assert_called_once_with(
            'GET',
            f'{self.yelp.config.api_host}{self.yelp.config.search_path}',
            headers={'Authorization': f'Bearer {self.config.api_key}'},
            params={'term': 'restaurant', 'location': 'New+York', 'limit': 5}
        )
        self.assertEqual(result, mock_response)


