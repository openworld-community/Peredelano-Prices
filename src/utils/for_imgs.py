import gridfs
from pymongo import MongoClient
import os
import requests


def get_database_imgs():
    CONNECTION_STRING = os.getenv('MONGO_CONN_STR', "mongodb://user:pass@localhost/?retryWrites=true&w=majority")
    client = MongoClient(CONNECTION_STRING)

    return client['imgsDB']


dbname = get_database_imgs()
collection_name = dbname["test_imgs"]
fs = gridfs.GridFS(dbname)


# image_name = "img_name_" + str(counter) + ".jpg"
def download_image(image_url, image_name):
    response = requests.get(image_url)
    fs.put(response.content, filename=image_name)




