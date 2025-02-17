#!/usr/bin/python3
import unittest
from api.v1.app import app
from flask import jsonify

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status_route(self):
        """Test the /status route"""
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

if __name__ == '__main__':
    unittest.main()