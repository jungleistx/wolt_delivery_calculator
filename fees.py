from const import *


def check_free_delivery(cart_value:int) -> bool:
	if cart_value >= FREE_DELIVERY_LIMIT:
		return True
	return False


def calculate_delivery_items(items:int) -> int:
	delivery_items_fee = 0

	if items > ITEM_LIMIT:
		delivery_items_fee = (items - ITEM_LIMIT) * EXTRA_ITEM_SURCHARGE
		if items > BULK_ITEM_LIMIT:
			delivery_items_fee += EXTRA_ITEMS_BULK_FEE

	return delivery_items_fee


def calculate_delivery_distance(distance:int) -> int:
	delivery_distance_fee = BASE_DELIVERY_FEE
	additional_delivery_fee = 100

	while distance > 1000:
		delivery_distance_fee += additional_delivery_fee
		distance -= 500
	return delivery_distance_fee


def calculate_delivery_surcharge(cart_value:int) -> int:
	if cart_value < MINIMUM_CART_VALUE:
		return MINIMUM_CART_VALUE - cart_value
	return 0
