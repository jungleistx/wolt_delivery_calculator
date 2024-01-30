from src.validation import *
from src.const import *


DEFAULT_DATA = {
	"cart_value": 1100,
	"delivery_distance": 900,
	"number_of_items": 1,
	"time": "2024-01-15T13:00:00Z"
}



def test_cart_keys(client):
	data = {"cart_value": 0, "delivery_distance": 0, "number_of_items": 1, "time": "2024-01-15T13:00:00Z"}
	assert validate_cart_keys(data) == True

	del data['cart_value']
	assert validate_cart_keys(data) == False

	data['cart_value'] = 1
	assert validate_cart_keys(data) == True
	del data['delivery_distance']
	assert validate_cart_keys(data) == False

	data['delivery_distance'] = 1
	del data["number_of_items"]
	assert validate_cart_keys(data) == False

	data["number_of_items"] = 1
	del data["time"]
	assert validate_cart_keys(data) == False
	data["time"] = "2024-01-15T13:20:00Z"
	assert validate_cart_keys(data) == True
