from flask import jsonify


def wrong_method():
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


def invalid_input():
	return jsonify({"delivery_fee": "Invalid input!"})
