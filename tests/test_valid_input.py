from src.const import *
import json


DEFAULT_DATA = {
	"cart_value": 1100,
	"delivery_distance": 900,
	"number_of_items": 1,
	"time": "2024-01-15T13:00:00Z"
}


def test_default_values(client):
	response = client.post('/', json=DEFAULT_DATA)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 200


def test_example_values(client):
	data = DEFAULT_DATA.copy()
	data.update({"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 710


def test_free_delivery(client):
	data = DEFAULT_DATA.copy()
	data.update({"cart_value": FREE_DELIVERY_LIMIT + 250})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 0


def test_multiple_items(client):
	data = DEFAULT_DATA.copy()
	data.update({"number_of_items": 8})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 400


def test_bulk_items(client):
	data = DEFAULT_DATA.copy()
	data.update({"number_of_items": 15})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 870


def test_rushhour(client):
	data = DEFAULT_DATA.copy()
	data.update({"time": "2024-01-19T16:00:00Z"})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 240


def test_min_delivery_distance(client):
	data = DEFAULT_DATA.copy()
	data.update({"delivery_distance": 0})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 200


def test_bigger_delivery_distance(client):
	data = DEFAULT_DATA.copy()
	data.update({"delivery_distance": 2600})
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 600
