from traceback import print_tb
import numpy as np
from utils.Secciones import *
from tkinter import messagebox

import matplotlib.pyplot as plot
from utils.Funciones import EscribirPerfil, FactoresDeConversion

rutaImagen = SeleccionarImagen()
nombreArchivo = rutaImagen.split("/")[-1].split(".")[0]

if rutaImagen != 'Repetir':

    tipoHerramienta = SeleccionarTipoHerramienta()

    if tipoHerramienta != '----------':

        imagenEscalada, exito, x1, y1, x2, y2 = SeleccionarPuntos(rutaImagen)

        if exito == True:

            imagenCentrada, almaCentrada = PreprocesarImagen(imagenEscalada, tipoHerramienta, x1, x2, y1, y2)

            imagenIzquierda, imagenDerecha, xIzquierda,yIzquierda,xDerecha,yDerecha, herramienta = ObtenerPerfil(imagenCentrada, tipoHerramienta,almaCentrada)

            factorVertical, factorHorizontal = FactoresDeConversion(herramienta)
            print(factorVertical)
            print(factorHorizontal)

            if almaCentrada != False and xIzquierda != False:

                herramientaNueva = messagebox.askyesno(message="¿La herramienta es nueva?", title="Aviso")
  
                if herramientaNueva == False:

                    xNuevoIzquierda, yNuevoIzquierda, xNuevoDerecha, yNuevoDerecha  = SeleccionarPerfil()

                    DesgasteIzquierda, DesgasteDerecha = CalcularDesgaste(xNuevoIzquierda, yNuevoIzquierda, xNuevoDerecha, yNuevoDerecha, xIzquierda, yIzquierda, xDerecha, yDerecha)

                    #rutaGuardarPerfil = filedialog.asksaveasfilename(title = "¿Dónde quiere guardar el archivo del perfil de la nueva herramienta?")
         
                    #if rutaGuardarPerfil != '':

                    nombreArchivo, rutaCarpetaHerramienta = EscribirPerfil(rutaImagen, xIzquierda,yIzquierda,xDerecha,yDerecha)

                    #rutaGuardarArea = filedialog.asksaveasfilename(title = "¿Dónde quiere guardar el archivo del desgaste de la herramienta?")

                    #rutaGuardarResultados = filedialog.asksaveasfilename(title = "¿Dónde quiere guardar el archivo de resultados?")
                    
                    #if rutaGuardarResultados != '':
                    print(np.array(xDerecha))
                    print('--------')
                    print(np.array(xDerecha)/factorHorizontal)
                    figura, f1 = plot.subplots(ncols = 2, nrows = 3, figsize = (12,8))
                    f1[0,0].imshow(imagenEscalada,cmap = 'gray')
                    f1[0,1].imshow(imagenCentrada,cmap = 'gray')
                    f1[0,1].plot(almaCentrada[1], almaCentrada[0], color='red', marker='+',linestyle='None', markersize=6)
                    f1[1,0].imshow(imagenIzquierda,cmap = 'gray')
                    f1[1,1].imshow(imagenDerecha,cmap = 'gray')
                    f1[1,0].scatter(xIzquierda,yIzquierda, s = 0.5, color = 'red')
                    f1[1,1].scatter(xDerecha,yDerecha, s = 0.5, color = 'red')
                    f1[2,0].bar(np.array(xIzquierda), np.array(DesgasteIzquierda)*(1/factorVertical))
                    f1[2,1].bar(np.array(xDerecha), np.array(DesgasteDerecha)*(1/factorVertical))
                    figura.savefig(rutaCarpetaHerramienta+'/Resultados/'+nombreArchivo,dpi=500)                      
                    #f1.set_xticklabels
                else: 

                    #rutaGuardarPerfil = filedialog.asksaveasfilename(title = "¿Dónde quiere guardar el archivo del perfil de la nueva herramienta?")
                    
                    #if rutaGuardarPerfil != '':

                    nombreArchivo, rutaCarpetaHerramienta = EscribirPerfil(rutaImagen, xIzquierda,yIzquierda,xDerecha,yDerecha)

                    #rutaGuardarResultados = filedialog.asksaveasfilename(title = "¿Dónde quiere guardar el archivo de resultados?")
                    
                    #if rutaGuardarResultados != '':

                    figura, f1 = plot.subplots(ncols = 2, nrows = 2, figsize = (12,8))
                    f1[0,0].imshow(imagenEscalada,cmap = 'gray')
                    f1[0,1].imshow(imagenCentrada,cmap = 'gray')
                    f1[0,1].plot(almaCentrada[1], almaCentrada[0], color='red', marker='+',linestyle='None', markersize=6)
                    f1[1,0].imshow(imagenIzquierda,cmap = 'gray')
                    f1[1,1].imshow(imagenDerecha,cmap = 'gray')
                    f1[1,0].scatter(xIzquierda,yIzquierda, s = 0.5, color = 'red')
                    f1[1,1].scatter(xDerecha,yDerecha, s = 0.5, color = 'red')
                    figura.savefig(rutaCarpetaHerramienta+'/Resultados/'+nombreArchivo,dpi=500)   