from flask import Blueprint

from dao.CRUD import *
from utils import from_db_to_file
from utils.get_weight import *
from utils.info import *

# Создаем Blueprint, чтобы определить маршруты
utils_bp = Blueprint('utils_routes', __name__)


@utils_bp.route('/weight-to-file')
def weight_to_file():
    write_weight_to_file()

    list_to_return = list()

    try:
        with open("weight_check.txt", 'r') as file:
            for temp_str in file:
                list_to_return.append(temp_str)

        return list_to_return
    except FileNotFoundError:
        return "Файл weight_check.txt не найден, 404"


@utils_bp.route('/tree-of-category')
def get_tree_of_category():
    return tree_of_categories


@utils_bp.route('/to-file')
def to_file():
    dbname = get_database()

    counter = from_db_to_file.to_file(tree_of_categories, list_of_group_Aroma, list_of_group_Franca, list_of_group_Voli,
                                      dbname)

    return str(counter)
