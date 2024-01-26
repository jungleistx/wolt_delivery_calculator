import json
from flask import Flask, jsonify, request
from datetime import datetime

FREE_DELIVERY_LIMIT = 20000
MAX_DELIVERY_FEE = 1500
DELIVERY_FEE_RUSH_MULTIPLIER = 1.2
MINIMUM_CART_VALUE = 1000
BASE_DELIVERY_FEE = 200
EXTRA_ITEM_SURCHARGE = 50
EXTRA_ITEMS_BULK_FEE = 120
ITEM_LIMIT = 4
BULK_ITEM_LIMIT = 12
ISO_FRIDAY = 5

app = Flask(__name__)


@app.route('/')
def usage_wrong_method():
	return '''
<p>Calculate delivery fee:</p>
<table>
	<tr><td>METHOD</td> <td>POST</td></tr>
	<tr><td>content-type</td> <td>application/json</td></tr>
	<tr><td>\'cart_value\'</td> <td>integer</td></tr>
	<tr><td>\'delivery_distance\'</td> <td>integer</td></tr>
	<tr><td>\'number_of_items\'</td> <td>integer</td></tr>
	<tr><td>\'time\'</td> <td>string</td></tr>
</table>
'''


@app.route('/', methods=['POST'])
def calculate_delivery_fee():
	cart_details = request.json
	if not validate_cart_details(cart_details):
		return usage_invalid_input()

	delivery_fee = 0
	if check_free_delivery(cart_details['cart_value']):
		return jsonify({"delivery_fee": delivery_fee})

	delivery_fee += calculate_delivery_surcharge(cart_details['cart_value'])
	delivery_fee += calculate_delivery_distance(cart_details['delivery_distance'])
	delivery_fee += calculate_delivery_items(cart_details['number_of_items'])

	if is_rushhour(cart_details['time']):
		delivery_fee *= DELIVERY_FEE_RUSH_MULTIPLIER

	if delivery_fee > MAX_DELIVERY_FEE:
		delivery_fee = MAX_DELIVERY_FEE

	return jsonify({'delivery_fee': delivery_fee})


def is_rushhour(time:str) -> bool:
	delivery_date = datetime.fromisoformat(time)

	if delivery_date.isoweekday() == ISO_FRIDAY:
		if delivery_date.hour >= 15 and delivery_date.hour < 19:
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


def check_free_delivery(cart_value:int) -> bool:
	if cart_value >= FREE_DELIVERY_LIMIT:
		return True
	return False


def usage_invalid_input():
	return '''
Invalid input!
Make sure that you POST the following attributes:
	content-type: application/json
	\'cart_value\': integer
	\'delivery_distance\': integer
	\'number_of_items\': integer
	\'time\': string
'''


def validate_cart_keys(cart_keys:dict) -> bool:
	keys_to_check = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
	for key in keys_to_check:
		if key not in cart_keys:
			return False
	return True


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


def validate_cart_details(cart_details:dict) -> bool:
	if not cart_details:
		return False
	if not validate_cart_keys(cart_details):
		return False
	if not validate_cart_content(cart_details):
		return False
	return True


if __name__ == '__main__':
	app.run(port=8000, debug=True)


# normal 710
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}" "localhost:8000"

# normal 300
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": 7290, \"delivery_distance\": 200, \"number_of_items\": 6, \"time\": \"2024-01-15T13:00:00Z\"}" "localhost:8000"

# normal 1500
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": 19900, \"delivery_distance\": 6200, \"number_of_items\": 13, \"time\": \"2024-01-19T18:00:00Z\"}" "localhost:8000"

# normal 0
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": 20460, \"delivery_distance\": 200, \"number_of_items\": 6, \"time\": \"2024-01-15T13:00:00Z\"}" "localhost:8000"

# rush hour + normal 852.0
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-19T16:00:00Z\"}" "localhost:8000"

# negative value in cart_value
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": -1, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}" "localhost:8000"

# wrong type in cart_value (str)
# curl -X POST -H "Content-type: application/json" -d "{\"cart_value\": \"790\", \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}" "localhost:8000"
