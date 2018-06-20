"""
******* Reconhecimento de faces em imagens de animes *******
Autora: Karine Pires
"""
import cv2
import numpy as np
import random
import randomcolor
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

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

def kmeansImagemRGB(img):
  # load the image and convert it from BGR to RGB so that
  # we can dispaly it with matplotlib
  image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
  # show our image
  plt.figure()
  plt.axis("off")
  plt.imshow(image)

  arrayImage = np.reshape(image, (image.shape[0] * image.shape[1], 3))

  # reshape the image to be a list of pixels
  image = image.reshape((image.shape[0] * image.shape[1], 3))
  type(image)

  novalista = [x for x in image if list(x) != [255, 255, 255]]

  # cluster the pixel intensities
  clt = KMeans(3)
  clt.fit(novalista)
  return clt

def centroid_histogram(clt):
  # grab the number of different clusters and create a histogram
  # based on the number of pixels assigned to each cluster
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  (hist, _) = np.histogram(clt.labels_, bins = numLabels)
 
  # normalize the histogram, such that it sums to one
  hist = hist.astype("float")
  hist /= hist.sum()
 
  # return the histogram
  return hist

def plot_colors(hist, centroids):
  # initialize the bar chart representing the relative frequency
  # of each of the colors
  bar = np.zeros((50, 300, 3), dtype = "uint8")
  startX = 0

  print(hist)
  print(centroids)

  # loop over the percentage of each cluster and the color of
  # each cluster
  for (percent, color) in zip(hist, centroids):
    # plot the relative percentage of each cluster
    endX = startX + (percent * 300)
    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
    color.astype("uint8").tolist(), -1)
    startX = endX
  # return the bar chart
  return bar

#def buscaCoordenadas(img, vetRosto):
#  x1, y1, x2, y2 = 0
#  for linha in range(0, largura):
#    for coluna in range(0, altura):
#      if img[coluna, linha, 0] == vetRosto[coluna] and img[coluna, linha, 1] == vetRosto[coluna] and img[coluna, linha, 2] == vetRosto[coluna]:
#        if coluna > y1 and linha > x1
#          x1 = linha
#          y1 = coluna

img = cv2.imread('naruto.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgExtracaoBordas = extraiBorda(gray)

imgPeleExtraida = extraiPele(img)
imgSegmetada = segmentaRegioes(imgPeleExtraida)

teste = kmeansImagemRGB(imgSegmetada)

# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color
hist = centroid_histogram(teste)
bar = plot_colors(hist, teste.cluster_centers_)
 
# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()

cv2.waitKey(0)
