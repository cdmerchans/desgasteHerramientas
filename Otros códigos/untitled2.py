from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import rescale
from Funciones import CentarImagen, FiltarImagenPerfil
import matplotlib.pyplot as plot
import numpy as np
from skimage.exposure import equalize_hist, adjust_sigmoid
from skimage.filters import threshold_local
from skimage.morphology import area_closing, area_opening
from skimage.feature import canny

import time

class Herramienta:
    
    def __init__(self, nombre, thetaobjetivo, ancho, rangoX, rangoY, perdidaY, sigmoid, thresholdLocal, areaThreshold):
        
        self.nombre = nombre
        self.thetaobjetivo = thetaobjetivo
        self.ancho = ancho
        self.rangoX = rangoX
        self.rangoY = rangoY
        self.perdidaY = perdidaY
        self.sigmoid = sigmoid
        self.thresholdLocal = thresholdLocal
        self.areaThreshold = areaThreshold
        
def Perfiles(imagen, sigmoid, thresholdLocal,areaThreshold):
    
    imagen = equalize_hist(imagen)
  
    if sigmoid:
        
        imagen = adjust_sigmoid(imagen)

    threshold = threshold_local(imagen, thresholdLocal, offset=0)
    imagen = imagen > threshold

    imagen = area_closing(imagen,area_threshold=areaThreshold, connectivity=1, parent=None, tree_traverser=None)
    imagen = area_opening(imagen,area_threshold=areaThreshold, connectivity=1, parent=None, tree_traverser=None)

    imagen = canny(imagen) 
        
    x = []
    y = []
    
    for i in range(2, np.size(imagen,1)-2):
        for j in range(2, np.size(imagen,0)):
            if imagen[j,i] > 0:
                x.append(i)
                y.append(j)
    return x, y

        
file = open('C:/Users/PC/Documents/Archivos/Análisis de desgaste/Código final/Herramientas disponibles/Herramienta esférica de 3mm.txt')
contents = file.read().split('\n')

herramienta = Herramienta('Herramienta esférica de 3 mm', float(contents[0]), float(contents[1]), int(contents[2]), int(contents[3]), int(contents[4]), bool(contents[5]), int(contents[6]), int(contents[7]))

imagen  = imread('C:/Users/PC/Documents/Archivos/Análisis de desgaste/350/Esférica de 3 mm/19-05-2022/Imágenes/1/Thu May 19 17-04-27.jpg')
imagenGris = rgb2gray(imagen)
imagenEscalada = rescale(imagenGris, 0.2, anti_aliasing=False)

x1 = 330
y1 = 450
x2 = 600
y2 = 540

imagen, alma = CentarImagen(imagenEscalada, herramienta, x1, x2, y1, y2)

imagen = imagen[range(alma[0]-herramienta.rangoX,alma[0]+herramienta.rangoX),:]
imagen1 = imagen[:,range(alma[1]-herramienta.perdidaY-herramienta.rangoY,alma[1]-herramienta.perdidaY)]
imagen2 = imagen[:,range(alma[1]+herramienta.perdidaY,alma[1]+herramienta.perdidaY+herramienta.rangoY)]

start = time.time()
xi, yi = Perfiles(imagen1, True, 551, 10240)
end = time.time()
xd, yd = Perfiles(imagen2, True, 551, 10240)


figura, f1 = plot.subplots(ncols = 2, figsize = (12,8))
f1[0].imshow(imagen1,cmap = 'gray')
f1[1].imshow(imagen2,cmap = 'gray')
f1[0].scatter(xi,yi, s = 0.5, color = 'red')
f1[1].scatter(xd, yd, s = 0.5, color = 'red')


print(end - start)