import cv2
import numpy as np
import random
import randomcolor

def extraiPele(img):
  #Transforma a imagem original em matrizes nos canais BGR
  B = img[:, :, 0]
  G = img[:, :, 1]
  R = img[:, :, 2]

  #Define a altura e a largura da imagem de entrada
  largura = img.shape[1]
  altura = img.shape[0]

  #Define uma matriz com zeros com as dimensões da imagem original
  imgPeleExtraida = np.zeros((altura,largura,3), np.uint8)

  #Percorre os pixels das matrizes RGB
  for linha in range(0, largura):
    for coluna in range(0, altura):  
      #Verifica se o pixel representa um pixel de pele
      if (R[coluna, linha] > 120 and R[coluna, linha] < 255) and (G[coluna, linha] > 90 and G[coluna, linha] < 250) and (B[coluna, linha] > 70 and B[coluna, linha] < 218) and (R[coluna, linha] > G[coluna, linha]) and (G[coluna, linha] > B[coluna, linha]):
        imgPeleExtraida[coluna, linha] = [B[coluna, linha], G[coluna, linha], R[coluna, linha]]
      else:
        imgPeleExtraida[coluna, linha] = 255
  
  return imgPeleExtraida

def extraiBorda(img):
  #Utiliza a função de extração de bordas Canny
  edges = cv2.Canny(img,100,200)
  return edges

def busca_sequencial(seq, x):
  ''' (list, float) -> bool '''
  for i in range(len(seq)):
    if seq[i] == x:
      return True
    return False

def segmentaRegioes(img):
  #Define a altura e a largura da imagem de entrada
  largura = img.shape[1]
  altura = img.shape[0]

  seed_pt = None
  h, w = img.shape[:2]
  mask = np.zeros((h+2, w+2), np.uint8)

  listaCores = [0]
  for linha in range(0, largura):
    for coluna in range(0, altura):
      if img[coluna, linha, 0] != 255 and img[coluna, linha, 1] != 255 and img[coluna, linha, 2] != 255:
        randomCor = random_color()
        if not busca_sequencial(listaCores, randomCor):
          seed_pt = linha, coluna
          cv2.floodFill(img, mask, seed_pt, randomCor, (30,)*3, (30,)*3, cv2.FLOODFILL_FIXED_RANGE)
          listaCores.append(randomCor)
  
  return img

def random_color(): 
  levels = range(32,256,32) 
  return tuple(random.choice(levels) for _ in range(3))

def deteccaoRostoSimetria(img):
  

img = cv2.imread('naruto.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgExtracaoBordas = extraiBorda(gray)

imgPeleExtraida = extraiPele(img)
cv2.imshow("Imagem Pele sem Canny", segmentaRegioes(imgPeleExtraida))
cv2.waitKey(0)
