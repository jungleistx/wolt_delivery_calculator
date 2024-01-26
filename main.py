import json

FREE_DELIVERY_LIMIT = 20000
MAX_DELIVERY_FEE = 1500
DELIVERY_FEE_RUSH_MULTIPLIER = 1.2


def main():
	get_delivery_fee()


def get_delivery_fee(cart_details:json) -> json:
	delivery_fee = 0

	if check_free_delivery(cart_details['cart_value']):
		return {"delivery_fee": delivery_fee}

	delivery_fee += calculate_delivery_surcharge(cart_details['cart_value'])

	return {"delivery_fee": delivery_fee}


def check_free_delivery(cart_value:int) -> bool:
	if cart_value >= FREE_DELIVERY_LIMIT:
		return True
	return False


def calculate_delivery_surcharge(cart_value:int) -> int:
	if cart_value < 1000:
		return 1000 - cart_value
	return 0

main()