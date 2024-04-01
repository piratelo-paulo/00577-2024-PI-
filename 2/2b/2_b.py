import os
import rasterio as rs
import numpy as np
import matplotlib.pyplot as plt
import cv2

#refs satellite
#https://www.esri.com/arcgis-blog/products/arcgis-desktop/imagery/band-combinations-for-worldview-2/
#https://satimagingcorp.s3.amazonaws.com/site/pdf/WorldView-2_8-Band_Applications_Whitepaper.pdf


def choosing_bands(images_path, list_of_images, list_of_bands):
    """
    function to choose the bands from the .tif and generates the images
    """
    images_filtered = []

    for img in list_of_images:

        with rs.open(os.path.join(images_path, img), 'r') as file:
            arr_st = file.read()

        features = np.moveaxis(arr_st, 0, -1)

        #UINT16 (range: 0 through 65535 decimal)
        bands_filtered = features[:,:, list_of_bands]

        #normalizing/converting to an RGB like format (255 values)
        bands_1 = bands_filtered[:,:,0]
        bands_2 = bands_filtered[:,:,1]
        bands_3 = bands_filtered[:,:,2]

        bands_1 = (bands_1-np.min(bands_1))/np.max(bands_1)*255
        bands_2 = (bands_2-np.min(bands_2))/np.max(bands_2)*255
        bands_3 = (bands_3-np.min(bands_3))/np.max(bands_3)*255


        bands_filtered = np.moveaxis(np.uint8([bands_1,bands_2,bands_3]),0,-1)

        images_filtered.append(bands_filtered)
       
    
    return images_filtered

images_path = os.path.join("C:/Users/Paulo/Documents/ISI Embarcados/", 
                           "vagas/Pesquisador I - 00577_2024 -14-03-2024/prova_pratica/exercicios/2/images")

results_path = 'C:/Users/Paulo/Documents/ISI Embarcados/vagas/Pesquisador I - 00577_2024 -14-03-2024/prova_pratica/exercicios/2/results/'

#getting the list of images
list_of_images = []
for i in os.listdir(images_path):
    #print(i)
    list_of_images.append(i)

#vegetation     NIR2	Yellow	Coastal
#                8        4        1       
bands_vegetation = [8, 4, 1]
#python's format of index
bands_vegetation = [x - 1 for x in bands_vegetation]

#print(bands_vegetation)

#choosing the bands "vegetation"
images_vegetation = choosing_bands(images_path, list_of_images, bands_vegetation)

#RGB            Red 	Green	  Blue
#                5        3        2       
bands_RGB = [5, 3, 2]
#python's format of index
bands_RGB = [x - 1 for x in bands_RGB]

#choosing the bands "RGB"
images_RGB = choosing_bands(images_path, list_of_images, bands_RGB)

#checking values and info
#print("type: ",  images_vegetation[0].dtype) 
#print("shape: ", images_vegetation[0].shape) 
#print("minimo valor: ", np.min(images_vegetation[0]))
#print("maximo valor: ", np.max(images_vegetation[0]))


#choosing the boundaries for the vegetation in a HSV map range 
#https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/

# lower boundary RED color range values; Hue (0 - 6) 
lower1 = np.array([0, 150, 20])
upper1 = np.array([6, 255, 255])

# upper boundary RED color range values; Hue (175 - 179)
lower2 = np.array([175,150,20])
upper2 = np.array([179,255,255])

#processing the images and getting the results
for idx, image in enumerate(images_vegetation):

    #transforming to HSV color
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    #applying the boundaries to get the vegetation red values
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)
    
    #getting the mask
    full_mask = lower_mask + upper_mask
    
    #ploting the result on the RGB image
    result = cv2.bitwise_and(images_RGB[idx], images_RGB[idx], mask=full_mask)
    
    #saving masks and RGB image with ROI
    plt.imsave(results_path + 'mask' + str(idx) + ".png", full_mask)
    plt.imsave(results_path + 'vegetation_segmented' + str(idx) + ".png", result)
    



