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

"""def buscarChoque(panel):
    diccChoques = {}
    
    return diccChoques"""




def classificarDiccionario(path,diccionari):
    
    for linea in open(path):
        
        palabra = []
        aux = linea.strip('\t')
        aux = linea.strip('\n')
        tamany = len(aux)
        for code in bytearray(aux):
            #if (code != 10): 
            palabra.append(code)
        
        
        #diccionari[tamany-1].append(np.array(palabra,dtype=np.int8) )
        palabra2 = np.asarray(palabra,dtype=np.int8)
        #palabra2 = np.reshape(palabra2,(-1,tamany))
        #palabra2.reshape(tamany-1,1)
        diccionari[tamany] = np.append(diccionari[tamany], palabra2)
        diccionari[tamany] = np.reshape(diccionari[tamany], (-1,tamany))
        #np.ndarray.reshape()
    return palabra2














def Domini(palabra,d):
    #o mirar una variable que tiene la info
    return d[palabra.size()]
    


#inicializar lva con 0
def SatisfaRestriccions(dic,lva,pos):
    #dic lista palabras
    #lva tiene posi
    #lva[pos][i[][(lva==i )]]
    #cruz = lva[pos][lva!=0]
    #for i in cruzpos:
    #    dic[:][i==cruzvalor]
    
    
    cruzpos = lva[pos][:].nonzero()
    #cruzvalor = lva[pos][cruzpos]
    if (np.any(dic[:][cruzpos==lva[pos][cruzpos]]) == True):
        return True
    return False
    
    #
def Insertar(palabra,lva,pos):
    lva[pos] = palabra
    #tratar cruzes, tener un diccionario donde cada pos es una lista con nombre de id del juego
    #y luego cada valor es pos 0 id choque y pos 1 posicion palabra. diccionario ya tendrai que estar rellenado
     
    
    
#def BorrarFront(lvna):
    
    
#lvna lista
#var[0] por ahora es numero de palabra
    
def Backtracking(lva, lvna, d):
    if lvna.size() == 0: return(lva)
    var=lvna[0]
    lvna[0] = np.delete(lvna,0)
    for i in Domini(var,d):
        if SatisfaRestriccions(i,lva,var[0]):
            res=Backtracking(Insertar(i,lva,var[0]),lvna,d)
            #if np.any(res[:][:].nonzero()) != false:
            if lvna.size() == 0:
                return res
    return 0






    
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
    
    """for i in range(panelID[1:][0]):
        diccChoque[i] = buscarChoque(panel,i); #panel choque devuelve un"""
    
    dicci = {}
    
    for i in range(2,16):
        dicci[i] = np.array([],dtype=np.int8)  
        #np.ndarray.
    hola = classificarDiccionario(diccionari,dicci)
    
    numeroAProbar = 4
    print
    print(numeroAProbar,"Es Horizontal",es_horizontal(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
    print 
    print(numeroAProbar,"Longitud:",len_palabra(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
    print
    print ("----------Tabla IDS----------")
    print("  id#posI#posJ#esHoriz#tamaño#")
    print(tabla_ids(panel))
    
    #numeroAProbar = 2
    #print(numeroAProbar,"Es Horizontal",es_horizontal(panel,numeroAProbar)) #0 es vertical, 1 horizontal y 2 ambos
    
    
    

    
    
    
    
    
"""
    Funcio Backtracking(LVA,LVNA,R,D)
        Si (LVNA és buida) llavors Retornar(LVA) fSi
        Var=Cap(LVNA);
        Per a cada (valor del Domini(Var, D) que podem assignar a Var) fer
            Si (SatisfaRestriccions([Var valor],LVA,R)) llavors
                Res=Backtracking(Insertar([Var, valor],LVA),Cua(LVNA),R,D);
                Si (Res és una solució completa)  llavors 
                    Retornar(Res);
                Fsi
            Fsi
        Fper
        Retornar(Falla)
    FFuncio
    

    
SatisfaRestriccions(, ,) g g A,LVA,R): Retorna cert si l’assignació A afegida la llista
d’assignacions LVA satisfan les restriccions R.

Domini(V,D): Retorna un valor del domini D per a la variable V.

Insertar(e,L):Retorna la llista resultant d’afegir e al principi de L.

Cua(L) i Cap(L): Retornen la cua i el cap de L, respectivament.
    """
    
