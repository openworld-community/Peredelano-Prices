from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import requests
import bcrypt

from dao.Users_db import get_database_users, add_user
from dao.add_new_fields_to_docs import add_weight_and_price_per_kg
from entities.UserClass import User
from utils.hash_check import hash_password, check_password

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
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    dbname = get_database_users()
    collection_name = dbname["users"]

    user_data = collection_name.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)

    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    dbname = get_database_users()
    collection_name = dbname["users"]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = collection_name.find_one({'user.name': username})
        if existing_user:
            return 'This user already exists!'

        hashed_password = hash_password(password)

        #   #   #   #   #   #   #   #

        add_user(username, hashed_password)

        #   #   #   #   #   #   #   #

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    dbname = get_database_users()
    collection_name = dbname["users"]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = collection_name.find_one({'user.name': username})
        if user_data and check_password(password, user_data['user']['password']):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('dashboard'))
            # return "all_ok"

        return 'The username or password you entered is incorrect!'

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # return "its your personal area"
    return f'Hi, {current_user.username}! Welcome to your personal area!'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin-page')
@login_required
def admin_page():
    if not current_user.is_admin():
        return f'Hi, {current_user.username}! \n go fuck yourself! ' \
               f'\n you are not admin \n you are {current_user.role}'
    return f'Hi, {current_user.username}! Welcome to your ADMIN page!'


@app.route('/user-page')
@login_required
def user_page():
    return 'Привет, user! Это ваша личная область.'


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
