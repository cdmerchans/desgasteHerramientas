import statistics as stat
from xml.dom import minicompat
from matplotlib.pyplot import prism
import numpy as np
import math
import csv
from scipy import signal
from skimage import io
from skimage.transform import rotate, rescale
from skimage.filters import threshold_local
from skimage.morphology import area_closing, area_opening
from skimage.feature import canny
from skimage.exposure import equalize_hist, adjust_sigmoid
import os

class Herramienta:
    
    def __init__(self, nombre, thetaobjetivo, ancho, rangoX, rangoY, perdidaY, sigmoid, thresholdLocal, areaThreshold, distanciaReferencia):
        
        self.nombre = nombre
        self.thetaobjetivo = thetaobjetivo
        self.ancho = ancho
        self.rangoX = rangoX
        self.rangoY = rangoY
        self.perdidaY = perdidaY
        self.sigmoid = sigmoid
        self.thresholdLocal = thresholdLocal
        self.areaThreshold = areaThreshold
        self.distanciaReferencia = distanciaReferencia

def LeerListadoHerramientas(ruta):
    
        herramientasDisponibles = []
        rutaHerramientas = ruta #'C:/Users/PC/Documents/Archivos/Análisis de desgaste/Código final/Herramientas disponibles'
        
        for archivo in os.listdir(rutaHerramientas):
            
            if archivo.endswith(".txt") and not archivo.startswith("."):
                
                herramientasDisponibles.append(archivo.removesuffix('.txt'))

        return herramientasDisponibles

def VerificarEntero(variable):

	try:

		entero = int(variable)
		return True

	except ValueError as verr:

		return False

def MedirDistanciaTotal(coordenadas1, coordenadas2):

    distanciaTotalEnx = coordenadas2[0]-coordenadas1[0]
    distanciaTotalEny = coordenadas2[1]-coordenadas1[1]

    distanciaTotalTotal =  math.sqrt(distanciaTotalEnx**2+distanciaTotalEny**2)

    return distanciaTotalTotal, abs(distanciaTotalEnx), abs(distanciaTotalEny)

def RecortarTipoHerramienta(tipoHerramienta):
    
    herramientasDisponibles = []
    rutaHerramientas = './Herramientas disponibles'

    for archivo in os.listdir(rutaHerramientas):
        
        if archivo.endswith(".txt"):
            
            herramientasDisponibles.append(archivo.removesuffix('.txt'))

    try:
        
        herramientasDisponibles.index(tipoHerramienta)
        
        file = open(rutaHerramientas+'/'+tipoHerramienta+'.txt')
        contents = file.read().split('\n')
        
        herramienta = Herramienta(herramientasDisponibles[2], float(contents[0]), float(contents[1]), int(contents[2]), int(contents[3]), int(contents[4]), bool(contents[5]), int(contents[6]), int(contents[7]), float(contents[8]))
        
        return herramienta
    
    except ValueError as verr:
    
        return 'Herramienta no encontrada'

def CentarImagen(imagen, herramienta, x1, x2, y1, y2):

    distanciaTotalPatron = [100,400]

    thetaObjetivo = herramienta.thetaobjetivo

    coordenadas = np.matrix([[x1,y1],[x2,y2]])
    theta = math.atan((coordenadas[1,0]-coordenadas[0,0])/(coordenadas[1,1]-coordenadas[0,1]))

    distanciaTotal, distanciaEnx, distanciaEny =  MedirDistanciaTotal((np.asarray(coordenadas[1])).flatten(), (np.asarray(coordenadas[0])).flatten())

    alma = np.asarray(coordenadas[1,:]-[distanciaTotal/2*math.sin(theta),distanciaTotal/2*math.cos(theta)])[0]

    imagenRotada = rotate(imagen, -thetaObjetivo+theta*180/math.pi, center = [alma[1], alma[0]])

    alpha = thetaObjetivo*math.pi/180
    deltayRotado = distanciaTotal/2*(math.cos(theta)-math.cos(alpha))
    deltaxRotado = distanciaTotal/2*(math.sin(alpha)-math.sin(theta))
    coordenadasRotadas = np.matrix([[x1-deltaxRotado,y1+deltayRotado],[x2+deltaxRotado,y2-deltayRotado]])
    distanciaTotal, distanciaEnx, distanciaEny =  MedirDistanciaTotal((np.asarray(coordenadasRotadas[1])).flatten(), (np.asarray(coordenadasRotadas[0])).flatten())

    escalaEnx = distanciaTotalPatron[1]/distanciaEnx
    escalaEny = distanciaTotalPatron[0]/distanciaEny
    escalas = (escalaEnx, escalaEny)
    imagenEscalada = rescale(imagenRotada,escalas,anti_aliasing=True)

    coordenadasEscaladas = np.multiply(coordenadasRotadas,escalas)
    almaEscalada = np.multiply(alma,escalas)

    imagenCentrada = imagenEscalada[range(int(coordenadasEscaladas[0,0]),int(coordenadasEscaladas[1,0])),:]

    ancho = herramienta.ancho

    imagenCentrada = imagenCentrada[:,range(int(almaEscalada[1])-int(distanciaTotalPatron[0]*ancho),int(almaEscalada[1])+int(distanciaTotalPatron[0]*ancho))]
    almaCentrada = [int(np.size(imagenCentrada,0)/2),int(np.size(imagenCentrada,1)/2)]

    return imagenCentrada, almaCentrada

def FiltarImagenPerfil(imagen, sigmoid, thresholdLocal, areaThreshold):

    imagen = equalize_hist(imagen)
  
    if sigmoid:
        
        imagen = adjust_sigmoid(imagen)

    threshold = threshold_local(imagen, thresholdLocal, offset=0)
    imagen = imagen > threshold

    imagen = area_closing(imagen,area_threshold=areaThreshold, connectivity=1, parent=None, tree_traverser=None)
    imagen = area_opening(imagen,area_threshold=areaThreshold, connectivity=1, parent=None, tree_traverser=None)

    imagen = canny(imagen) 

    return imagen

def DeterminarPerfil(imagen, herramienta, alma):

    imagen = imagen[range(alma[0]-herramienta.rangoX,alma[0]+herramienta.rangoX),:]
    imagen1 = imagen[:,range(alma[1]-herramienta.perdidaY-herramienta.rangoY,alma[1]-herramienta.perdidaY)]
    imagen2 = imagen[:,range(alma[1]+herramienta.perdidaY,alma[1]+herramienta.perdidaY+herramienta.rangoY)]
    sigmoid = herramienta.sigmoid
    thresholdLocal = herramienta.thresholdLocal 
    areaThreshold = herramienta.areaThreshold 

    imagenIzquierda = FiltarImagenPerfil(imagen1, sigmoid, thresholdLocal, areaThreshold)   
    imagenDerecha = FiltarImagenPerfil(imagen2, sigmoid, thresholdLocal, areaThreshold)

    xIzquierda = []
    yIzquierda = []

    for i in range(2, np.size(imagenIzquierda,1)-2):
        for j in range(2, np.size(imagenIzquierda,0)):
            if imagenIzquierda[j,i] > 0:
                xIzquierda.append(i)
                yIzquierda.append(j)

    xDerecha = []
    yDerecha = []

    for i in range(2, np.size(imagenDerecha,1)-2):
        for j in range(np.size(imagenDerecha,0)-2):
            if imagenDerecha[j,i] > 0:
                xDerecha.append(i)
                yDerecha.append(j)

    return imagen1, imagen2, xIzquierda, yIzquierda, xDerecha, yDerecha

def VerificarCarpetas(rutaImagen):

    rutaDesglosada = rutaImagen.split("/")
    
    nombreArchivo = rutaDesglosada[-1].split(".")[0]
    
    for i in range(3):
        rutaDesglosada.remove(rutaDesglosada[-1])
    
    rutaCarpetaHerramienta = '/'.join(rutaDesglosada)
    
    if not os.path.exists(rutaCarpetaHerramienta+'/Resultados'):

        os.mkdir(rutaCarpetaHerramienta+'/Resultados') 

    if not os.path.exists(rutaCarpetaHerramienta+'/Perfiles'):
    
        os.mkdir(rutaCarpetaHerramienta+'/Perfiles') 
    
    return nombreArchivo, rutaCarpetaHerramienta

def EscribirPerfil(rutaImagen, xIzquierda, yIzquierda, xDerecha, yDerecha):

    nombreArchivo, rutaCarpetaHerramienta = VerificarCarpetas(rutaImagen)
    print(nombreArchivo)
    print(rutaCarpetaHerramienta)
    limite = np.size(xIzquierda)
    x = np.concatenate((limite,xIzquierda,xDerecha), axis = None)
    y = np.concatenate((limite,yIzquierda,yDerecha), axis = None)


    with open(rutaCarpetaHerramienta+'/Perfiles/'+nombreArchivo+'.csv', "w", newline='') as filePerfil:
                writer = csv.writer(filePerfil, delimiter='\t')
                writer.writerows(np.column_stack((x,y)))

    return nombreArchivo, rutaCarpetaHerramienta


def LeerPerfil(rutaPerfil):

    with open(rutaPerfil) as file:
        reader = csv.reader(file,delimiter="\t")
        perfilNuevo = np.array(list(reader))
        perfilNuevo = perfilNuevo.astype(np.float)
        
        
    xIzquierda = list(perfilNuevo[range(1,int(perfilNuevo[0,0]+1)),0].astype(int))
    yIzquierda = list(perfilNuevo[range(1,int(perfilNuevo[0,0]+1)),1].astype(int))
    xDerecha = list(perfilNuevo[range(int(perfilNuevo[0,0]+1), perfilNuevo.shape[0]),0].astype(int))
    yDerecha = list(perfilNuevo[range(int(perfilNuevo[0,0]+1),perfilNuevo.shape[0]),1].astype(int))

    return xIzquierda, yIzquierda, xDerecha, yDerecha

def MedirDesgaste(xNuevo, yNuevo, xActual, yActual):

    distancias = []
    xNuevo = np.array(xNuevo)
    yNuevo = np.array(yNuevo)
    xActual =np.array(xActual)
    yActual= np.array(yActual)

    for i in range(np.size(xActual)):
        xa = xActual[i]
        absolute_val_array = np.abs(xNuevo - xa)
        smallest_difference_index = absolute_val_array.argmin()
        distancia = yNuevo[smallest_difference_index]-yActual[i]
        distancias.append(distancia)

    numeradorFiltro, denominadorFiltro = signal.butter(8, 0.025, 'lowpass')
    distancias = signal.filtfilt(numeradorFiltro, denominadorFiltro, distancias) 
    
    return distancias

def ValoresDesgateTotal(desgate):

    maximo = max(desgate)
    minimo = min(desgate)
    promedio = stat.mean(desgate)

    if len(desgate[desgate>0]) != 0:
        promedioPositivo = stat.mean(desgate[desgate>0])
    else:
        promedioPositivo = 0
    if len(desgate[desgate<0]) != 0:
        promedioNegativo = stat.mean(desgate[desgate<0])
    else:
        promedioNegativo = 0

    return round(maximo,2), round(minimo,2), round(promedio,2), round(promedioPositivo,2), round(promedioNegativo,2)


def ValoresDesgate(desgate, x):

    maximo = max(desgate)
    minimo = min(desgate)
    promedio = stat.mean(desgate)
    integral = np.trapz(desgate, x)

    if len(desgate[desgate>0]) != 0:
        desgastePositivo = []
        xPositivo = []
        for i in range(np.size(desgate)):
            if desgate[i]>0:
                desgastePositivo.append(desgate[i]) 
                xPositivo.append(x[i])

        promedioPositivo = stat.mean(desgastePositivo)
        integralPositiva = np.trapz(desgastePositivo, xPositivo)
    else:
        promedioPositivo = 0
        integralPositiva = 0
    if len(desgate[desgate<0]) != 0:
        desgasteNegativo = []
        xNegativo = []
        for i in range(np.size(desgate)):
            if desgate[i]<0:
                desgasteNegativo.append(desgate[i]) 
                xNegativo.append(x[i])
        promedioNegativo = stat.mean(desgasteNegativo)
        integralNegativa = np.trapz(desgasteNegativo, xNegativo)
    else:
        promedioNegativo = 0
        integralNegativa = 0

    return round(maximo,2), round(minimo,2), round(promedio,2), round(promedioPositivo,2), round(promedioNegativo,2), round(integral,2), round(integralPositiva,2), round(integralNegativa,2), 

def FactoresDeConversion(herramienta):

    distancia = herramienta.distanciaReferencia
    print(distancia)
    print(herramienta.thetaobjetivo)
    theta = herramienta.thetaobjetivo*math.pi/180
    print(theta)

    factorVertical = 400/(distancia*math.sin(theta))
    factorHorizontal = 100/(distancia*math.cos(theta))

    return factorVertical, factorHorizontal