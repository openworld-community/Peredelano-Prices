import os
import re

from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import requests
from scraping import Franca, voli_scraper, Aroma, glovo_scraper
from search import grouping, searching, creatingRegex
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re

app = Flask(__name__)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['productsDB']


@app.route('/')
def hello_world():  # put application's code here

    categories_to_scrap_all = {
        'Aroma':
            ["Mesne prerađevine", "Mlijeko, mliječni proizvodi i jaja", "Voće i povrće", "Hljeb, peciva i kolači"],
        'Franca':
            ["Meso i živina", "Mliječni proizvodi ", "Voće i povrće ", "Pekarski proizvodi"],
        'Voli':
            ["Mesara", "Mliječni proizvodi i jaja", "Voće", "Pekara"]
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


    # dbname = get_database()
    # collection_name_Franca = dbname["fromFranca"]
    # collection_name_Voli = dbname["fromVoli"]
    # collection_name_Aroma = dbname["fromAroma"]

    # toRetVoli = voli_scraper.scraping("https://glovoapp.com/me/sr/podgorica/voli1/", collection_name_Voli)
    # toRetFranca = Franca.scraping("https://glovoapp.com/me/sr/podgorica/franca-supermarket/", collection_name_Franca)
    # toRetAroma = Aroma.scraping("https://glovoapp.com/me/sr/podgorica/aroma-cetinjska-pdg/", collection_name_Aroma)

    return str(result_glovo)


@app.route('/drop-all/')
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
