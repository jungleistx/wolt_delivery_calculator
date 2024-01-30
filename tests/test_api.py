from app import app
import pytest, json

@pytest.fixture
def client():
	# Create a test client using the Flask app instance
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


def test_zero_items(client):
	input = {
		"cart_value": 0,
		"delivery_distance": 0,
		"number_of_items": 0,
		"time": "2024-01-15T13:00:00Z"
	}

	response = client.post('/', json=input)
	assert response.status_code == 200

	result = json.loads(response.data)
	assert 'delivery_fee' in result
	assert result['delivery_fee'] == 1200
