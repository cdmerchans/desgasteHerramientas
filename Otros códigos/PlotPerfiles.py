#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:31:53 2022

@author: cdmerchans
"""

from Funciones import LeerPerfil
import matplotlib.pyplot as plot
from scipy import signal

def Filtrar(desgaste):
    
    numeradorFiltro, denominadorFiltro = signal.butter(4, 0.03, 'lowpass')
    desgaste = signal.filtfilt(numeradorFiltro, denominadorFiltro, desgaste) 
    
    return desgaste


xIzquierda0, yIzquierda0, xDerecha0, yDerecha0 = LeerPerfil('Desktop\\1.csv')
xIzquierda1, yIzquierda1, xDerecha1, yDerecha1 = LeerPerfil('Desktop\\2.csv')
xIzquierda2, yIzquierda2, xDerecha2, yDerecha2 = LeerPerfil('Desktop\\3.csv')
xIzquierda3, yIzquierda3, xDerecha3, yDerecha3 = LeerPerfil('Desktop\\4.csv')

figura, f1 = plot.subplots(ncols = 2, nrows = 1, figsize = (12,8))
f1[0].plot(xIzquierda0, -Filtrar(yIzquierda0), color='red', markersize=6)
f1[0].plot(xIzquierda1, -Filtrar(yIzquierda1), color='blue', markersize=6)
f1[0].plot(xIzquierda2, -Filtrar(yIzquierda2), color='green',markersize=6)
f1[0].plot(xIzquierda3, -Filtrar(yIzquierda3), color='black', markersize=6)

f1[1].plot(xDerecha0, -Filtrar(yDerecha0), color='red',markersize=6)
f1[1].plot(xDerecha1, -Filtrar(yDerecha1), color='blue', markersize=6)
f1[1].plot(xDerecha2, -Filtrar(yDerecha2), color='green',markersize=6)
f1[1].plot(xDerecha3, -Filtrar(yDerecha3), color='black', markersize=6)
    
f1[0].grid()
f1[0].set_xlabel('x [pixel]')
f1[0].set_ylabel('Perfil [pixel]')
f1[0].set_title('Desgaste perfil izquierdo')
f1[0].legend(['Nueva', 'Uso 1', 'Uso 2', 'Uso 3'])
f1[1].grid()
f1[1].set_xlabel('x [pixel]')
f1[1].set_ylabel('Perfil [pixel]')
f1[1].set_title('Desgaste perfil derecho')
f1[1].legend(['Nueva', 'Uso 1', 'Uso 2', 'Uso 3'])
figura.savefig('hola',dpi=500)