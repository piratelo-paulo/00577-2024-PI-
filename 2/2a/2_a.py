import os
import cv2
import numpy as np

image_airport = cv2.imread('C:/Users/Paulo/Documents/ISI Embarcados/vagas/Pesquisador I - 00577_2024 -14-03-2024/prova_pratica/exercicios/2/airport.png')
image_airport_backup = np.copy(image_airport)

#cv2.imshow("image_airport", image_airport)
#checking values and info
print(image_airport.dtype)
print("minimo valor: ", np.min(image_airport))
print("maximo valor: ", np.max(image_airport))
print(image_airport.shape)

hsv_airport = cv2.cvtColor(image_airport, cv2.COLOR_BGR2HSV)

cv2.imwrite("C:/Users/Paulo/Documents/ISI Embarcados/vagas/Pesquisador I - 00577_2024 -14-03-2024/prova_pratica/exercicios/2/airport_HSV.png", hsv_airport)


