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
#import matplotlib.pyplot as plt
# para el manejo de imágenes
#import cv2
from PIL import Image

from flask import Flask, render_template, request
import dns
import db
app = Flask(__name__)
@app.route('/')
def flask_mongodb_atlas():    
    return render_template('index.html')

@app.route("/procesar", methods=['POST'])
def procesar():
    username = request.form.get("username")
    password = request.form.get("password")

    database = db.client["imageBot"]
    collection = database["imageBotCT"]

    usern = collection.find_one({"username":{"$in":[username]}})
    for i in usern:
        
        if usern[i] == password:
            passwordFind = usern[i]            
        elif usern[i] == username: 
            usernameFind = usern[i]
        else:
            usernameFind = ""
            passwordFind = ""
    
    db.client.close()

    if(usernameFind == username and passwordFind == password):
        return render_template("form.html", username=username)
    
    return render_template("AccessDenied.html")

@app.route("/procesarImg", methods=['POST'])
def procesarImg():

    if request.method == 'POST':  
        fileContentS = request.files['files'].read() 
        
    fileName = request.form.get("fileName")
    
    img = fileContentS

    fid = ""
    encoded_string = base64.b64encode(img)

    # Carga de la imagen
    filename = fileName
    database = db.db
    fs = gridfs.GridFS(database)
    fileid = fs.put(encoded_string, filename=filename)
    database.image.insert_one({"filename":filename,"fileid":fileid})

    # Consulta
    for item in database.image.find({"filename":filename}):
        print(item)
    fid = item["fileid"]
    if fid != "":
        output = fs.get(fid).read()
        print(output)

    # Construccion de la imagen
    file = fs.find_one({"filename":filename})
    bytedata = file.read()

    # Pillow
    ima_IO = BytesIO(base64.b64decode(bytedata))
    img_PIL = Image.open(ima_IO)
    img_PIL.show()

    db.client.close()
    
    return render_template("Upload.html")

#test to insert data to the data base
@app.route("/test")
def test():
    db.db.imageBotCT.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == '__main__':
    app.run(port=8000)