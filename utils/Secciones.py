from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import rescale
import plotly.express as px
import numpy as np
from scipy import signal

from .Clases import *
from .Funciones import *

def SeleccionarImagen():

    rutaImagen = askopenfilename(title = "Escoja la imagen de la herramienta a analizar", filetypes = (("jpg files","*.jpg"),("all files","*.*")))

    if rutaImagen.endswith('.jpg'):
        
        return rutaImagen

    else:
        return 'Repetir'

def SeleccionarTipoHerramienta():

    ventanaListaHerramientas = VentanaListaHerramientas()
    tipoHerramienta = ventanaListaHerramientas.tipoHerramienta.get()

    try :
        
        ventanaListaHerramientas.close()
        
    except:
        
        return '----------'

    return tipoHerramienta

def SeleccionarPuntos(rutaImagen):

    imagen  = imread(rutaImagen)
    imagenGris = rgb2gray(imagen)
    print(imagenGris.shape)
    imagenEscalada = rescale(imagenGris, [948/imagenGris.shape[0], 1265/imagenGris.shape[1]], anti_aliasing=False)
    print(imagenEscalada.shape)
    figura = px.imshow(imagenEscalada, color_continuous_scale='gray')
    figura.update_layout(coloraxis_showscale=False)
    figura.update_xaxes(showticklabels=False)
    figura.update_yaxes(showticklabels=False)
    figura.show()   

    banderaCoordenadas = False

    while not banderaCoordenadas:

        ventanaCoordenadas = VentanaCoordenadas()
        banderaCoordenadas = ventanaCoordenadas.verificarCoordenadas()

        if banderaCoordenadas:

            y1 = int(ventanaCoordenadas.x1.get())
            x1 = int(ventanaCoordenadas.y1.get())
            y2 = int(ventanaCoordenadas.x2.get())
            x2 = int(ventanaCoordenadas.y2.get())

        try:

            ventanaCoordenadas.close()
            exito = True

        except:

            exito = False

    return imagenEscalada, exito, x1, y1, x2, y2

def PreprocesarImagen(imagen, tipo, x1, x2, y1, y2):

    herramienta = RecortarTipoHerramienta(tipo)

    if herramienta != 'Herramienta no encontrada':

        try:

            imagenCentrada, almaCentrada = CentarImagen(imagen, herramienta, x1, x2, y1, y2)

            return imagenCentrada, almaCentrada
        
        except:
        
            return '[]', False
    else:

        return [], False

def ObtenerPerfil(imagen, tipo, alma):

    herramienta = RecortarTipoHerramienta(tipo)

    if herramienta != 'Herramienta no encontrada':

        try:

            imagenIzquierda, imagenDerecha,xIzquierda, yIzquierda, xDerecha, yDerecha= DeterminarPerfil(imagen, herramienta, alma)

            return imagenIzquierda, imagenDerecha, xIzquierda, yIzquierda, xDerecha, yDerecha, herramienta

        except Exception as e:

            return [e], [], False, False, False, False, False

    else:
        
        return '[ee]', [], False, False, False, False, False

def SeleccionarPerfil():

    rutaPerfil = filedialog.askopenfilename(title = "Escoja el perfil con el que se va a comprar", filetypes = (("csv files","*.csv"),("all files","*.*")))

    if rutaPerfil.endswith('.csv'):

        xIzquierda, yIzquierda, xDerecha, yDerecha = LeerPerfil(rutaPerfil)
        
        return xIzquierda, yIzquierda, xDerecha, yDerecha 

    else:

        return False, False, False, False

def CalcularDesgaste(xINuevo, yINuevo, xDNuevo, yDNuevo, xI, yI, xD, yD):

    try:

        distanciasIzquierda = MedirDesgaste(xINuevo,yINuevo,xI,yI)

        distanciasDerecha = MedirDesgaste(xDNuevo,yDNuevo,xD,yD)

        return distanciasIzquierda, distanciasDerecha

    except Exception as e:

        return e, False