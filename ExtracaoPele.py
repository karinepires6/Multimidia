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
matrizf = np.zeros((largura, altura))

#Percorre os pixels das matrizes RGB
for coluna in range(0, largura):
  for linha in range(0, altura):
    #Verifica se o pixel representa um pixel de pele
    if (R[linha, coluna] > 120 and R[linha, coluna] < 255) and (G[linha, coluna] > 90 and G[linha, coluna] < 250) and (R[linha, coluna] > 70 and R[linha, coluna] < 218) and (R[linha, coluna] > G[linha, coluna]) and (G[linha, coluna] > B[linha, coluna]):
      matrizf[coluna, linha] = 1
    else:
      matrizf[coluna, linha] = 0

#Exibe a suposta matriz com os pixels de pele da matriz original
cv2.imshow("Matriz final", matrizf)

cv2.waitKey(0)
