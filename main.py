import validation, fees, usage
from const import *
import json
from flask import Flask, jsonify, request
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def frontpage_get():
	return usage.wrong_method()


@app.route('/', methods=['POST'])
def calculate_delivery_fee():
	cart_details = request.json
	if not validation.validate_cart_details(cart_details):
		return usage.invalid_input()

	delivery_fee = 0
	if fees.check_free_delivery(cart_details['cart_value']):
		return jsonify({"delivery_fee": delivery_fee})

	delivery_fee += fees.calculate_delivery_surcharge(cart_details['cart_value'])
	delivery_fee += fees.calculate_delivery_distance(cart_details['delivery_distance'])
	delivery_fee += fees.calculate_delivery_items(cart_details['number_of_items'])

	if validation.is_rushhour(cart_details['time']):
		delivery_fee *= DELIVERY_FEE_RUSH_MULTIPLIER

	if delivery_fee > MAX_DELIVERY_FEE:
		delivery_fee = MAX_DELIVERY_FEE

	return jsonify({'delivery_fee': delivery_fee})




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
