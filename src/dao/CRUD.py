import os

from bson import ObjectId
from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

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


def get_collection_name(title):
    dbname = get_database()
    collection_name = dbname[title]
    return collection_name


def add_document(collection_name, title, price, group):
    item = {
        "name": title,
        "price": price,
        "group": group
    }
    collection_name.insert_one(item)
    return "item"


def drop_collection(title):
    dbname = get_database()
    collection_name = dbname[title]
    collection_name.drop()
    return "deleted"


def get_product_by_id(coll_name, document_id):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'_id': ObjectId(document_id)}  # Преобразуем строку идентификатора в ObjectId
    document = collection_name.find_one(query)
    return document


def delete_product_by_id(coll_name, document_id):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'_id': ObjectId(document_id)}  # Преобразуем строку идентификатора в ObjectId
    collection_name.delete_one(query)
    return "deleted"


def get_product_by_title(coll_name, name):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'name': name}
    document = collection_name.find_one(query)
    return document


def delete_product_by_title(coll_name, name):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'name': name}
    collection_name.delete_one(query)
    return "deleted"


def get_products_by_subcategory():
    pass


def get_products_by_group():
    pass


def get_the_cheapest_product_in_group():
    pass


def get_top_5_in_group():
    pass
