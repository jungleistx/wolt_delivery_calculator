from src.const import *
from datetime import datetime


def is_rushhour(time:str) -> bool:
	delivery_date = datetime.fromisoformat(time)

	if delivery_date.isoweekday() == ISO_FRIDAY:
		if 15 <= delivery_date.hour < 19:
			return True
	return False


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


def calculate_delivery_fee(cart_details:dict) -> int:
	if check_free_delivery(cart_details['cart_value']):
		return 0

	delivery_fee = 0
	delivery_fee += calculate_delivery_surcharge(cart_details['cart_value'])
	delivery_fee += calculate_delivery_distance(cart_details['delivery_distance'])
	delivery_fee += calculate_delivery_items(cart_details['number_of_items'])

	if is_rushhour(cart_details['time']):
		delivery_fee *= DELIVERY_FEE_RUSH_MULTIPLIER

	if delivery_fee > MAX_DELIVERY_FEE:
		delivery_fee = MAX_DELIVERY_FEE

	return int(delivery_fee)
