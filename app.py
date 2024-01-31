from src import usage
from src.fees import calculate_delivery_fee
from src.validation import validate_cart_details
from flask import Flask, jsonify, request
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
	app.run(port=8000)
