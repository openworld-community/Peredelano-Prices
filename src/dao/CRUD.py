import os

from bson import ObjectId
from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['productsDB']


def get_database_users():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['userDB']


def insert_to_db_from_scraping(collection_name, counter, product, sub_category, min_group):
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


# потом еще как нибудь добавим срок годности
def add_document(collection_name, title, price, group, market):
    item = {
        "name": title,
        "price": price,
        "group": group,
        "market": market
    }
    collection_name.insert_one(item)
    return item


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
    query = {'product.name': name}
    document = collection_name.find_one(query)
    return document


def delete_product_by_title(coll_name, name):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'product.name': name}
    collection_name.delete_one(query)
    return "deleted"


def get_products_by_category(coll_name, category):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'category': category}
    documents = collection_name.find(query)
    documents_list = list(documents)
    return documents_list


def get_products_by_subcategory(coll_name, subcategory):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'subcategory': subcategory}
    documents = collection_name.find(query)
    documents_list = list(documents)
    return documents_list


def get_products_by_group(coll_name, group):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'group': group}
    documents = collection_name.find(query)
    documents_list = list(documents)
    return documents_list


def get_products_by_market(coll_name, market):
    dbname = get_database()
    collection_name = dbname[coll_name]
    query = {'market': market}
    documents = collection_name.find(query)
    documents_list = list(documents)
    return documents_list


def get_the_cheapest_product_in_group():
    pass


def get_top_5_in_group():
    pass
