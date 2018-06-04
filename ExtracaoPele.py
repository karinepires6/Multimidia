import cv2
import numpy as np
img = cv2.imread('naruto.png')

#Transforma a imagem original em matrizes nos canais RGB
B = img[:, :, 0]
G = img[:, :, 1]
R = img[:, :, 2]

#Define a altura e a largura da imagem de entrada
largura = img.shape[1]
altura = img.shape[0]

#Define uma matriz com zeros com as dimensões da imagem original
blank_image = np.zeros((altura,largura,1), np.uint8)

#Percorre os pixels das matrizes RGB
for linha in range(0, largura):
  for coluna in range(0, altura):  
    #Verifica se o pixel representa um pixel de pele
    if (R[coluna, linha] > 120 and R[coluna, linha] < 255) and (G[coluna, linha] > 90 and G[coluna, linha] < 250) and (B[coluna, linha] > 70 and B[coluna, linha] < 218) and (R[coluna, linha] > G[coluna, linha]) and (G[coluna, linha] > B[coluna, linha]):
      #lin.append(0)
      blank_image[coluna, linha] = 0
    else:
      blank_image[coluna, linha] = 255

#Exibe a suposta matriz com os pixels de pele da matriz original
cv2.imshow("Matriz final", blank_image)
cv2.waitKey(0)
