# from src.fees import *
# from src.const import *
import json


DEFAULT_DATA = {
	"cart_value": 1100,
	"delivery_distance": 900,
	"number_of_items": 1,
	"time": "2024-01-15T13:00:00Z"
}


def test_wrong_field(client):
	data = DEFAULT_DATA.copy()
	del data['cart_value']
	data['price'] = 450

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_missing_field(client):
	data = DEFAULT_DATA.copy()
	del data['cart_value']

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_wrong_field_type(client):
	data = DEFAULT_DATA.copy()
	data['cart_value'] = "150"

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_negative_value(client):
	data = DEFAULT_DATA.copy()
	data['cart_value'] = -15

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result
