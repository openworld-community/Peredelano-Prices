import os

from flask import Flask
from scraping import glovo_scraper
from utils import from_db_to_file
from pymongo import MongoClient
import csv

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
    return "hello_world"


@app.route('/to-file')
def to_file():
    tree_of_categories = {
        'meat_category':
            {
                'pork':
                    {
                        'Aroma':
                            ["empty"],
                        'Franca':
                            ["Svinjsko meso"],
                        'Voli':
                            ["Svinjetina"]
                    },
                'beef':
                    {
                        'Aroma':
                            ["empty"],
                        'Franca':
                            ["Juneće meso"],
                        'Voli':
                            ["Junetina"]
                    },
                'chicken':
                    {
                        'Aroma':
                            ["empty"],
                        'Franca':
                            ["Pileće meso"],
                        'Voli':
                            ["Piletina", "Piletina smrznuto", "Ćuretina smrznuto"]
                    },
                'veal':
                    {
                        'Aroma':
                            ["empty"],
                        'Franca':
                            ["Teleće meso"],
                        'Voli':
                            ["Teletina"]
                    },
                'semi-finished products':
                    {
                        'Aroma':
                            ["Suhomesnato slajs", "Mini salame, kobasice i virsle", "Pršut,čajna,budimska,suvi vrat,kulen"],
                        'Franca':
                            ["Delikates, mesne prerađevine"],
                        'Voli':
                            ["Roštilj"]
                    }
            },
        'milk_category':
            {
                'milk':
                    {
                        'Aroma':
                            ["Dugotrajno mlijeko", "Svjeze mlijeko"],
                        'Franca':
                            ["Mlijeko uht", "Mlijeko uht mala pakovanja", "Mlijeko svježe pasterizovano"],
                        'Voli':
                            ["Mlijeko"]
                    },
                'cheese':
                    {
                        'hard cheese':
                            {
                                'Aroma':
                                    ["Tvrdi i polutvrdi sirevi"],
                                'Franca':
                                    ["empty"],
                                'Voli':
                                    ["Edamer , gauda emental", "Ostali delikatesni sirevi", "Koziji sir & ovčiji sir"]
                            },
                        'melted cheese':
                            {
                                'Aroma':
                                    ["Namazni i topljeni sirevi"],
                                'Franca':
                                    ["empty"],
                                'Voli':
                                    ["Tost & topljeni sirevi"]
                            }
                    },
                'jogurt':
                    {
                        'Aroma':
                            ["Jogurt", "Voćni jogurt"],
                        'Franca':
                            ["Jogurt", "Jogurt voćni"],
                        'Voli':
                            ["Jogurt kefir i slično"]
                    },
                'maslac':
                    {
                        'Aroma':
                            ["Maslac"],
                        'Franca':
                            ["Maslac"],
                        'Voli':
                            ["Maslac & margarin"]
                    }
            },
        'pekara_category':
            {
                'bread':
                    {
                        'Aroma':
                            ["Hljeb dnevni"],
                        'Franca':
                            ["empty"],
                        'Voli':
                            ["Hljeb"]
                    },
                'toast and packaged bread':
                    {
                        'Aroma':
                            ["Pakovani hljeb", "Dvopek"],
                        'Franca':
                            ["Hljeb pakovani"],
                        'Voli':
                            ["Tost & dvopek hljeb"]
                    },
                'cakes and pastries':
                    {
                        'Aroma':
                            ["Gotove torte I kolaci"],
                        'Franca':
                            ["Kolači industrijski suhi", "Kolači sveži pakovani", "Kolači sveži suhi"],
                        'Voli':
                            ["Gotove torte i kolači"]
                    }
            },
        'fr_veg_nut_category':
            {
                'fruits':
                    {
                        'Aroma':
                            ["Svježe voće"],
                        'Franca':
                            ["Voće"],
                        'Voli':
                            ["Voće"]
                    },
                'vegetables':
                    {
                        'Aroma':
                            ["Svježe povrće"],
                        'Franca':
                            ["Povrće"],
                        'Voli':
                            ["Povrće"]
                    },
                'dried fruits':
                    {
                        'Aroma':
                            ["Rinfuzno suvo grozdje", "Rinfuzno voće"],
                        'Franca':
                            ["empty"],
                        'Voli':
                            ["Dehidrirano voće"]
                    },
                'nuts':
                    {
                        'Aroma':
                            ["Rinfuzni pistaci", "Rinfuzni badem", "Rinfuzni ljesnik", "Rinfuzni kikiriki", "Rinfuzni orah"],
                        'Franca':
                            ["empty"],
                        'Voli':
                            ["Orašasti plodovi & sjemenke"]
                    }
            }
    }

    list_of_group_Aroma = [
        "Suhomesnato slajs", "Mini salame, kobasice i virsle",
        "Pršut,čajna,budimska,suvi vrat,kulen",
        "Dugotrajno mlijeko", "Svjeze mlijeko",
        "Tvrdi i polutvrdi sirevi", "Namazni i topljeni sirevi",
        "Jogurt", "Voćni jogurt", "Maslac", "Hljeb dnevni",
        "Pakovani hljeb", "Dvopek", "Gotove torte I kolaci",
        "Svježe voće", "Svježe povrće", "Rinfuzno suvo grozdje",
        "Rinfuzno voće", "Rinfuzni pistaci", "Rinfuzni badem",
        "Rinfuzni ljesnik", "Rinfuzni kikiriki", "Rinfuzni orah"
    ]
    list_of_group_Franca = [
        "Svinjsko meso", "Juneće meso", "Pileće meso", "Teleće meso",
        "Delikates, mesne prerađevine", "Mlijeko uht",
        "Mlijeko uht mala pakovanja", "Mlijeko svježe pasterizovano",
        "Jogurt", "Jogurt voćni", "Maslac", "Hljeb pakovani",
        "Kolači industrijski suhi", "Kolači sveži pakovani",
        "Kolači sveži suhi", "Voće", "Povrće"
    ]
    list_of_group_Voli = [
        "Svinjetina", "Junetina", "Piletina", "Piletina smrznuto",
        "Ćuretina smrznuto", "Teletina", "Roštilj", "Mlijeko",
        "Edamer , gauda emental", "Ostali delikatesni sirevi",
        "Koziji sir & ovčiji sir", "Tost & topljeni sirevi",
        "Jogurt kefir i slično", "Maslac & margarin", "Hljeb",
        "Tost & dvopek hljeb", "Gotove torte i kolači", "Voće",
        "Povrće", "Dehidrirano voće", "Orašasti plodovi & sjemenke"
    ]

    dbname = get_database()

    # search from db

    counter = from_db_to_file.to_file(tree_of_categories, list_of_group_Aroma, list_of_group_Franca, list_of_group_Voli, dbname)




    # with open('data.csv', mode='w', newline='') as file:
    #     writer = csv.writer(file)  # Создаем объект writer
    #     for data in list_to_write:
    #         writer.writerow(data)


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
