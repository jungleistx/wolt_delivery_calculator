from const import *
from datetime import datetime

def validate_cart_content(cart:dict) -> bool:
	if not isinstance(cart['cart_value'], int) or cart['cart_value'] < 0:
		return False
	if not isinstance(cart['delivery_distance'], int) or cart['delivery_distance'] < 0:
		return False
	if not isinstance(cart['number_of_items'], int) or cart['number_of_items'] < 0:
		return False
	if not isinstance(cart['time'], str) or cart['time'] is None:
		return False
	return True


def validate_cart_keys(cart_keys:dict) -> bool:
	keys_to_check = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
	for key in keys_to_check:
		if key not in cart_keys:
			return False
	return True


def validate_cart_details(cart_details:dict) -> bool:
	if not cart_details:
		return False
	if not validate_cart_keys(cart_details):
		return False
	if not validate_cart_content(cart_details):
		return False
	return True


def is_rushhour(time:str) -> bool:
	delivery_date = datetime.fromisoformat(time)

	if delivery_date.isoweekday() == ISO_FRIDAY:
		if delivery_date.hour >= 15 and delivery_date.hour < 19:
			return True
	return False
