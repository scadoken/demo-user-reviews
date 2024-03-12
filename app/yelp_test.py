import unittest
from app.yelp import Yelp, Address, Business
from app.config import YelpConfig
from unittest.mock import patch
from urllib.parse import quote


class TestAddress(unittest.TestCase):

    def test_basic(self):
        street = 'street'
        street2 = 'street2'
        city = 'city'
        state = 'state'
        zip = 'zip'

        addr = Address(
            street=street,
            street2=street2,
            city=city,
            state=state,
            zip=zip,
        )
        assert addr.street == street
        assert addr.street2 == street2
        assert addr.city == city
        assert addr.state == state
        assert addr.zip == zip
        assert issubclass(Address, tuple)
        assert isinstance(addr, tuple)
        assert hasattr(addr, '_asdict')
        assert hasattr(addr, '_fields')


    def test_missing_addr2(self):
        street = 'street'
        street2 = None
        city = 'city'
        state = 'state'
        zip = 'zip'

        addr = Address(
            street=street,
            street2=street2,
            city=city,
            state=state,
            zip=zip,
        )
        assert addr.street == street
        assert addr.street2 == street2
        assert addr.city == city
        assert addr.state == state
        assert addr.zip == zip


class TestBusiness(unittest.TestCase):

    def test_default(self):
        id = '111'
        name = 'ABC Corp'
        address = '123 Main'
        phone = '(123) 456-7890'
        reviews = []

        biz = Business(
            id=id,
            name=name,
            address=address,
            phone=phone,
            reviews=reviews,
        )
        assert biz.id == id
        assert biz.name == name
        assert biz.address == address
        assert biz.phone == phone
        assert biz.reviews == reviews

        
        

class TestYelp(unittest.TestCase):
    @patch('os.getenv')
    def setUp(self, mock_getenv):
        client_id = 'client_id'
        api_key = 'api_key'
        mock_getenv.side_effect = [client_id, api_key]

        self.yelp = Yelp()

    def test_config(self):
        
        assert self.yelp.config.client_id == 'client_id'
        assert self.yelp.config.api_key == 'api_key'

    def test_initialize(self):
        self.yelp = Yelp()
        assert self.yelp.default_search_limit == 10


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
            f'{self.yelp.config.api_host}{quote("/v3/businesses/search".encode("utf8"))}',
            headers={'Authorization': f'Bearer {self.yelp.config.api_key}'},
            params={'term': 'restaurant', 'location': 'New+York', 'limit': 5}
        )
        self.assertEqual(result, mock_response)
    

    @patch('yelp.requests.request')
    def test_get_business_reviews(self, mock_request):
        mock_response = {
            'reviews': [
                {'user': 'John Doe', 'rating': 5, 'review': 'best company ever!'},
                {'user': 'Jane Doe', 'rating': 1, 'review': 'worst place to go'}
            ]
        }

        mock_request.return_value.json.return_value = mock_response

        biz_id='some_id'
        result = self.yelp.get_business_reviews(biz_id)

        mock_request.assert_called_once_with(
            'GET',
            f'{self.yelp.config.api_host}{quote(f"/v3/businesses/{biz_id}/reviews".encode("utf8"))}',
            headers={'Authorization': f'Bearer {self.yelp.config.api_key}'},
            params={'limit': 10}
        )
        self.assertEqual(result, mock_response)




