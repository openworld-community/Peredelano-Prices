from pymongo import MongoClient
import os


def get_database_users():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['usersDB']


dbname = get_database_users()
collection_name = dbname["users"]


def add_user(name, password):#, role, subscription_level):
    item = {
        "user": {
            'name': name,
            'password': password
        },
        'role': "user",
        'subscription_level': "subscription_level_1",
        'info': {
            'history_of_orders': ["empty", "empty"],
            'top_products': ["empty", "empty"],
            'monthly_budget': "",
            'special_preferences': ["empty", "empty"]
        }
        #to promote in china add:
        #'social_rating': social_rating
        #'is_uyghur': is_uyghur
    }
    collection_name.insert_one(item)
    return "item"


def get_user_by_name(name):
    query = {'user.name': name}
    document = collection_name.find_one(query)
    return document


def update_acc(username, updated_element, new_value):
    str_updated_el = str(updated_element)
    update = {
        "$set": {
            str_updated_el: new_value
        }
    }
    # Выполните обновление документа
    collection_name.update_one({"user.name": username}, update)
    collection_name.find()
    return get_user_by_name(username)
