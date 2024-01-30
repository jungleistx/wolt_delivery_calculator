from src.fees import *
from src.const import *
import pytest, json


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
	input = {
		"cart_value": 20005,
		"delivery_distance": 500,
		"number_of_items": 1,
		"time": "2024-01-15T13:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 0


def test_multiple_items(client):
	input = {
		"cart_value": 900,
		"delivery_distance": 500,
		"number_of_items": 7,
		"time": "2024-01-15T13:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 450


def test_bulk_items(client):
	input = {
		"cart_value": 900,
		"delivery_distance": 500,
		"number_of_items": 15,
		"time": "2024-01-15T13:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 970


def test_rushhour(client):
	input = {
		"cart_value": 920,
		"delivery_distance": 500,
		"number_of_items": 16,
		"time": "2024-01-19T17:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 1200


def test_min_delivery_distance(client):
	input = {
		"cart_value": 1750,
		"delivery_distance": 0,
		"number_of_items": 1,
		"time": "2024-01-18T17:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 200


def test_bigger_delivery_distance(client):
	input = {
		"cart_value": 1750,
		"delivery_distance": 2600,
		"number_of_items": 1,
		"time": "2024-01-18T17:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 600
