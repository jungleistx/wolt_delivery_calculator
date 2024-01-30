from app import app
import pytest, json


@pytest.fixture
def client():
	with app.test_client() as client:
		yield client


def test_example_input(client):
	input = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2024-01-15T13:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 710


def test_one_item(client):
	input = {
		"cart_value": 900,
		"delivery_distance": 500,
		"number_of_items": 1,
		"time": "2024-01-15T13:00:00Z"
	}
	response = client.post('/', json=input)
	result = json.loads(response.data)

	assert response.status_code == 200
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 300


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
