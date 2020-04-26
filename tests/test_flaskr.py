import os
import tempfile

import pytest
import sys
sys.path.append('../bachelor_kitchen')
from bachelor_kitchen import app


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
