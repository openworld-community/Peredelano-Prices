import gridfs
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import json

from dao.CRUD import get_database, get_collection_name, get_products_by_group
from dao.Users_db import get_database_users, add_user
from entities.UserClass import User
from utils.hash_check import hash_password, check_password
from utils.for_imgs import *

from routes.collections_routes import collections_bp
from routes.map_routes import map_bp
from routes.products_routes import products_bp
from routes.scraping_routes import scraping_bp
from routes.user_choice_routes import user_choice_bp
from routes.users_routes import users_bp
from routes.utils_routes import utils_bp
from routes.tests_routes import tests_bp


app = Flask(__name__)

login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager.login_view = 'login'

# Регистрируем Blueprint
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(map_bp)
app.register_blueprint(collections_bp)
app.register_blueprint(utils_bp)
app.register_blueprint(scraping_bp)
app.register_blueprint(user_choice_bp)
app.register_blueprint(tests_bp)


#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #

# image_name = "img_name_" + str(counter) + ".jpg"
@app.route("/test-products-container")
def test_products_container():

    return render_template('test-products-container.html')


@app.route('/get_image/<image_id>')
def get_image(image_id):
    try:
        image_name = "img_name_" + str(image_id) + ".jpg"
        image_data = fs.find_one({'filename': image_name}).read()
        return Response(image_data, content_type='image/jpeg')
    except gridfs.errors.NoFile:
        return "Image not found.", 404


@app.route('/get_product_data/<product_id>')
def get_product_data(product_id):
    coll_name_Aroma = get_collection_name("fromAroma")
    coll_name_Franca = get_collection_name("fromFranca")
    coll_name_Voli = get_collection_name("fromVoli")

    docA = coll_name_Aroma.find_one({"_id": int(product_id)})
    if docA:
        product_name = docA['product']['name']
        product_price = docA['product']['price']
        price_per_kg = docA['price_per_kg']
        price_per_kg = str(price_per_kg) + " " + str(product_price[1]) + "/kg"
        product_data = {
            "product_name": product_name,
            "price_per_kg": price_per_kg,
            "market": "Aroma"
        }
        return jsonify(product_data)

    docF = coll_name_Franca.find_one({"_id": int(product_id)})
    if docF:
        product_name = docF['product']['name']
        product_price = docF['product']['price']
        price_per_kg = docF['price_per_kg']
        price_per_kg = str(price_per_kg) + " " + str(product_price[1]) + "/kg"
        product_data = {
            "product_name": product_name,
            "price_per_kg": price_per_kg,
            "market": "Franca"
        }
        return jsonify(product_data)

    docV = coll_name_Voli.find_one({"_id": int(product_id)})
    if docV:
        product_name = docV['product']['name']
        product_price = docV['product']['price']
        price_per_kg = docV['price_per_kg']
        price_per_kg = str(price_per_kg) + " " + str(product_price[1]) + "/kg"
        product_data = {
            "product_name": product_name,
            "price_per_kg": price_per_kg,
            "market": "Voli"
        }
        return jsonify(product_data)


@app.route('/get_arr_of_id/<what_we_need>')
def get_the_id_we_need(what_we_need):
    arr = []
    if what_we_need == "cheese":
        group_to_find1 = "hard cheese"
        A_list1 = get_products_by_group("fromAroma", group_to_find1)
        F_list1 = get_products_by_group("fromFranca", group_to_find1)
        V_list1 = get_products_by_group("fromVoli", group_to_find1)

        for doc in A_list1:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        for doc in F_list1:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        for doc in V_list1:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        group_to_find2 = "melted cheese"
        A_list2 = get_products_by_group("fromAroma", group_to_find2)
        F_list2 = get_products_by_group("fromFranca", group_to_find2)
        V_list2 = get_products_by_group("fromVoli", group_to_find2)

        for doc in A_list2:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        for doc in F_list2:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        for doc in V_list2:
            current_id = doc["_id"]
            if doc['weight'] != "not_found":
                arr.append(current_id)

        data = {
            "arr": arr
        }
        return jsonify(data)


    group_to_find = what_we_need
    A_list = get_products_by_group("fromAroma", group_to_find)
    F_list = get_products_by_group("fromFranca", group_to_find)
    V_list = get_products_by_group("fromVoli", group_to_find)

    for doc in A_list:
        current_id = doc["_id"]
        if doc['weight'] != "not_found":
            arr.append(current_id)

    for doc in F_list:
        current_id = doc["_id"]
        if doc['weight'] != "not_found":
            arr.append(current_id)

    for doc in V_list:
        current_id = doc["_id"]
        if doc['weight'] != "not_found":
            arr.append(current_id)

    data = {
        "arr": arr
    }
    return jsonify(data)


@app.route('/get_titles/<what_we_need>')
def get_titles_of_category_and_subcategory(what_we_need):
    match what_we_need:
        case "categories":
            arr = ["meat", "dairy", "bakery", "fruits and vegetables"]
            data = {
                "arr": arr
            }
            return jsonify(data)

        case "meat":
            arr = ["pork", "beef", "chicken", "veal", "semi-finished products"]
            data = {
                "arr": arr
            }
            return jsonify(data)

        case "dairy":
            arr = ["milk", "cheese", "jogurt", "maslac"]
            data = {
                "arr": arr
            }
            return jsonify(data)

        case "bakery":
            arr = ["bread", "toast and packaged bread", "cakes and pastries"]
            data = {
                "arr": arr
            }
            return jsonify(data)

        case "fruits and vegetables":
            arr = ["fruits", "vegetables", "dried fruits", "nuts"]
            data = {
                "arr": arr
            }
            return jsonify(data)





#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #


@app.route('/login', methods=['GET', 'POST'])
def login():
    dbname = get_database_users()
    collection_name = dbname["users"]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = collection_name.find_one({'user.name': username})
        role = user_data['role']
        if user_data and check_password(password, user_data['user']['password']):
            user = User(user_data)
            login_user(user)
            if role == 'admin':
                return redirect(url_for('admin_page'))
            if role == 'user':
                return redirect(url_for('user_page'))

        return 'The username or password you entered is incorrect!'

    return render_template('login.html')


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


@login_manager.user_loader
def load_user(user_id):
    dbname = get_database_users()
    collection_name = dbname["users"]

    user_data = collection_name.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)

    return None


@app.route('/admin-page')
@login_required
def admin_page():
    return render_template('admin_page.html')


@app.route('/info-for-admin', methods=['GET', 'POST'])
@login_required
def info_for_admin():
    dbname = get_database_users()
    collection_name = dbname["users"]
    if request.method == 'GET':
        user_data = collection_name.find_one({'user.name': current_user.username})
        name = user_data['user']['name']
        role = user_data['role']
        subscription_level = user_data['subscription_level']
        data = {
            "username": name,
            "role": role,
            "subscription_level": subscription_level
        }
        return jsonify(data)
    else:
        data = {
            "message": "your methods not get"
        }
        return jsonify(data)


@app.route('/user-page')
@login_required
def user_page():
    return render_template('user_page.html')


@app.route('/info-for-user', methods=['GET', 'POST'])
@login_required
def info_for_user():
    dbname = get_database_users()
    collection_name = dbname["users"]
    if request.method == 'GET':
        user_data = collection_name.find_one({'user.name': current_user.username})
        name = user_data['user']['name']
        role = user_data['role']
        subscription_level = user_data['subscription_level']
        data = {
            "username": name,
            "role": role,
            "subscription_level": subscription_level
        }
        return jsonify(data)
    else:
        data = {
            "message": "your methods not get"
        }
        return jsonify(data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #


@app.route('/')
def hello_world():
    return render_template("start_page.html")


#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
