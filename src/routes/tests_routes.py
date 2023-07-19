import requests
from flask import url_for, render_template, redirect, request, Blueprint, jsonify
import json


tests_bp = Blueprint('test_routes', __name__)


@tests_bp.route("/test-api-data")
def testt():
    return render_template("for_tests.html")


@tests_bp.route("/api/data", methods=['GET', 'POST'])
def test_api_data():
    if request.method == 'POST':
        data_from_frontend = request.get_json()
        with open("test_front.json", "w") as file:
            json.dump(data_from_frontend, file, ensure_ascii=False, indent=4)

        return jsonify(data_from_frontend)
    if request.method == 'GET':
        data = {
            "message": "hello from backend!",
            "data": [1, 2, 3, 4, 5]
        }
        return jsonify(data)


@tests_bp.route('/test-request')
def test_request():
    url = 'http://127.0.0.1:5000/user_choice'
    data = [1, 2, 3, 4, 5]

    response = requests.post(url, json=data)
    # Если вы используете форм-данные, замените строку выше на:
    # response = requests.post(url, data={'array': data})

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return response.text
