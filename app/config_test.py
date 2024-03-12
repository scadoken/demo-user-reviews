import unittest
from app.config import YelpConfig
from unittest.mock import patch


class TestYelpConfig(unittest.TestCase):
    @patch('os.getenv')
    def test_get_yelp_config(self, mock_getenv):
        client_id = 'client_id'
        api_key = 'api_key'
        mock_getenv.side_effect = [client_id, api_key]

        expected_config = [
            client_id,
            api_key,
            'https://api.yelp.com',
            {'Authorization': f'Bearer {api_key}'},
        ]

        config = YelpConfig()

        actual_config = [
            config.client_id,
            config.api_key,
            config.api_host,
            config.headers,
        ]

        self.assertEqual(actual_config, expected_config)

