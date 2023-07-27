from flask import Blueprint

from dao.CRUD import *
from scraping import glovo_scraper
from scraping.test_scrap_6 import scraping_6

# Создаем Blueprint, чтобы определить маршруты
scraping_bp = Blueprint('scraping_routes', __name__)


@scraping_bp.route('/scrap-6')
def scrap_6():
    urls_6_markets = {
        'Aroma':
            "https://glovoapp.com/me/en/podgorica/aroma-cetinjska-pdg/",
        'Franca':
            "https://glovoapp.com/me/en/podgorica/franca-supermarket/",
        'Voli':
            "https://glovoapp.com/me/en/podgorica/voli1/",
        'IDEA':
            "https://glovoapp.com/me/en/podgorica/idea-podgorica/",
        'C_market':
            "https://glovoapp.com/me/en/podgorica/c-market/",
        'City_Market':
            "https://glovoapp.com/me/en/podgorica/city-marketpdg/"
    }
    markets_6 = [
        'Aroma', 'Franca', 'Voli',
        'IDEA', 'C_market', 'City_Market'
    ]
    return scraping_6(markets_6, urls_6_markets, 0)


@scraping_bp.route('/scraping')
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
