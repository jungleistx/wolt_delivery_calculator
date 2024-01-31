import json


DEFAULT_DATA = {
	'cart_value': 1100,
	'delivery_distance': 900,
	'number_of_items': 1,
	'time': '2024-01-15T13:00:00Z'
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
	data['cart_value'] = '150'

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


def test_zero_items(client):
	data = DEFAULT_DATA.copy()
	data['number_of_items'] = 0

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_wrong_method(client):
	response = client.get('/')

	assert response.status_code == 405


def test_invalid_time(client):
	data = DEFAULT_DATA.copy()
	data['time'] = '2024-01-35T13:00:00Z'

	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_empty_json(client):
	data = {}
	response = client.post('/', json=data)
	result = json.loads(response.data)

	assert response.status_code == 400
	assert 'error' in result


def test_wrong_content_type(client):
	data = DEFAULT_DATA.copy()
	headers = {'Content-Type': 'text/html'}

	response = client.post('/', json=data, headers=headers)
	result = json.loads(response.data)

	assert response.status_code == 415
	assert 'error' in result


def test_no_json(client):
	response = client.post('/')
	result = json.loads(response.data)

	assert response.status_code == 415
	assert 'error' in result
