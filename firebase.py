from cv2 import imread
import pyrebase
# DOCUMENTAÇÃO https://github.com/thisbejim/Pyrebase#storage
import requests
import json
import os
from configFirebase import config


firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
auth = firebase.auth()

# UPLOAD STORAGE
def saveImg(path, img):
    storage.child(f'{path}/{img}').put(img)

# DOWNLOAD STORAGE
def downloadImg(path, img, nome):
    storage.child(f'{path}/{img}').download(filename=f'{nome}', path=os.path.basename(img))

# POST DATABASE
def postDatabase(dados):
    requisicao = requests.post(f'{link}/imagens/.json', data=json.dumps(dados))
    print(requisicao)

# GET DATABASE
def getDatabase():
    requisicao = requests.get(f'{link}/.json')
    dic_requisicao = requisicao.json()
    print(requisicao)
    listImg = dic_requisicao['imagens']
    return listImg


# NOME DA PASTA DA IMAGEM !!!!
path = "Gabriel"
link = "https://aruco-64098-default-rtdb.firebaseio.com/"
# PEGANDO URL DA IMAGEM STORAGE
url = storage.child("Gabriel/cebola.jpg").get_url(auth)
# DADOS PARA POST
dados = {'id':23, 'url':url}


