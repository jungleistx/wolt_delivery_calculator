from src.const import *
from src.fees import *
from test_valid_input import DEFAULT_DATA

def test_surcharge(client):
	assert calculate_delivery_surcharge(MINIMUM_CART_VALUE) == 0
	assert calculate_delivery_surcharge(MINIMUM_CART_VALUE - 250) == 250
	assert calculate_delivery_surcharge(MINIMUM_CART_VALUE + 250) == 0
	assert calculate_delivery_surcharge(2550) == 0
	assert calculate_delivery_surcharge(25500) == 0
	assert calculate_delivery_surcharge(700) == 300
	assert calculate_delivery_surcharge(300) == 700
	assert calculate_delivery_surcharge(0) == MINIMUM_CART_VALUE


def test_delivery_distance(client):
	assert calculate_delivery_distance(0) == 200
	assert calculate_delivery_distance(500) == 200
	assert calculate_delivery_distance(1000) == 200
	assert calculate_delivery_distance(1001) == 300
	assert calculate_delivery_distance(1499) == 300
	assert calculate_delivery_distance(1500) == 300
	assert calculate_delivery_distance(1501) == 400
	assert calculate_delivery_distance(2100) == 500
	assert calculate_delivery_distance(6500) == 1300


def test_free_delivery(client):
	assert check_free_delivery(FREE_DELIVERY_LIMIT) == True
	assert check_free_delivery(FREE_DELIVERY_LIMIT - 100) == False
	assert check_free_delivery(45000) == True
	assert check_free_delivery(200) == False
	assert check_free_delivery(0) == False


def test_delivery_items(client):
	assert calculate_delivery_items(ITEM_LIMIT - 1) == 0
	assert calculate_delivery_items(ITEM_LIMIT + 1) == EXTRA_ITEM_SURCHARGE
	assert calculate_delivery_items(ITEM_LIMIT + 6) == EXTRA_ITEM_SURCHARGE * 6
	assert calculate_delivery_items(2) == 0
	assert calculate_delivery_items(5) == 50
	assert calculate_delivery_items(10) == 300
	assert calculate_delivery_items(BULK_ITEM_LIMIT + 1) == (BULK_ITEM_LIMIT + 1 - ITEM_LIMIT) * EXTRA_ITEM_SURCHARGE + EXTRA_ITEMS_BULK_FEE
	assert calculate_delivery_items(15) == 670
	assert calculate_delivery_items(25) == 1170


def test_rushhour(client):
	assert is_rushhour("2024-01-15T13:00:00Z") == False
	assert is_rushhour("2024-01-15T16:00:00Z") == False
	assert is_rushhour("2024-01-19T13:00:00Z") == False
	assert is_rushhour("2024-01-19T15:00:00Z") == True
	assert is_rushhour("2024-01-19T18:59:00Z") == True
	assert is_rushhour("2024-01-15T08:00:00-05:00") == False
	assert is_rushhour("2024-01-15T11:00:00-05:00") == False
	assert is_rushhour("2024-01-19T08:00:00-05:00") == False
	assert is_rushhour("2024-01-19T11:00:00-05:00") == True
	assert is_rushhour("2024-01-19T13:59:00-05:00") == True


def test_delivery_fee(client):
	data = DEFAULT_DATA.copy()
	assert calculate_delivery_fee(data) == 200

	data['cart_value'] = 800
	assert calculate_delivery_fee(data) == 400

	data['delivery_distance'] = 1200
	assert calculate_delivery_fee(data) == 500

	data['time'] = "2024-01-19T15:00:00Z"
	assert calculate_delivery_fee(data) == 600

	data['cart_value'] = FREE_DELIVERY_LIMIT + 100
	assert calculate_delivery_fee(data) == 0

	data = {'cart_value': 40, 'delivery_distance': 6500, 'number_of_items': 25, 'time': "2024-01-19T15:00:00Z"}
	assert calculate_delivery_fee(data) == 1500

	data = {'cart_value': 0, 'delivery_distance': 0, 'number_of_items': 1, 'time': "2024-01-19T13:00:00Z"}
	assert calculate_delivery_fee(data) == 1200
