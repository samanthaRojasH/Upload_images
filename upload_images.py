# importaciones
# para la codificación y decodificación de las imágenes
import base64
# para conectarnos a MongoDB
#from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ConnectionFailure
# para controlar la carga de multimedia
import gridfs
# para leer bytes
from io import BytesIO
# para el manejo de conjuntos de números
import numpy as np
# para graficar resultados
import matplotlib.pyplot as plt
# para el manejo de imágenes
#import cv2
from PIL import Image

from flask import Flask
from flask_pymongo import pymongo
from app import app



app = Flask(__name__)
@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"
if __name__ == '__main__':
    app.run(port=8000)



CONNECTION_STRING = "mongodb+srv://bot:bot12345*-+@imagescluster.2kpes.mongodb.net/imagebot?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('imagebot')
user_collection = pymongo.collection.Collection(db, 'user_collection')


import db
#test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"
