from src.validation import *
from src.const import *


DEFAULT_DATA = {
	"cart_value": 1100,
	"delivery_distance": 900,
	"number_of_items": 1,
	"time": "2024-01-15T13:00:00Z"
}


def test_cart_keys(client):
	data = DEFAULT_DATA.copy()
	assert validate_cart_keys(data) == True

	del data['cart_value']
	assert validate_cart_keys(data) == False

	data['cart_value'] = 100
	assert validate_cart_keys(data) == True
	del data['delivery_distance']
	assert validate_cart_keys(data) == False

	data['delivery_distance'] = 50
	del data["number_of_items"]
	assert validate_cart_keys(data) == False

	data["number_of_items"] = 1
	del data["time"]
	assert validate_cart_keys(data) == False
	data["time"] = "2024-01-15T13:20:00Z"
	assert validate_cart_keys(data) == True


def test_cart_field_types(client):
	data = {"cart_value": 50, "delivery_distance": 100, "number_of_items": 1, "time": "2024-01-15T13:00:00Z"}
	assert validate_cart_field_types(data) == True

	data["cart_value"] = ""
	assert validate_cart_field_types(data) == False

	data["cart_value"] = 50
	assert validate_cart_field_types(data) == True

	data["delivery_distance"] = ""
	assert validate_cart_field_types(data) == False

	data["delivery_distance"] = 100
	data["time"] = 50
	assert validate_cart_field_types(data) == False
