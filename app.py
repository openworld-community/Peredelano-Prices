from flask import Flask
from bs4 import BeautifulSoup
import requests
from scraping import Franca
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "enter your credentials"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['productsDB']

@app.route('/')
def hello_world():  # put application's code here

    dbname = get_database()
    collection_name = dbname["fromFranca"]

    # testItem = {
    #     "_id" : "999",
    #     "item_name" : "test_name"
    # }
    # collection_name.insert_one(testItem)

    toRet = Franca.scraping("https://glovoapp.com/me/sr/podgorica/franca-supermarket/", collection_name)
    return "Hello world! Counter = " + str(toRet)


if __name__ == '__main__':
    app.run(debug=True)
