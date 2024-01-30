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

