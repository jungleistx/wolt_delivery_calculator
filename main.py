import json

FREE_DELIVERY_LIMIT = 20000
MAX_DELIVERY_FEE = 1500
DELIVERY_FEE_RUSH_MULTIPLIER = 1.2

def get_delivery_fee(cart_details:json) -> json:
	delivery_fee = 0

	return {"delivery_fee": delivery_fee}
