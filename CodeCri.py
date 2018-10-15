# -*- coding: utf-8 -*-
"""
Practica CRI: CrossWord

Enrique Fernandez | NIU: 1456537
Daniel Romero | NIU: 1459469
Sergio Morales | NIU: 1455254
"""

#from tabulate import tabulate
import math
import numpy as np #importem la llibreria
import sys
import  time
###############################################################################
"""
                    INICIALITZACIONS, PRINTS I CONVERSIONS
"""
###############################################################################
def leer_panel(crossword):
    panel = []
    for linea in open(crossword):
        panel.append(linea.strip('\t'))
    return panel


def print_panel(panel):
    for i in range(0,len(panel)):
        for j in range(0,len(panel[i])):
            sys.stdout.write(panel[i][j])


def PanelFinal(tablaID,lva,mapa):
    tablaID[:,0] = tablaID[:,0]-1
    for ID in tablaID[:,0]:
        tamany = tablaID[ID,4]
        i = tablaID[ID,1]
        j = tablaID[ID,2]
        horizontal = tablaID[ID,3]
        if horizontal == 0:
            for pos in range(0,tamany):
                mapa[i+pos,j] = lva[ID+1][0,pos]
        else:
            for pos in range(0,tamany):
                mapa[i,j+pos] = lva[ID+1][0,pos]
    tablaID[:,0] = tablaID[:,0]+1
    return mapa


def print_panel_final(panel):
    print('\n'.join(['\t'.join(['{:4}'.format(item) for item in row])
      for row in panel]))


def StringToInt8(panel_raw):
    linea = []
    panel = []
    for j in range(0,(len(panel_raw))):
        linea = panel_raw[j].split()
        linea = np.array(linea,dtype=(np.unicode_,16))
        linea[linea=="#"] = "-1"
        panel.append(linea)
    panel = np.array(panel,dtype=np.int8)
    return panel


def Int8ToString(panel_raw):
    linea = []
    panel = []
    for j in range(0,(len(panel_raw))):
        linea = panel_raw[j]
        linea[linea==-1] = 35
        linea=linea.tostring().decode("ascii")
        linea = list(linea)
        panel.append(linea)
    return panel


def inicializarLVNA_LVA(tablaID):
    LVNA = np.array([],dtype=np.int8)
    LVA = {}
    for ID in tablaID[:,0]:
        LVA[ID] = np.zeros(tablaID[ID-1,4],dtype=np.int8)
        LVA[ID] = np.reshape(LVA[ID], (-1,tablaID[ID-1,4]))
        ld = diccChoque[ID]
        ch = ld.shape
        lineaa =  np.array([ID,ch[0]],dtype=np.int8)
        LVNA = np.append(LVNA, lineaa)
        LVNA = np.reshape(LVNA, (-1,2))
    LVNA[::-1] = LVNA[LVNA[:,1].argsort(kind='quicksort')]
    return LVNA,LVA


def create_da(tabla_ids,dicci):
    da={}
    for elem in tabla_ids:
        da[elem[0]]=dicci[elem[4]]
    return da








###############################################################################
"""
            RECONEIXEMENT DE LES PARAULES AL TAULELL I CLASSIFICACIO
"""
###############################################################################
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



#0 es vertical, 1 horizontal y 2 ambos
###########id###pos i###posj###esHoriz(0=si,1=no)###tamaño########
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


def classificarDiccionario(path):
    diccionari = {}
    for i in range(2,18):
        diccionari[i] = np.array([],dtype=np.int8)
    for linea in open(path):
        palabra = []
        aux = linea.replace('\r','')
        aux = aux.replace('\t','')
        #aux = aux.strip('\r')
        aux = aux.replace('\n','')
        tamany = len(aux)
        for code in bytearray(aux):
            palabra.append(code)
        palabra2 = np.asarray(palabra,dtype=np.int8)
        diccionari[tamany] = np.append(diccionari[tamany], palabra2)
        diccionari[tamany] = np.reshape(diccionari[tamany], (-1,tamany))
    return diccionari


#j columnas, i filas
def buscarChoque(panel,tablaID):
    diccChoques = {}
    tablaID[:,0] = tablaID[:,0]-1
    for ID in tablaID[:,0]:
        diccChoques[ID+1] = np.array([],dtype=np.int8)
        posI = tablaID[ID,1]
        posJ = tablaID[ID,2]
        tamany = tablaID[ID,4]
        if tablaID[ID,3] == 0:
            for pos in range(posI,posI+tamany):
                for ID2 in tablaID[:,0]:
                    if ID != ID2:
                        posI2 = tablaID[ID2,1]
                        posJ2 = tablaID[ID2,2]
                        tamany2 = tablaID[ID2,4]
                        if tablaID[ID2,3] == 1:
                            for pos2 in range(posJ2,posJ2+tamany2):
                                if posI2==pos:
                                    if pos2==posJ:
                                        array = np.array([pos-posI,ID2+1,pos2-posJ2],dtype=np.int8)
                                        diccChoques[ID+1] = np.append(diccChoques[ID+1], array)
                                        diccChoques[ID+1] = np.reshape(diccChoques[ID+1], (-1,3))
        else:
            for pos in range(posJ,posJ+tamany):
                for ID2 in tablaID[:,0]:
                    if ID != ID2:
                        posI2 = tablaID[ID2,1]
                        posJ2 = tablaID[ID2,2]
                        tamany2 = tablaID[ID2,4]
                        if tablaID[ID2,3] == 0:
                            for pos2 in range(posI2,posI2+tamany2):
                                if posJ2==pos:
                                    if pos2==posI:
                                        array = np.array([pos-posJ,ID2+1,pos2-posI2],dtype=np.int8)
                                        diccChoques[ID+1] = np.append(diccChoques[ID+1], array)
                                        diccChoques[ID+1] = np.reshape(diccChoques[ID+1], (-1,3))
    tablaID[:,0] = tablaID[:,0]+1
    return diccChoques











###############################################################################
"""
                                BACKTRACKING
"""
###############################################################################
def Domini(palabra,d):
    return d[len(palabra[0])]


def SatisfaRestriccions(palabra,lva,pos,diccChoque):
    li = diccChoque[pos]
    for p in range(len(li[:,0])):
        if np.any(lva[li[p,1]][0,:]) != 0:
            if lva[pos][0,li[p,0]] != 0:
                if palabra[li[p,0]] != lva[pos][0,li[p,0]]:
                    return False
    return True


def Insertar(palabra,lva, lvna,pos,diccChoque):
    li = diccChoque[pos]
    lva[pos] = palabra
    lva[pos] = np.reshape(lva[pos], (-1,palabra.shape[0]))
    for i in range(0,li.shape[0]):
        if li[i,1] in lvna[:,0]:
            lva[li[i,1]][0,li[i,2]] = lva[pos][0,li[i,0]]
        else:
            lva[pos][0,li[i,0]] = lva[li[i,1]][0,li[i,2]]
    return lva


#lvna columna 1 id, columna 2 choques
def Backtracking(lva, lvna, d, diccChoque,r):
    if lvna.size == 0 or r == 1:
        r=1
        return lva,r
    var=lvna[0]
    for i in Domini(lva[var[0]],d):
        if SatisfaRestriccions(i,lva,var[0],diccChoque):
            if var[0] == lvna[0,0]:
                lvna = np.delete(lvna,0,0)
            lva,r=Backtracking(Insertar(i,lva, lvna,var[0],diccChoque),lvna,d, diccChoque,r)
            if lvna.size == 0 or r == 1:
                r=1
                return lva,r
            Insertar(np.zeros(lva[var[0]].shape[1],dtype=np.int8),lva, lvna,var[0],diccChoque)
    return lva,r











###############################################################################
"""
                       BACKTRACKING FORWARD CHECKING
"""
###############################################################################

def DominiFW(palabra,d):
    return d[len(palabra[0])]


def ActualizarDominio(palabra,lva,pos,da, diccChoque, tablaID):
    #seCumple = True
    listaChoque = diccChoque[pos[0]]
    actualiza = True
    for j in range(0,listaChoque.shape[0]):
        id_palabra2 = listaChoque[j][1]
        corte_palabra2 = listaChoque[j][2]
        tamano = tablaID[id_palabra2-1][4]
        nouDiccionari = np.array([],dtype=np.int8)
        listaDicc = da[id_palabra2]
        for i in listaDicc :
            if palabra[listaChoque[j][0]] == i[corte_palabra2]:
                nouDiccionari = np.append(nouDiccionari, i)    
        if nouDiccionari.size == 0:
            actualiza = False
            return da, actualiza
        nouDiccionari = np.reshape(nouDiccionari, (-1,tamano))
        da[id_palabra2] = nouDiccionari
    return da, actualiza


def ForwardBacktracking(lva, lvna, da, diccChoque,r, tablaID):
    if lvna.size == 0 or r == 1:
        r=1
        return lva,r
    var=lvna[0]
    for i in da[var[0]]:
        #da = {}
        da,actualiza = ActualizarDominio(i, lva, var, da, diccChoque,tablaID)
        if SatisfaRestriccions(i,lva,var[0],diccChoque) and actualiza:
                if var[0] == lvna[0,0]:
                    lvna = np.delete(lvna,0,0)
                lva,r=ForwardBacktracking(Insertar(i,lva, lvna,var[0],diccChoque),lvna,da, diccChoque,r,tablaID)
                if lvna.size == 0 or r == 1:
                    r=1
                    return lva,r
                Insertar(np.zeros(lva[var[0]].shape[1],dtype=np.int8),lva, lvna,var[0],diccChoque)
    return lva,r











###############################################################################
"""
                                    MAIN
"""
###############################################################################
if __name__ == '__main__':

    ### INICIALITZACIO ###
    temps_ini_i = time.time()
    crossword = "crossword_CB.txt"
    diccionari = "diccionari_CB.txt"
    panel_raw = leer_panel(crossword)
    panel = StringToInt8(panel_raw)
    dicci = classificarDiccionario(diccionari)
    tablaID = tabla_ids(panel)
    tablaID = np.array(tablaID,dtype=np.int8)
    diccChoque = buscarChoque(panel,tablaID)
    LVNA,LVA = inicializarLVNA_LVA(tablaID)
    da=create_da(tablaID,dicci)
    temps_ini_f = time.time()
    temps_ini = temps_ini_f - temps_ini_i


    ### PRINTS ###
    print crossword
    print diccionari
    print
    print_panel(panel_raw)
    print
    print
    print ("----------Tabla IDS----------")
    print("  id#posI#posJ#esHoriz(0=si,1=no)#tamaño#")
    print tablaID
    print


    ### PROCESS ###
    ## BACKTRACKING ##
    r=0
    temps_Backtracking_i = time.time()
    LVA,r= Backtracking(LVA,LVNA,dicci,diccChoque,r)
    #LVA,r= ForwardBacktracking(LVA,LVNA,da,diccChoque,r,tablaID)
    temps_Backtracking_f = time.time()
    temps_Backtracking = temps_Backtracking_f - temps_Backtracking_i


    ### FINAL ###
    panel = PanelFinal(tablaID,LVA,panel)
    panel = Int8ToString(panel)
    print_panel_final(panel)
    print
    print "\nInicialitzacio: %f segons." % (temps_ini)
    print "\nBacktracking: %f segons." % (temps_Backtracking)
