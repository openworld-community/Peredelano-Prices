from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import requests
from scraping import Franca, Voli, Aroma
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv:// * enter your credentials * @formvppricesclaster.2yittu7.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['productsDB']

@app.route('/')
def hello_world():  # put application's code here

    dbname = get_database()
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]
    collection_name_Aroma = dbname["fromAroma"]

    toRetVoli = Voli.scraping("https://glovoapp.com/me/sr/podgorica/voli1/", collection_name_Voli)
    toRetFranca = Franca.scraping("https://glovoapp.com/me/sr/podgorica/franca-supermarket/", collection_name_Franca)
    toRetAroma = Aroma.scraping("https://glovoapp.com/me/sr/podgorica/aroma-cetinjska-pdg/", collection_name_Aroma)
    return "Hello world! CounterVoli = " + str(toRetVoli) \
        + " CounterFranca = " + str(toRetFranca) \
        + " CounterAroma = " + str(toRetAroma)
    #return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
