import os

from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['productsDB']


def insert_to_db(collection_name, counter, product, sub_category, min_group):
    item = {
        "_id": counter,
        "product": {
            'name': product.name.strip(),
            'price': product.price.strip().split('\xa0')
        },
        "subcategory": sub_category.strip(),
        "group": min_group.strip()
    }
    collection_name.insert_one(item)


def get_product_by_id():
    pass


def delete_product_by_id():
    pass


def get_product_by_title():
    pass


def delete_product_by_title():
    pass


def get_products_by_subcategory():
    pass


def get_products_by_group():
    pass


def get_the_cheapest_product():
    pass


def get_top_5():
    pass
