from src import usage
from src.fees import calculate_delivery_fee
from src.validation import validate_cart_details
from flask import Flask, jsonify, request
from datetime import datetime
from werkzeug.exceptions import UnsupportedMediaType

app = Flask(__name__)


@app.route('/', methods=['GET'])
def frontpage_get():
	return usage.error_wrong_method(), 405


@app.route('/', methods=['POST'])
def frontpage_api():
	try:
		cart_details = request.json

		validation_error = validate_cart_details(cart_details)
		if validation_error:
			return jsonify(validation_error), 400

		delivery_fee = calculate_delivery_fee(cart_details)
		response_data = {'delivery_fee': delivery_fee}
		return jsonify(response_data), 200

	except UnsupportedMediaType as e:
		return jsonify({'error': str(e)}), 415

	except Exception as e:
		return jsonify({'error': str(e)}), 500


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
