from flask import Flask, render_template, jsonify
import folium
from folium.plugins import MousePosition

from dao.Users_db import *
from scraping import glovo_scraper
from utils import from_db_to_file
from utils.get_weight import *
from utils.info import *
from dao.CRUD import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("start_page.html")


@app.route('/add-user/test')
def test_add_user():
    add_user("testname", "testpass", "slave", "1")
    doc = get_user_by_name("testname")
    return str(doc)


@app.route('/update-user/test')
def test_update_user_acc():
    list_to_show = list()
    list_to_show.append(str(get_user_by_name("testname")))
    updated_user = update_acc("testname", "subscription_level", "2")
    list_to_show.append(str(updated_user))
    if updated_user["subscription_level"] == "2":
        list_to_show.append(str(update_acc("testname", "role", "dungeon_master")))
    return jsonify(results=list_to_show)


@app.route('/weight-to-file')
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


@app.route('/tree-of-category')
def get_tree_of_category():
    return tree_of_categories


@app.route('/coords-of-markets/<market>')
def get_coords_of_markets(market):
    to_ret = None
    match market:
        case "Aroma":
            to_ret = coords_of_Aroma_markets
        case "Franca":
            to_ret = coords_of_Franca_markets
        case "Voli":
            to_ret = coords_of_Voli_markets

    return to_ret


@app.route('/add-collection/<title>')
def add_collection(title):
    collection_name = get_collection_name(title)
    return str(collection_name)


@app.route('/drop-collection/<title>')
def delete_collection(title):
    return drop_collection(title)


@app.route('/add-doc/<coll_name>/<name>/<price>/<group>/<market>')
def add_doc(coll_name, name, price, group, market):
    collection_name = get_collection_name(coll_name)
    item = add_document(collection_name, name, price, group, market)
    return jsonify(item)


@app.route('/get-by-id/<coll_name>/<product_id>')
def get_by_id(coll_name, product_id):
    item = get_product_by_id(coll_name, product_id)
    return jsonify(item)


@app.route('/get-by-name/<coll_name>/<product_name>')
def get_by_name(coll_name, product_name):
    item = get_product_by_title(coll_name, product_name)
    return jsonify(item)


@app.route('/del-by-id/<coll_name>/<product_id>')
def del_by_id(coll_name, product_id):
    return delete_product_by_id(coll_name, product_id)


@app.route('/del-by-name/<coll_name>/<product_name>')
def del_by_name(coll_name, product_id):
    return delete_product_by_title(coll_name, product_id)


@app.route('/get-by-subcat/<coll_name>/<category>')
def get_docs_by_category(coll_name, category):
    docs_list = get_products_by_category(coll_name, category)
    return jsonify(results=docs_list)


@app.route('/get-by-subcat/<coll_name>/<sub_cat>')
def get_docs_by_subcat(coll_name, sub_cat):
    docs_list = get_products_by_subcategory(coll_name, sub_cat)
    return jsonify(results=docs_list)


@app.route('/get-by-group/<coll_name>/<group>')
def get_docs_by_group(coll_name, group):
    docs_list = get_products_by_group(coll_name, group)
    return jsonify(results=docs_list)


@app.route('/get-by-group/<coll_name>/<market>')
def get_docs_by_market(coll_name, market):
    docs_list = get_products_by_market(coll_name, market)
    return jsonify(results=docs_list)


@app.route('/map')
def open_map():

    map = folium.Map(location=[42.44510285, 19.258387751564968], zoom_start=14)

    for coords in coords_of_Aroma_markets:
        folium.Marker(location=coords, popup="Aroma", icon=folium.Icon(color='orange')).add_to(map)

    for coords in coords_of_Franca_markets:
        folium.Marker(location=coords, popup="Franca", icon=folium.Icon(color='red')).add_to(map)

    for coords in coords_of_Voli_markets:
        folium.Marker(location=coords, popup="Voli", icon=folium.Icon(color='green')).add_to(map)

    map.add_child(folium.ClickForLatLng())
    map.add_child(folium.LatLngPopup())
    map.add_child(folium.ClickForMarker())

    MousePosition().add_to(map)

    map.save("templates/Podgorica_map.html")

    return render_template("Podgorica_map.html")


@app.route('/to-file')
def to_file():

    dbname = get_database()

    counter = from_db_to_file.to_file(tree_of_categories, list_of_group_Aroma, list_of_group_Franca, list_of_group_Voli, dbname)

    return str(counter)


@app.route('/scraping')
def scraping():
    categories_to_scrap_all = {
        'Aroma':
            ["Mesne prerađevine", "Mlijeko, mliječni proizvodi i jaja", "Voće i povrće", "Hljeb, peciva i kolači"],
        'Franca':
            ["Meso i živina", "Mliječni proizvodi ", "Voće i povrće ", "Pekarski proizvodi"],
        'Voli':
            ["Mesara i ribara", "Mliječni proizvodi i jaja", "Voće i povrće", "Pekara"]
    }

    urls_markets_glovo = {
        'Aroma':
            "https://glovoapp.com/me/sr/podgorica/aroma-cetinjska-pdg/",
        'Franca':
            "https://glovoapp.com/me/sr/podgorica/franca-supermarket/",
        'Voli':
            "https://glovoapp.com/me/sr/podgorica/voli1/"
    }

    dbname = get_database()
    collection_name_Aroma = dbname["fromAroma"]
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]

    collections_names_glovo = {
        'Aroma':
            collection_name_Aroma,
        'Franca':
            collection_name_Franca,
        'Voli':
            collection_name_Voli
    }

    markets = [
        'Aroma', 'Franca', 'Voli'
    ]

    result_glovo = glovo_scraper.scraping(
        markets,
        urls_markets_glovo,
        collections_names_glovo,
        categories_to_scrap_all
    )

    return str(result_glovo)


@app.route('/drop-all')
def drop_all():
    dbname = get_database()
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]
    collection_name_Aroma = dbname["fromAroma"]

    collection_name_Franca.drop()
    collection_name_Voli.drop()
    collection_name_Aroma.drop()
    return "Dropped all collections"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
