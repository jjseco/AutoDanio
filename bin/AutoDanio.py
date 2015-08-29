# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:30:30 2015

@author: user
"""

##################################################################
#                  Librerias Necesarias                          #
##################################################################
#from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
%matplotlib inline

################################################################ 
#                 Definición de funciones                      #
################################################################

# Conversión a escala de grises
def esgri(imagen):
    imagen=cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY )
    return imagen

# Normalización de la imagen escala 0:1
def normalizacion(x):
    a = []
    for pixel in np.nditer(x):
        b=float(pixel)/x.max()
        a.append(b)
  
    B = np.reshape(a, (len(x),len(x)))
    return B

# Reajuste de la imagen para disminuir el ruido de la misma
def reajuste(x):
    for pixel in np.nditer(x, op_flags=['readwrite']):
        if pixel>0.75:
            pixel[...]=1
        else:
            pixel[...]=pixel
        if pixel<0.7:
            pixel[...]=random.uniform(0.1,0.4)
        else:
            pixel[...]=pixel
    return x

#This board possesses a 0 border that allows to accelerate things a bit by avoiding to have specific tests for 
#borders when counting the number of neighbours. First step is to count neighbours:

def compute_neigbours(image_final):
    image_final.astype(int)
    shape = len(image_final), len(image_final[0])
    N  = [[0,]*(shape[0])  for i in range(shape[1])]
    for x in range(1,shape[0]-1):
        for y in range(1,shape[1]-1):
            N[x][y] = image_final[x][y-1] \
                    + image_final[x-1][y]            +image_final[x+1][y]   \
                    + image_final[x][y+1]
            
                 
    return N


# Determinación de la concentración de ms (sustancia producida por los melanoforos)

def delta_ms (image_final):
    shape = len(image_final), len(image_final[0])
    ms  = [[0,]*(shape[0])  for i in range(shape[1])]
    for r in range(1,shape[0]-1):
        for s in range(1,shape[1]-1):
            if ms[r][s]<0.2:
                ms[r][s] = (((cmsp * image_final[r][s]) - (cmsd * image_final[r][s])) \
                        + (dms * (N[r][s] - (4* image_final[r][s]))))
            else:
                ms[r][s]==ms[r][s]
            
    return ms


#Cambio en la producción de la sustancia XS, producida por xantoforos
#tener en cuenta la tasa de produccion de xs , cxsp, no està en el paper
def delta_xs (image_final):
    shape = len(image_final), len(image_final[0])
    xs  = [[0,]*(shape[0])  for i in range(shape[1])]
    for r in range(1,shape[0]-1):
        for s in range(1,shape[1]-1):
            if 0.4>xs[r][s]>0.2:
                xs[r][s] = (((cxsp * image_final[r][s]) - (cxsd * image_final[r][s])) \
                        + (dxs * (N[r][s] - (4* image_final[r][s]))))
            else:
                xs[r][s]=xs[r][s]
    return xs

# 
# Cambie por la imagen a procesar
danio= cv2.imread('//home/user/MEGAsync/proyectos/AutoDanio/images/prueba1.JPG')

