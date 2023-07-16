import os

from bson import ObjectId
from pymongo import MongoClient
from dao.CRUD import *
from utils.calculations import *
from utils.get_weight import *


Aroma_col = get_collection_name("fromAroma")
Franca_col = get_collection_name("fromFranca")
Voli_col = get_collection_name("fromVoli")

# fromGlovo_with_complete_information
Glovo_w_c_i = get_collection_name("GlovoWCI")


def update_or_add_some_fields(collection_name, doc_id, *args):
    counter = 0
    for field_name, value in args:
        collection_name.update_one(
            {"_id": doc_id},
            {'$set': {field_name: value}}
        )
        counter += 1
    return counter


def add_weight_and_price_per_kg():
    cursorA = Aroma_col.find()
    cursorF = Franca_col.find()
    cursorV = Voli_col.find()

    check_count = 0

    for document in cursorA:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        price = document["product"]["price"]

        weight = add_weight_field(product_name)

        price_per_kg = add_price_per_kg_field(price[0], weight)

        mod_count = update_or_add_some_fields(Aroma_col, product_id,
                                              ["weight", weight], ["price_per_kg", price_per_kg])
        check_count += mod_count

    for document in cursorF:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        price = document["product"]["price"]

        weight = add_weight_field(product_name)

        price_per_kg = add_price_per_kg_field(price[0], weight)

        mod_count = update_or_add_some_fields(Franca_col, product_id,
                                              ["weight", weight], ["price_per_kg", price_per_kg])
        check_count += mod_count

    for document in cursorV:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        price = document["product"]["price"]

        weight = add_weight_field(product_name)

        price_per_kg = add_price_per_kg_field(price[0], weight)

        mod_count = update_or_add_some_fields(Voli_col, product_id,
                                              ["weight", weight], ["price_per_kg", price_per_kg])
        check_count += mod_count

    return check_count


def add_weight_field(product_str):
    field_value = find_weight(product_str)
    if field_value:
        return field_value
    else:
        return "not_found"


def add_price_per_kg_field(price, weight):
    if not weight or weight == "not_found":
        return "not_found"
    else:
        field_value = price_per_kg(price, weight)
    if field_value:
        return field_value
    else:
        return "not_found"


def add_custom_group_field_manual_ver(group):
    field_value = "field_value"

    if field_value:
        return field_value
    else:
        return "not_found"


# def add_market_field():
#     field_value = "field_value"
#     return field_value


#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #

# ML algorithm required
def add_custom_group_field_ml_ver(product_str):

    # need to find
    field_value = "field_value"

    #
    # magic
    #

    return field_value

#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
