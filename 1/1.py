import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio

def MSE(image1,image2):
  """ 
  Mean Squared Error
  :param image1: image1
  :param image2: image2
  :rtype: float
  :return: MSE value
  """

  # Calculating the Mean Squared Error
  mse = np.mean(np.square(image1.astype(float) - image2.astype(float)))
  
  return mse

def PSNR(image1, image2, peak=255):
  """ 
  Peak signal-to-noise ratio
  :param image1: image1
  :param image2: image2
  :param peak: max value of pixel 8-bit image (255)
  :rtype: float
  :return: PSNR value
  """

  # Calculating the Mean Squared Error
  mse = MSE(image1,image2)

  # Calculating the Peak Signal Noise Ratio
  psnr = 10*np.log10(peak**2/mse)

  return psnr

path_to_folder = 'C:/Users/Paulo/Documents/ISI Embarcados/vagas/Pesquisador I - 00577_2024 -14-03-2024/prova_pratica/exercicios/1/'
#image grey noise
path_image_gray_noisy = "airport_gray_noisy.png"
image_gray_noisy = cv2.imread(path_to_folder+path_image_gray_noisy)
#image grey
path_image_gray = "airport_gray.png"
image_gray = cv2.imread(path_to_folder+path_image_gray)

#calculating the PSNR 
psnr = PSNR(image_gray, image_gray_noisy)
print("PSNR " + path_image_gray + " and " + path_image_gray_noisy + ": ", psnr)

#Median Filter
kernel_median = 5
median = cv2.medianBlur(image_gray_noisy, kernel_median)

cv2.imwrite(path_to_folder + "kernel_" + str(kernel_median)+ '_median_noise_removed.png', median)

#calculating the PSNR for median
psnr_median = PSNR(image_gray, median)
print("PSNR " + path_image_gray + " and median_kernel_" + str(kernel_median) + ": ", psnr_median)





