import cv2
from funcs import medianCut, constructImage
import numpy as np


#imagem BGR (RGB pra que)
image = cv2.imread('testPics/birds.jpeg')
grupos = medianCut(image, 255)
novaImagem = constructImage(grupos, image)
novaImagem = np.array(novaImagem)
cv2.imshow("imagem", novaImagem)
#important, do not remove
cv2.waitKey(0)
cv2.destroyAllWindows()