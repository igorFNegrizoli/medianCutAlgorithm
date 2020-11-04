import cv2
from funcs import medianCut, constructImage
import numpy as np
from bmp import buildBMP


#imagem BGR (RGB pra que)
image = cv2.imread('testPics/birds.jpeg')
grupos = medianCut(image, 255)
image = constructImage(grupos, image)
buildBMP(image, "teste.bmp")
#image = np.array(image)
#cv2.imshow("imagem", image)
#important, do not remove
#cv2.waitKey(0)
#cv2.destroyAllWindows()
