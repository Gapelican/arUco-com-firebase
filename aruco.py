import cv2
from cv2 import aruco
import numpy as np
from skimage import io
import os
import re
from firebase import *


# CARREGANDO IMAGENS LOCAL E COLOCANDO O ID COMO CHAVE DE CADA IMAGEM
def loadAugImagesLocal(path):
    myList = os.listdir(path)
    augDics = {}
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0])
        imgAug = cv2.imread(f'{path}/{imgPath}')
        augDics[key] = imgAug

    return augDics

# CARREGANDO IMAGENS DO STORAGE E COLOCANDO O ID COMO CHAVE DE CADA IMAGEM
def loadAugImages(listImg):
    print(f'Total {len(listImg)}')
    augDics = {}
    for idImg, values in listImg.items():
      key = values['id']
      urlsSemTratamento = values["url"]
      urls = re.search("(?P<url>https?://[^\s]+)", urlsSemTratamento).group("url")
      imgAug = io.imread(urls)
      imgAug = cv2.cvtColor(imgAug, cv2.COLOR_RGB2BGR)
      augDics[key] = imgAug

    return augDics

def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}') #dicionario 6x6
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]

def arucoAug(bbox, id, img, imgAug, drawId=True):
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    h, w, c = imgAug.shape

    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0,0], [w,0], [w,h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1],img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0,0,0))
    imgOut = img + imgOut

    if drawId:
        n1 = tl[0]
        n2 = tl[1]
        org = (int(n1),int(n2))
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        colorFont = (255,0,0)
        thickness = 2
        cv2.putText(imgOut, str(id), org, font, fontScale, colorFont, thickness, cv2.LINE_AA)
    return imgOut

def main():
    cap = cv2.VideoCapture(0)
    augDics = loadAugImages(getDatabase())
    #augDics = loadAugImagesLocal("imgs") imagens locais
    
    while True:
 
        sccuess, img = cap.read()
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        arucofound = findArucoMarkers(img)

        if len(arucofound[0]) != 0:
            for bbox, id in zip(arucofound[0], arucofound[1]):
                if int(id) in augDics.keys():
                    img = arucoAug(bbox, id, img, augDics[int(id)]) 

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
  main()