from flask import Blueprint

from dao.CRUD import *
from dao.add_new_fields_to_docs import add_more_information

# Создаем Blueprint, чтобы определить маршруты
collections_bp = Blueprint('collections_routes', __name__)


@collections_bp.route('/add-collection/<title>')
def add_collection(title):
    collection_name = get_collection_name(title)
    return str(collection_name)


@collections_bp.route('/add-more-information')
def test_add_fields():
    counter = add_more_information()
    return str(counter)


@collections_bp.route('/drop-collection/<title>')
def delete_collection(title):
    return drop_collection(title)


@collections_bp.route('/drop-all')
def drop_all():
    dbname = get_database()
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]
    collection_name_Aroma = dbname["fromAroma"]

    collection_name_Franca.drop()
    collection_name_Voli.drop()
    collection_name_Aroma.drop()
    return "Dropped all collections"
