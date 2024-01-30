
def validate_cart_content(cart:dict) -> bool:
	validations = [
		isinstance(cart['cart_value'], int) and cart['cart_value'] >= 0,
		isinstance(cart['delivery_distance'], int) and cart['delivery_distance'] >= 0,
		isinstance(cart['number_of_items'], int) and cart['number_of_items'] >= 0,
		isinstance(cart['time'], str) and cart['time'] is not None,
	]
	return all(validations)


def validate_cart_keys(cart_keys:dict) -> bool:
	keys_to_check = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
	for key in keys_to_check:
		if key not in cart_keys:
			return False
	return True


def validate_cart_field_types(cart):
	validations = [
		isinstance(cart['cart_value'], int),
		isinstance(cart['delivery_distance'], int),
		isinstance(cart['number_of_items'], int),
		isinstance(cart['time'], str)
	]
	return all(validations)


def validate_cart_details(cart_details:dict) -> bool:
	if not cart_details:
		return {"error": "Missing input, please provide the required fields!"}
	if not validate_cart_keys(cart_details):
		return {'error': 'Invalid input, field(s) missing!'}
	if not validate_cart_field_types(cart_details):
		return {'error': 'Invalid input, wrong field-type(s)!'}
	return None
