# -*- coding: utf-8 -*-
"""
Practica CRI: CrossWord

Enrique Fernandez | NIU: 1456537
Daniel Romero | NIU: 
Sergio Morales | NIU: 
"""

import math
import numpy as np #importem la llibreria
import sys

def leer_panel(crossword):
    panel = []
    for linea in open(crossword):
        panel.append(linea.strip('\t'))
    return panel

def print_panel(panel):
    for i in range(0,len(panel)):
        for j in range(0,len(panel[i])):
            sys.stdout.write(panel[i][j])

def busca_pos_ij(panel,id):
    auxI = -1   #caso de no encontrado
    auxJ = -1
    for i in range(0,len(panel)):
        for j in range(0,len(panel[i])):
            if(panel[i][j] == id):
                auxI=i
                auxJ=j
    return auxI,auxJ

def busca_izq(panel,i,j):
    ret=0
    auxJ = j-1
    while (auxJ >= 0 and panel[i][auxJ] != -1):
        if(panel[i][auxJ] > 0):
            ret=1
        auxJ = auxJ-1       
    return ret

def es_vertical(panel,id):
    auxI,auxJ=busca_pos_ij(panel,id)    #i=fila  j =columna
    ret=0
    if(auxI < len(panel) -1 and panel[auxI+1][auxJ] >= 0):
        if(auxJ < len(panel[auxI]) and panel[auxI][auxJ+1] == -1):
           ret = 1
        if(busca_izq(panel,auxI,auxJ) == 1):
            ret = 1
    return ret
        
def busca_arriba(panel,i,j):
    ret=0
    auxI = i-1
    while (auxI >= 0 and panel[auxI][j] != -1):
        if(panel[auxI][j] > 0):
            ret=1
        auxI = auxI-1
    return ret

def es_horizontal(panel,id):
    auxI,auxJ=busca_pos_ij(panel,id)    #i=fila  j =columna
    ret=0
    if(auxJ < len(panel[0]) -1 and panel[auxI][auxJ+1] >= 0):
        if(auxI < len(panel) and panel[auxI+1][auxJ] == -1):
           ret = 1
        if(busca_arriba(panel,auxI,auxJ) == 1):
            ret = 1
        if(ret == 0 and es_vertical(panel,id)==0):
            ret = 2
    return ret      






def classificarDiccionario(path,diccionari):
    
    for linea in open(path):
        
        palabra = []
        aux = linea.strip('\t')
        tamany = len(aux)
        for code in bytearray(aux):
            if (code != 10): palabra.append(code)
        
        diccionari[tamany-1].append(np.array(palabra,dtype=np.int8) )
    return palabra



    
if __name__ == '__main__':
    #crossword_CB.txt
    #diccionari_CB.txt
    crossword = "crossword_CB.txt"
    print crossword
    diccionari = "diccionari_CB.txt"
    print diccionari
    print 
    aux = []
    aux2 = leer_panel(crossword)
    print_panel(aux2)
    panel = []
    for j in range(0,(len(aux2))):
        
        aux = aux2[j].split()
        aux = np.array(aux,dtype=(np.unicode_,16)) 
        aux[aux=="#"] = "-1"                        
        panel.append(aux)

    panel = np.array(panel,dtype=np.int8)            
    
    dicci = {}
    for i in range(2,16):
        dicci[i] = []
    hola = classificarDiccionario(diccionari,dicci)
    
    
    numeroAProbar = 2
    print(numeroAProbar,"Es Horizontal",es_horizontal(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
