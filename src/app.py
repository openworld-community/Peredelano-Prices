from flask import Flask, render_template
from scraping import glovo_scraper
from utils import from_db_to_file
import folium
from folium.plugins import MousePosition
from utils.info import *
from dao.CRUD import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("start_page.html")


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
    return item


@app.route('/get-by-id/<coll_name>/<product_id>')
def get_by_id(coll_name, product_id):
    item = get_product_by_id(coll_name, product_id)
    name = item["name"]
    price = item["price"]
    group = item["group"]
    return str(name) + "\n" + str(price) + "\n" + str(group) + "\n"


@app.route('/get-by-name/<coll_name>/<product_name>')
def get_by_name(coll_name, product_name):
    item = get_product_by_title(coll_name, product_name)
    name = item["name"]
    price = item["price"]
    group = item["group"]
    return str(name) + "\n" + str(price) + "\n" + str(group) + "\n"


@app.route('/del-by-id/<coll_name>/<product_id>')
def del_by_id(coll_name, product_id):
    return delete_product_by_id(coll_name, product_id)


@app.route('/del-by-name/<coll_name>/<product_name>')
def del_by_name(coll_name, product_id):
    return delete_product_by_title(coll_name, product_id)


@app.route('/get-by-subcat/<coll_name>/<category>')
def get_docs_by_category(coll_name, category):
    docs = get_products_by_category(coll_name, category)
    count = 0
    for doc in docs:
        count += 1
    return str(count)


@app.route('/get-by-subcat/<coll_name>/<sub_cat>')
def get_docs_by_subcat(coll_name, sub_cat):
    docs = get_products_by_subcategory(coll_name, sub_cat)
    count = 0
    for doc in docs:
        count += 1
    return str(count)


@app.route('/get-by-group/<coll_name>/<group>')
def get_docs_by_group(coll_name, group):
    docs = get_products_by_group(coll_name, group)
    count = 0
    for doc in docs:
        count += 1
    return str(count)


@app.route('/get-by-group/<coll_name>/<market>')
def get_docs_by_market(coll_name, market):
    docs = get_products_by_market(coll_name, market)
    count = 0
    for doc in docs:
        count += 1
    return str(count)


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
