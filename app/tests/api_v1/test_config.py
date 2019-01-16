''' This module contains test configuration setup '''
import pytest
from instance import create_app

@pytest.fixture
def test_client():
    ''' The test client that will simulate the app behaviour to test '''
    app = create_app('testing')
    return app.test_client()
    