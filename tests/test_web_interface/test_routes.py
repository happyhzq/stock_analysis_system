# tests/test_web_interface/test_routes.py
from unittest.mock import patch
from flask_testing import TestCase
from web_interface.app import create_app

class TestDataRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app
    
    @patch('data_processor.data_loader.DataLoader')
    def test_data_upload(self, mock_loader):
        response = self.client.post('/api/upload', json={
            'source': 'edgar',
            'symbol': 'AAPL'
        })
        self.assertEqual(response.status_code, 201)