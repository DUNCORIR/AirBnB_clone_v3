#!/usr/bin/python3
import unittest
from api.v1.app import app

class TestIndex(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = app.test_client()  # Flask test client to simulate requests
        self.app.testing = True

    def test_status_route(self):
        """Test the /status route"""
        response = self.app.get('/api/v1/status')  # Send a GET request to /status
        self.assertEqual(response.status_code, 200)  # Check if the status code is 200 OK
        self.assertEqual(response.json, {"status": "OK"})  # Check if the response matches the expected JSON

if __name__ == '__main__':
    unittest.main()