from flask import Flask, render_template
import requests

from dao.add_new_fields_to_docs import add_weight_and_price_per_kg
from routes.collections_routes import collections_bp
from routes.map_routes import map_bp
from routes.products_routes import products_bp
from routes.scraping_routes import scraping_bp
from routes.user_choice_routes import user_choice_bp
from routes.users_routes import users_bp
from routes.utils_routes import utils_bp

from classification.test_local import classificator_test


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("start_page.html")


# Регистрируем Blueprint
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(map_bp)
app.register_blueprint(collections_bp)
app.register_blueprint(utils_bp)
app.register_blueprint(scraping_bp)
app.register_blueprint(user_choice_bp)


@app.route('/test-ml')
def test_ml():

    return classificator_test("Francuski makaronsi 24 kom 288g Chateau")


@app.route('/test-add-fields')
def test_add_fields():
    counter = add_weight_and_price_per_kg()
    return str(counter)


# это то в каком виде должен присылаться выбор пользователя
@app.route('/test-request')
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
