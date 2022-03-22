# importar bibliotecas importantes
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# -----------------------------------------------------
# Funcao para exibir a imagem na tela - apenas teste
def printImagem(imagem):
    cv2.imshow("Janela", imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# -----------------------------------------------------

# Por enquanto a leitura é feita a partir de uma imagem estática
# passada por parametro.
# Sugestao: acrescentar a imagem de leitura diretamente a partir 
# da camera.

#################################
#
# 1. CONSTRUCAO DO ARGPARSER
#
#################################

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a imagem")

# falta implementar
ap.add_argument("-g", "--gabarito", 
        help="caminho para o arquivo de texto contendo o gabarito")
args = vars(ap.parse_args())

# gabarito - Implementar leitura do gabarito externa.
GABARITO = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

######################################
#
# 2. Leitura e processamento da imagem
#
######################################

# Consiste na leitura da imagem, conversao para escala de cinza, 
# aplicacao de blur e determinacao dos extremos (algoritmo Canny).
#
# OBSERVACAO - parametros que podem ser calibrados para melhor resultado:
# - kernel da GaussianBlur - (5, 5)
# - sigma da GaussinaBlur - 0
# - Histeresys threshold - Canny: minVal = 75, maxVal = 200 
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)


# print teste
printImagem(edged)


