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
        if(auxI < len(panel)-1 and panel[auxI+1][auxJ] == -1):
           ret = 1
        if(busca_arriba(panel,auxI,auxJ) == 1):
            ret = 1
        if(ret == 0 and es_vertical(panel,id)==0):
            ret = 2
    return ret      


def len_palabra(panel,id):
    longitud = 0
    i,j = busca_pos_ij(panel,id)
    if(es_horizontal(panel,id) == 1):
        while(j<len(panel[i]) and panel[i][j]>=0):
            longitud = longitud +1
            j = j+1
    elif(es_horizontal(panel,id) == 0):
        while(i<len(panel) and panel[i][j]>=0):
            longitud = longitud +1
            i = i+1
    return longitud


def classificarDiccionario(path,diccionari):
    
    for linea in open(path):
        
        palabra = []
        aux = linea.strip('\t')
        tamany = len(aux)
        for code in bytearray(aux):
            if (code != 10): palabra.append(code)
        
        diccionari[tamany-1].append(np.array(palabra,dtype=np.int8) )
    return palabra

###########id###pos i###posj###esHoriz###tamaño########
def tabla_ids(panel):
    tabla_ids = np.zeros((np.max(panel),5))
    maxPanel = np.max(panel)
    for id in range(1,np.max(panel)+1):
        auxLine = np.zeros(5)
        auxLine[0]=id
        auxLine[1],auxLine[2]=busca_pos_ij(panel,id)
        vh =es_horizontal(panel,id)
        if(vh == 1 or vh == 0):
            auxLine[3]=vh
            auxLine[4]=len_palabra(panel,id)
        else:
            auxLine[3]=0    #id actual vertical arbitrariamente
            i,j=0,0
            i,j=busca_pos_ij(panel,id)
            longitud=0
            while(i<len(panel) and panel[i][j]>=0):
                longitud = longitud +1
                i = i+1
            auxLine[4]=longitud
            
            auxLine2 = np.zeros(5)  #creamos un nuevo id para la palabra en horizontal
            maxPanel = maxPanel+1
            auxLine2[0]=maxPanel
            i,j=0,0
            i,j=busca_pos_ij(panel,id)
            auxLine2[1],auxLine2[2]=i,j
            auxLine2[3]=1
            longitud=0
            while(j<len(panel[i]) and panel[i][j]>=0):
                longitud = longitud +1
                j = j+1
            auxLine2[4]=longitud
            tabla_ids = np.append(tabla_ids,auxLine2)
            tabla_ids = np.reshape(tabla_ids,(-1,5))
        tabla_ids[id-1]=auxLine
    return tabla_ids

    
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
    
    #dicci = {}
    #for i in range(2,16):
     #   dicci[i] = []
    #hola = classificarDiccionario(diccionari,dicci)
    
    
    numeroAProbar = 4
    print
    print(numeroAProbar,"Es Horizontal",es_horizontal(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
    print 
    print(numeroAProbar,"Longitud:",len_palabra(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
    print
    print ("----------Tabla IDS----------")
    print("  id#posI#posJ#esHoriz#tamaño#")
    print(tabla_ids(panel))