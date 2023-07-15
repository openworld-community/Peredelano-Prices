from flask import Blueprint, jsonify

from dao.CRUD import *

# Создаем Blueprint, чтобы определить маршруты
products_bp = Blueprint('products_routes', __name__)


@products_bp.route('/add-doc/<coll_name>/<name>/<price>/<group>/<market>')
def add_doc(coll_name, name, price, group, market):
    collection_name = get_collection_name(coll_name)
    item = add_document(collection_name, name, price, group, market)
    return jsonify(item)


@products_bp.route('/get-by-id/<coll_name>/<product_id>')
def get_by_id(coll_name, product_id):
    item = get_product_by_id(coll_name, product_id)
    return jsonify(item)


@products_bp.route('/get-by-name/<coll_name>/<product_name>')
def get_by_name(coll_name, product_name):
    item = get_product_by_title(coll_name, product_name)
    return jsonify(item)


@products_bp.route('/del-by-id/<coll_name>/<product_id>')
def del_by_id(coll_name, product_id):
    return delete_product_by_id(coll_name, product_id)


@products_bp.route('/del-by-name/<coll_name>/<product_name>')
def del_by_name(coll_name, product_id):
    return delete_product_by_title(coll_name, product_id)


@products_bp.route('/get-by-subcat/<coll_name>/<category>')
def get_docs_by_category(coll_name, category):
    docs_list = get_products_by_category(coll_name, category)
    return jsonify(results=docs_list)


@products_bp.route('/get-by-subcat/<coll_name>/<sub_cat>')
def get_docs_by_subcat(coll_name, sub_cat):
    docs_list = get_products_by_subcategory(coll_name, sub_cat)
    return jsonify(results=docs_list)


@products_bp.route('/get-by-group/<coll_name>/<group>')
def get_docs_by_group(coll_name, group):
    docs_list = get_products_by_group(coll_name, group)
    return jsonify(results=docs_list)


@products_bp.route('/get-by-group/<coll_name>/<market>')
def get_docs_by_market(coll_name, market):
    docs_list = get_products_by_market(coll_name, market)
    return jsonify(results=docs_list)
