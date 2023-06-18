import os
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
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")

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

    # toRetVoli = Voli.scraping("https://glovoapp.com/me/sr/podgorica/voli1/", collection_name_Voli)
    # toRetFranca = Franca.scraping("https://glovoapp.com/me/sr/podgorica/franca-supermarket/", collection_name_Franca)
    # toRetAroma = Aroma.scraping("https://glovoapp.com/me/sr/podgorica/aroma-cetinjska-pdg/", collection_name_Aroma)

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


    # return "New Test \n Counter Aroma: " + str(toRetAroma) +\
    #     " \n Counter Franca: " + str(toRetFranca) +\
    #     " \n Counter Voli: " + str(toRetVoli)

    return "HelloWorld"


@app.route('/get_list/<milk>')
def display_milk(milk):

    milk = "milk"

    # all milk from all shops
    toDisplay = list()
    milkFromAroma = list()
    milkFromFranca = list()
    milkFromVoli = list()
    toDisplay = [
        [milkFromAroma, "Aroma"],
        [milkFromFranca, "Franca"],
        [milkFromVoli, "Voli"]
    ]

    regex = creatingRegex.matching(str(milk))

    dbname = get_database()
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]
    collection_name_Aroma = dbname["fromAroma"]

    milkCategoryFromAroma = collection_name_Aroma.find({'category': "milkCategory"})
    milkCategoryFromFranca = collection_name_Franca.find({'category': "milkCategory"})
    milkCategoryFromVoli = collection_name_Voli.find({'category': "milkCategory"})



    for document in milkCategoryFromAroma:
        product_array = document['product']
        title = ""
        price = ""
        allOk = False

        if "mlijeko" in str(product_array[0]) :
            title = product_array[0]
            price = product_array[1]
            allOk = True
        else:
            if "Mlijeko" in str(product_array[0]) :
                title = product_array[0]
                price = product_array[1]
                allOk = True

        if(allOk):
            temp = [
                {'title': title},
                {'price': price},
                {'shop': toDisplay[0][1]}
            ]
            milkFromAroma.append(temp)


    for document in milkCategoryFromFranca:
        product_array = document['product']
        title = ""
        price = ""
        allOk = False

        if "mlijeko" in str(product_array[0]):
            title = product_array[0]
            price = product_array[1]
            allOk = True
        else:
            if "Mlijeko" in str(product_array[0]):
                title = product_array[0]
                price = product_array[1]
                allOk = True

        if (allOk):
            temp = [
                {'title': title},
                {'price': price},
                {'shop': toDisplay[1][1]}
            ]
            milkFromFranca.append(temp)


    for document in milkCategoryFromVoli:
        product_array = document['product']
        title = ""
        price = ""
        allOk = False

        if "mlijeko" in str(product_array[0]):
            title = product_array[0]
            price = product_array[1]
            allOk = True
        else:
            if "Mlijeko" in str(product_array[0]):
                title = product_array[0]
                price = product_array[1]
                allOk = True

        if (allOk):
            temp = [
                {'title': title},
                {'price': price},
                {'shop': toDisplay[2][1]}
            ]
            milkFromVoli.append(temp)


    return jsonify(toDisplay)



        # for document in milkCategoryFromAroma:
    #
    #     productInfo = document['product']
    #     productTitle = productInfo[0]
    #     productPrice = productInfo[1]
    #
    #     temp = [
    #         {'title': productTitle},
    #         {'price': productPrice},
    #         {'shop': toDisplay[0][1]}
    #     ]
    #     toDisplay[0][0].append(temp)
    #
    # for document in milkCategoryFromFranca:
    #     productInfo = document['product']
    #     productTitle = productInfo[0]
    #     productPrice = productInfo[1]
    #
    #     temp = [
    #         {'title': productTitle},
    #         {'price': productPrice},
    #         {'shop': toDisplay[1][1]}
    #     ]
    #     toDisplay[1][0].append(temp)
    #
    # for document in milkCategoryFromVoli:
    #     productInfo = document['product']
    #     productTitle = productInfo[0]
    #     productPrice = productInfo[1]
    #
    #     temp = [
    #         {'title': productTitle},
    #         {'price': productPrice},
    #         {'shop': toDisplay[2][1]}
    #     ]
    #     toDisplay[2][0].append(temp)

    #return jsonify(toDisplay)


if __name__ == '__main__':
    app.run(debug=True)
