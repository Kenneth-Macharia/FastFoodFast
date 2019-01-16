''' This module contains the test code for the endpoints code in views.py '''

from flask import json
from app.tests.api_v1.test_config import test_client


def test_testapp(test_client):
    '''Tests the GET '/' test endpoint '''

    test_response = test_client.get('/')
    assert 'Hello world' in json.loads(test_response.data)['data']
