from tkinter import *
from Funciones import VerificarEntero
import os
from Funciones import LeerListadoHerramientas        

class VentanaListaHerramientas():

    def __init__(self):

        self.root = Tk()
        self.root.title('')
        self.root.eval('tk::PlaceWindow . center')

        self.root.geometry( "350x100" )
        
        opciones = LeerListadoHerramientas('C:/Users/PC/Documents/Archivos/Análisis de desgaste/Código final/Herramientas disponibles')

        self.tipoHerramienta = StringVar()
        self.tipoHerramienta.set('----------')

        label = Label( self.root , text = " Seleccione el tipo de herramienta a analizar" )
        label.pack()

        menu = OptionMenu( self.root , self.tipoHerramienta , *opciones )
        menu.pack()

        boton = Button( self.root , text = "Seleccionar" , command = self.root.quit ).pack()

        self.root.mainloop()
    
    def close(self):
        self.root.destroy()

class VentanaCoordenadas():

    def __init__(self):
  
        self.root = Tk()
        self.root.title('Inserte las coordenadas de los puntos en la imagen')
        self.root.eval('tk::PlaceWindow . center')

        self.root.geometry( "400x120" )

        Label(self.root, text="Punto 1").grid(row=1, column=2)
        Label(self.root, text="Punto 2").grid(row=1, column=5)
        espacio = '                            '
        Label(self.root, text=espacio, ).grid(row=2, column=0)
        Label(self.root, text="x", ).grid(row=2, column=1)
        Label(self.root, text="y").grid(row=3, column=1)
        Label(self.root, text="x").grid(row=2, column=4)
        Label(self.root, text="y").grid(row=3, column=4)
        Label(self.root, text=espacio, ).grid(row=2, column=6)

        self.x1 = Entry(self.root,width=5)
        self.y1 = Entry(self.root,width=5)
        self.x2 = Entry(self.root,width=5)
        self.y2 = Entry(self.root,width=5)

        self.x1.grid(row=2, column=2)
        self.y1.grid(row=3, column=2)
        self.x2.grid(row=2, column=5)
        self.y2.grid(row=3, column=5)

        boton = Button(self.root, text='Ok', command=self.root.quit).grid(row=4, column=3, sticky=W, pady=4)

        self.root.mainloop()

    def verificarCoordenadas(self):
        
        try:
            condicion1 = VerificarEntero(self.x1.get())
            condicion2 = VerificarEntero(self.y1.get())
            condicion3 = VerificarEntero(self.x2.get())
            condicion4 = VerificarEntero(self.y2.get())
        except:
            condicion1 = False
            condicion2 = False
            condicion3 = False
            condicion4 = False

        if (condicion1 and condicion2 and condicion3 and condicion4):
            return True
        else: 
            return False
    
    def close(self):
        self.root.destroy()