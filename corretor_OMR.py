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

######################################
#
# 3. Encontrar os contornos da folha
#
######################################

# Busca todos os contornos presentes na imagem (da folha, das alternativas
# dos valores) e, em seguida, ordena e filtra os limites da folha.

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)

# contorno da folha de papel
docCnt = None

# Ordena os contornos e tenta encontrar a folha de papel
if len(cnts) > 0:     # se ao menos um contorno foi encontrado
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
    # percorre o vetor de contornos em ordem decrescente de area
    for c in cnts:
        # determina o perimetro do contorno
        peri = cv2.arcLength(c, True)
        epsilon = 0.02 * peri

        # faz uma aproximacao da curva original 'c' por um 
        # poligono com menos vertices.
        # epsilon e' a precisao da aproximacao. Nesse caso, 2% do
        # perimetro da curva.
        # Como temos uma folha com varias circunferencias, 
        # a aproximacao de maior area e com 4 vértices deve ser
        # a folha de papel.
        
        approx = cv2.approxPolyDP(c, epsilon, True)
        
        if len(approx) == 4:
            docCnt = approx
            break

# aplica transformacao de perspectiva na imagem original e na
# cinza, para uma visao perpendicular do papel
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))
