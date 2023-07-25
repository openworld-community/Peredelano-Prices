import os

import gridfs
from bson import ObjectId
from pymongo import MongoClient

from utils.for_imgs import fs


def get_database():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['productsDB']


def get_database_glovo():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['glovoDB']


def insert_to_db_from_scraping(collection_name, counter, product):#, sub_category, min_group):
    item = {
        "_id": counter,
        "product": {
            'name': product.name.strip(),
            'price': product.price.strip().split('\xa0')
        },
        # "subcategory": sub_category.strip(),
        # "group": min_group.strip()
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


#   #   #   #   ##   #   #   #   ##   #   #   #   ##   #   #   #   #

# to do func for update
# to do date of price
# to do new db and collection, add field image_name

#   #   #   #   ##   #   #   #   ##   #   #   #   ##   #   #   #   #

# collection of all products with full info for prod
# some products haven't weight or img - f*ck them


glovodb = get_database_glovo()
final_collection = glovodb["prod_for_prod"]


def to_glovodb():
    productsDB = get_database()
    Aroma_coll = productsDB["fromAroma"]
    Franca_coll = productsDB["fromFranca"]
    Voli_coll = productsDB["fromVoli"]

    all_products = 0
    products_with_full_info = 0

    cursorA = Aroma_coll.find()
    for document in cursorA:

        all_products += 1

        product_name = document["product"]["name"]
        price_arr = document["product"]["price"]
        price = str(price_arr[0]) + str(price_arr[1])
        group = document["group"]
        market = "Aroma"

        product_id = document["_id"]
        weight = document["weight"]
        price_per_kg = document["price_per_kg"]
        image_name = "img_name_" + str(product_id) + ".jpg"

        if check_full_info_before_insert(image_name, weight, price_per_kg):
            # product_id, product_name, image_name, price, weight, price_per_kg, group, market
            insert_to_glovodb(product_id, product_name, image_name, price, weight, price_per_kg, group, market)
            products_with_full_info += 1


    cursorF = Franca_coll.find()
    for document in cursorF:

        all_products += 1

        product_name = document["product"]["name"]
        price_arr = document["product"]["price"]
        price = str(price_arr[0]) + str(price_arr[1])
        group = document["group"]
        market = "Franca"

        product_id = document["_id"]
        weight = document["weight"]
        price_per_kg = document["price_per_kg"]
        image_name = "img_name_" + str(product_id) + ".jpg"

        if check_full_info_before_insert(image_name, weight, price_per_kg):
            # product_id, product_name, image_name, price, weight, price_per_kg, group, market
            insert_to_glovodb(product_id, product_name, image_name, price, weight, price_per_kg, group, market)
            products_with_full_info += 1


    cursorV = Voli_coll.find()
    for document in cursorV:

        all_products += 1

        product_name = document["product"]["name"]
        price_arr = document["product"]["price"]
        price = str(price_arr[0]) + str(price_arr[1])
        group = document["group"]
        market = "Voli"

        product_id = document["_id"]
        weight = document["weight"]
        price_per_kg = document["price_per_kg"]
        image_name = "img_name_" + str(product_id) + ".jpg"

        if check_full_info_before_insert(image_name, weight, price_per_kg):
            # product_id, product_name, image_name, price, weight, price_per_kg, group, market
            insert_to_glovodb(product_id, product_name, image_name, price, weight, price_per_kg, group, market)
            products_with_full_info += 1

    return [all_products, products_with_full_info]


def insert_to_glovodb(product_id, product_name, image_name, price, weight, price_per_kg, group, market):
    item = {
        "product_id": product_id,
        "product_name": product_name,
        "image_name": image_name,
        "price": price,
        "weight": weight,
        "price_per_kg": price_per_kg,
        "group": group,
        "market": market
    }
    final_collection.insert_one(item)


def check_full_info_before_insert(image_name, weight, price_per_kg):
    is_full_info = False
    try:
        image_data = fs.find_one({'filename': image_name}).read()
        if image_data is not None:
            if weight != "not_found" and price_per_kg != "not_found":
                is_full_info = True
    except gridfs.errors.NoFile:
        is_full_info = False
    finally:
        return is_full_info
