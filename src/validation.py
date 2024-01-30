from datetime import datetime


def validate_cart_keys(cart_keys:dict) -> bool:
	keys_to_check = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
	for key in keys_to_check:
		if key not in cart_keys:
			return False
	return True


def validate_cart_field_types(cart) -> bool:
	validations = [
		isinstance(cart['cart_value'], int),
		isinstance(cart['delivery_distance'], int),
		isinstance(cart['number_of_items'], int),
		isinstance(cart['time'], str)
	]
	return all(validations)


def validate_cart_content_negative(cart:dict) -> bool:
	validations = [
		cart['cart_value'] >= 0,
		cart['delivery_distance'] >= 0,
		cart['time'] is not None
	]
	return all(validations)


def validate_cart_items(cart:dict) -> bool:
	if cart['number_of_items'] < 1:
		return False
	return True


def validate_cart_time(time:str) -> bool:
	try:
		valid_date = datetime.fromisoformat(time)
		return True
	except:
		return False


def validate_cart_details(cart_details:dict) -> dict:
	if not cart_details:
		return {"error": "Missing input, please provide the required fields!"}
	if not validate_cart_keys(cart_details):
		return {'error': 'Invalid input, field(s) missing!'}
	if not validate_cart_field_types(cart_details):
		return {'error': 'Invalid input, wrong field-type(s)!'}
	if not validate_cart_content_negative(cart_details):
		return {'error': 'Invalid input, negative/NULL value detected!'}
	if not validate_cart_items(cart_details):
		return {'error': 'Invalid input, minimum of 1 \'number_of_items\' required!'}
	if not validate_cart_time(cart_details['time']):
		return {'error': 'Invalid input, \'time\' must be in ISO-format!'}
	return None
