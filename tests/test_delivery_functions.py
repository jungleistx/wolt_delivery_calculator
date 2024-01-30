from src.const import *
from src.fees import *


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
	assert calculate_delivery_distance(6500) == 1300


def test_free_delivery(client):
	assert check_free_delivery(FREE_DELIVERY_LIMIT) == True
	assert check_free_delivery(FREE_DELIVERY_LIMIT - 100) == False
	assert check_free_delivery(45000) == True
	assert check_free_delivery(200) == False
	assert check_free_delivery(0) == False
