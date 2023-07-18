from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import requests

from dao.CRUD import get_database_users
from dao.add_new_fields_to_docs import add_weight_and_price_per_kg
from entities.UserClass import User

from routes.collections_routes import collections_bp
from routes.map_routes import map_bp
from routes.products_routes import products_bp
from routes.scraping_routes import scraping_bp
from routes.user_choice_routes import user_choice_bp
from routes.users_routes import users_bp
from routes.utils_routes import utils_bp

# from classification.test_local import classificator_test


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


# @app.route('/test-ml')
# def test_ml():
#
#     return classificator_test("Francuski makaronsi 24 kom 288g Chateau")


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    dbname = get_database_users()
    collection_name = dbname["users"]

    user_data = collection_name.find_one({'_id': user_id})
    if user_data:
        return User(user_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    dbname = get_database_users()
    collection_name = dbname["users"]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = collection_name.find_one({'username': username})
        if existing_user:
            return 'This user already exists!'

        new_user = {'username': username, 'password': password}
        user_id = collection_name.insert_one(new_user).inserted_id

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    dbname = get_database_users()
    collection_name = dbname["users"]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = collection_name.find_one({'username': username})
        if user_data and user_data['password'] == password:
            user = User(user_data)
            login_user(user)
            return redirect(url_for('dashboard'))

        return 'The username or password you entered is incorrect!'

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hi, {current_user.username}! Welcome to your personal area!'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
