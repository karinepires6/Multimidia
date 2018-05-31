import cv2
img = cv2.imread('teste.jpg')

matriz = []
for i in img:
	# Split eye image into 3 channels
        B = eye[:, :, 0]
        G = eye[:, :, 1]
        R = eye[:, :, 2]

	if (120 < R < 255) and (90 < G < 250) and (70 < B < 218) and (R > G) and (G > B):
		matriz[i]=1
	else
		matriz[i]=0

%(B, G, R) = cv2.split(img)
cv2.imshow("Vermelho", matriz)
%cv2.imshow("Verde", G)
%cv2.imshow("Azul", B)
cv2.waitKey(0)
