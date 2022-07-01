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
import plotly.express as px

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

        
file = open('C:/Users/PC/Documents/Archivos/Análisis de desgaste/Código final/DesgasteHerramientas/Herramientas disponibles/Prueba Ing Cabas.txt')
contents = file.read().split('\n')

herramienta = Herramienta('Herramienta de prueba cuyo nombre vale mondá', float(contents[0]), float(contents[1]), int(contents[2]), int(contents[3]), int(contents[4]), bool(contents[5]), int(contents[6]), int(contents[7]))

#imagen  = imread('C:/Users/PC/Documents/Archivos/Análisis de desgaste/350/Plana de 2 mm/12-04-2022/Imágenes/3/Mon Apr 18 07-33-49.jpg')
imagen  = imread('C:/Users/PC/Desktop/Probetas/E/Fri Jun 17 17-02-55.jpg')
imagen  = imread('C:/Users/PC/Desktop/Probetas/F/Fri Jun 17 17-05-19.jpg')
imagenGris = rgb2gray(imagen)
imagenEscalada = rescale(imagenGris, 0.2, anti_aliasing=False)


figura = px.imshow(imagenEscalada, color_continuous_scale='gray')
figura.update_layout(coloraxis_showscale=False)
figura.update_xaxes(showticklabels=False)
figura.update_yaxes(showticklabels=False)
figura.show() 


x1 = 396#261
y1 = 233#496
x2 = 687#577
y2 = 533#767

imagen0, alma = CentarImagen(imagenEscalada, herramienta, x1, x2, y1, y2)

imagen = imagen0[range(alma[0]-herramienta.rangoX,alma[0]+herramienta.rangoX),:]
imagen1 = imagen[:,range(alma[1]-herramienta.perdidaY-herramienta.rangoY,alma[1]-herramienta.perdidaY)]
imagen2 = imagen[:,range(alma[1]+herramienta.perdidaY,alma[1]+herramienta.perdidaY+herramienta.rangoY)]

start = time.time()
xi, yi = Perfiles(imagen1, herramienta.sigmoid, herramienta.thresholdLocal, herramienta.areaThreshold)
end = time.time()
xd, yd = Perfiles(imagen2, herramienta.sigmoid, herramienta.thresholdLocal, herramienta.areaThreshold)
print(end - start)

figura, f1 = plot.subplots(ncols = 2, nrows = 2, figsize = (12,8))
f1[0,0].imshow(imagenEscalada,cmap = 'gray')
f1[0,1].imshow(imagen0,cmap = 'gray')
f1[0,1].plot(alma[1], alma[0], color='red', marker='+',linestyle='None', markersize=6)
f1[1,0].imshow(imagen1,cmap = 'gray')
f1[1,1].imshow(imagen2,cmap = 'gray')
f1[1,0].scatter(xi,yi, s = 0.5, color = 'red')
f1[1,1].scatter(xd, yd, s = 0.5, color = 'red')
