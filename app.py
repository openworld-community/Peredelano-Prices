import re

from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import requests
from scraping import Franca, Voli, Aroma
from search import grouping, searching, creatingRegex
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re

app = Flask(__name__)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://@formvppricesclaster.2yittu7.mongodb.net/?retryWrites=true&w=majority"

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

    # //    //  //  //  //  //  //  //  //  //  //  //  //  //  //  //  //
    # here we have arr of lists for categories of product
    # for a start
    # milk, meat, fruit
    # (maybe meat should be replaced with bread,
    #   regular expressions quickly turn into hell)
    # there will be all the info that is needed
    # to give the user what he wants in a particular session

    # return render_template('index.html', content1=toRetStr1, content2=toRetStr2, content3=toRetStr3)

    #return render_template("index.html")


    return "New Test \n Counter Aroma: " + str(toRetAroma) +\
        " \n Counter Franca: " + str(toRetFranca) +\
        " \n Counter Voli: " + str(toRetVoli)


if __name__ == '__main__':
    app.run(debug=True)
