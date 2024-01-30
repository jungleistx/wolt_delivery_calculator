from app import app
from src.fees import *
from src.const import *
import pytest, json


@pytest.fixture
def client():
	with app.test_client() as client:
		yield client
