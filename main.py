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
	delivery_fee += calculate_delivery_distance(cart_details['delivery_distance'])
	delivery_fee += calculate_delivery_items(cart_details['number_of_items'])

	return {"delivery_fee": delivery_fee}


def check_free_delivery(cart_value:int) -> bool:
	if cart_value >= FREE_DELIVERY_LIMIT:
		return True
	return False


def calculate_delivery_surcharge(cart_value:int) -> int:
	if cart_value < 1000:
		return 1000 - cart_value
	return 0


def calculate_delivery_distance(distance:int) -> int:
	delivery_distance_fee = 100 # minimum fee is 1e

	distance -= 500
	while distance >= 0:
		delivery_distance_fee += 100
		distance -= 500

	return delivery_distance_fee


def calculate_delivery_items(items:int) -> int:
	delivery_fee = 0

	if items >= 5:
		delivery_fee = (items - 4) * 50

		if items >= 12:
			delivery_fee += 120

	return delivery_fee


main()