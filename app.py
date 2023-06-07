from flask import Flask
from bs4 import BeautifulSoup
import requests
from scraping import Franca

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here

    toRet = Franca.scraping("https://glovoapp.com/me/sr/podgorica/franca-supermarket/")
    return "Hello world! Counter = " + str(toRet)


if __name__ == '__main__':
    app.run(debug=True)
