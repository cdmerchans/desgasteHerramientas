import os

class Herramienta:
    
    def __init__(self, nombre, thetaobjetivo, rangoX, rangoY, sigmoid, thresholdLocal, areaThreshold):
        
        self.nombre = nombre
        self.thetaobjetivo = thetaobjetivo
        self.rangoX = rangoX
        self.rangoY = rangoY
        self.sigmoid = sigmoid
        self.thresholdLocal = thresholdLocal
        self.areaThreshold = areaThreshold
        

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
    

a = VerificarCarpetas('C:/Users/PC/Documents/Archivos/Análisis de desgaste/550/Tórica de 1.5 mm/23-03-2022/Imágenes/2/Wed Mar 23 16-31-37.jpg')





herramientasDisponibles = []
rutaHerramientas = 'C:/Users/PC/Documents/Archivos/Análisis de desgaste/Código final/Herramientas disponibles'

for archivo in os.listdir(rutaHerramientas):
    
    if archivo.endswith(".txt"):
        
        herramientasDisponibles.append(archivo.removesuffix('.txt'))
        
        
try:
    herramientasDisponibles.index('Herramienta esférica de 1.5mmasd')
	except ValueError as verr:

		return False
        
        
  
file = open(rutaHerramientas+'/'+herramientasDisponibles[2]+'.txt')
contents = file.read().split('\n')

herramienta = Herramienta(herramientasDisponibles[2], float(contents[0]), int(contents[1]), int(contents[2]), bool(contents[3]), int(contents[4]), int(contents[5]))
    