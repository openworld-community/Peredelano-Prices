import gridfs
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import json

from dao.CRUD import get_database, get_collection_name
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
        product_data = {
            "product_name": product_name
        }
        return jsonify(product_data)

    docF = coll_name_Franca.find_one({"_id": int(product_id)})
    if docF:
        product_name = docF['product']['name']
        product_data = {
            "product_name": product_name
        }
        return jsonify(product_data)

    docV = coll_name_Voli.find_one({"_id": int(product_id)})
    if docV:
        product_name = docV['product']['name']
        product_data = {
            "product_name": product_name
        }
        return jsonify(product_data)


@app.route('/get_arr_of_id/<what_we_need>')
def get_the_id_we_need(what_we_need):

    if what_we_need == "first_ten_fromAroma":
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        data = {
            "arr": arr
        }
        return jsonify(data)

    if what_we_need == "first_ten_fromFranca":
        arr = [344, 345, 346, 347, 348, 349, 350, 351, 352, 353]
        data = {
            "arr": arr
        }
        return jsonify(data)

    if what_we_need == "first_ten_fromVoli":
        arr = [566, 567, 568, 569, 570, 571, 572, 573, 574, 575]
        data = {
            "arr": arr
        }
        return jsonify(data)


@app.route('/get_products_combined_data', methods=['GET'])
def get_combined_data():
    try:
        # # cursorA = (get_collection_name("fromAroma")).find()
        # cursorF = (get_collection_name("fromFranca")).find()
        # # cursorV = (get_collection_name("fromVoli")).find()
        #
        # # хотим достать первые 10 штук с 344 по 353
        # test_counter = 1
        # products_data_container = []
        # for document in cursorF:
        #     if test_counter <= 10:
        #         product_id = document["_id"]
        #         product_name = document["product"]["name"]
        #         image_name = "img_name_" + str(product_id) + ".jpg"
        #         image_data = fs.find_one({'filename': image_name}).read()
        #         product_data = {
        #             "product_name": product_name,
        #             "product_image": image_data
        #         }
        #         products_data_container.append(product_data)
        #
        # return jsonify(products_data_container)

        franca_coll = get_collection_name("fromFranca")
        query = {'_id': 344}
        doc = franca_coll.find_one(query)
        product_name = doc['product']['name']
        image_name = "img_name_" + str(344) + ".jpg"
        image_data = fs.find_one({'filename': image_name}).read()
        resp = Response(image_data, content_type='image/jpeg')
        product_data = {
            "product_name": product_name,
            "product_image": resp
        }
        return jsonify(product_data)

    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Internal Server Error'}), 500


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
