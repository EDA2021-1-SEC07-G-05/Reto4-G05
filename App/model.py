"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import haversine as hs
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def InitCatalog():
    catalog = {"connections":None,
               "countries":None,
               "LandingPoints": None,
               "countries_info": None,
               "cables":None}
    
    catalog["connections"] = gr.newGraph(datastructure= "ADJ_LIST", directed= False, size=14000, comparefunction= compareStopIds)
    catalog["countries"] = mp.newMap(numelements= 50, maptype="PROBING")
    catalog["LandingPoints"] = mp.newMap(numelements= 100, maptype="PROBING")
    catalog["countries_info"] = mp.newMap(numelements= 100, maptype="PROBING")
    catalog["cables"] = mp.newMap(numelements= 100, maptype="PROBING")
    return catalog

# Funciones para agregar informacion al catalogo
def carga_connections(catalog,connection):
    graph = catalog["connections"]
    mapa_paises = catalog["countries"]
    mapa_LP = catalog["LandingPoints"]
    length = connection["cable_length"]
    origin = formatOriginVertex(connection)
    destination = formatDestinationVertex(connection)
    addLandingPoint(origin, graph)
    addLandingPoint(destination,graph)
    addConnection(graph,origin,destination,length)
    addCableInMap(connection,mapa_paises,mapa_LP)
    return None

def carga_CountryAsKey(catalog,country_data):
    mapa = catalog["countries"]
    country = country_data["CountryName"].lower()
    mapa_sec = mp.newMap(numelements= 50, maptype= "PROBING", comparefunction= compareStopIds)
    entry = mp.get(mapa,country)
    if entry is None and country is not "":
        mp.put(mapa,country,mapa_sec)
    return None

def carga_LandingPointsAsKeys(catalog,LandingPointData):
    mapaOnlyLP = catalog["LandingPoints"]
    mp.put(mapaOnlyLP, LandingPointData["landing_point_id"], LandingPointData)
    mapa_1 = catalog["countries"]
    country = getCountry(LandingPointData)
    LD_id = LandingPointData["landing_point_id"]
    if country is not "":
        entry_1 = mp.get(mapa_1, country)
        mapa_2 = me.getValue(entry_1)
        entry_2 = mp.get(mapa_2, LD_id)
        if entry_2 is None:
            lista = lt.newList(datastructure= "ARRAY_LIST", cmpfunction= compareCables)
            mp.put(mapa_2, LD_id, lista)
        mp.put(mapa_1,country,mapa_2)
    return None


def connect_CableSameLP(catalog):
    grafo = catalog['connections']
    mapa_paises = catalog['countries']
    mapas_LP = mp.valueSet(mapa_paises)
    for mapa_LP in lt.iterator(mapas_LP):
        LandingPoints = mp.keySet(mapa_LP)
        for LandingPoint in lt.iterator(LandingPoints):
            entry = mp.get(mapa_LP, LandingPoint)
            list_cables = me.getValue(entry)
            i = 0
            for cable in lt.iterator(list_cables):
                if i != 0:
                    LastVertex = formatVertex(LandingPoint,anterior)
                    CurrentVertex = formatVertex(LandingPoint,cable)
                    gr.addEdge(grafo,LastVertex,CurrentVertex,100)
                anterior = cable
                i += 1
    return None

def carga_Countries_cap(catalog,pais):
    mapa = catalog["countries_info"]
    mp.put(mapa,pais["CountryName"].lower(),pais)
    return None

def carga_CablesInfo(catalog,connection):
    mapaInfoCables = catalog["cables"]
    InfoCable = formatCableInfo(connection)
    id = InfoCable["Id"]
    mp.put(mapaInfoCables,id,InfoCable)
    return None

def SortCablesList(catalog):
    mapa_paises = catalog["countries"]
    keys_mapa_paises = mp.keySet(mapa_paises)
    for pais in lt.iterator(keys_mapa_paises):
        entry_mapas_LP = mp.get(mapa_paises,pais)
        mapa_LP = me.getValue(entry_mapas_LP)
        lista_LandingPoints = mp.keySet(mapa_LP)
        for LandingPoint in lt.iterator(lista_LandingPoints):
            entry_lista_cables = mp.get(mapa_LP,LandingPoint)
            lista_cables = me.getValue(entry_lista_cables)
            sorted_list = sa.sort(lista_cables,compareBandas)
            mp.put(mapa_LP,LandingPoint,sorted_list)
        mp.put(mapa_paises,pais,mapa_LP)
    return None

def connect_capital(catalog):
    grafo = catalog["connections"]
    info_LandingPoints = catalog["LandingPoints"]
    info_paises = catalog["countries_info"]
    mapa_paises = catalog["countries"]
    paises = mp.keySet(mapa_paises)
    for pais in lt.iterator(paises):
        entry_capital = mp.get(info_paises,pais)
        entry_LandingPoints_mapa = mp.get(mapa_paises,pais)
        info_capital = me.getValue(entry_capital)
        LandingPoints_mapa = me.getValue(entry_LandingPoints_mapa)
        lat = info_capital["CapitalLatitude"]
        long = info_capital["CapitalLongitude"]
        name_capital = info_capital["CapitalName"]
        LandingPoints = mp.keySet(LandingPoints_mapa)
        for LandingPoint_individual in lt.iterator(LandingPoints):
            entry_listaCables = mp.get(LandingPoints_mapa,LandingPoint_individual)
            ListaCables = me.getValue(entry_listaCables)
            if not lt.isEmpty(ListaCables):
                cable_menor_banda = lt.lastElement(ListaCables)
                vertexCap = formatVertex(name_capital,cable_menor_banda)
                vertex = formatVertex(LandingPoint_individual,cable_menor_banda)
                gr.insertVertex(grafo,vertexCap)
                gr.addEdge(grafo,vertex,vertexCap,100)
            else:
                AllLandingPoints = mp.valueSet(info_LandingPoints)
                menor = 1E16
                for LP_in_mapa_completo in lt.iterator(AllLandingPoints):
                    LP_lat = LP_in_mapa_completo["latitude"]
                    LP_long = LP_in_mapa_completo["longitude"]
                    distance = hs.haversine((lat,long),(LP_lat,LP_long))
                    if distance < menor:
                        menor = distance
                        id_menor = LP_in_mapa_completo["landing_point_id"]
                        pais_interes = getCountry(LP_in_mapa_completo)
                entry_aux1 = mp.get(mapa_paises,pais_interes)
                mapa_aux = me.getValue(entry_aux1)
                entry_aux2 = mp.get(mapa_aux,id_menor)
                lista_aux = me.getValue(entry_aux2)
                cable_menor_banda = lt.lastElement(lista_aux)
                vertexCap = formatVertex(name_capital,cable_menor_banda)
                vertex = formatVertex(id_menor,cable_menor_banda)
                gr.insertVertex(grafo,vertexCap)
                gr.addEdge(grafo,vertex,vertexCap,100)
    return None


# Funciones para creacion de datos
def formatOriginVertex(connection):
    return connection["\ufefforigin"]+"-"+connection["cable_id"]

def formatDestinationVertex(connection):
    return connection["destination"]+"-"+connection["cable_id"]

def formatVertex(LandingPoint,Cable):
    return LandingPoint+'-'+Cable["Id"]

def formatCableInfo(connection):
    Info = {"Id": connection["cable_id"],
            "name": connection["cable_name"],
            "length": connection["cable_length"],
            "banda": connection["capacityTBPS"]}
    return Info

def addLandingPoint(vertex,graph):
    if not gr.containsVertex(graph,vertex):
        gr.insertVertex(graph,vertex)
    return None

def addConnection(graph, origin, destination, length):
    edge = gr.getEdge(graph,origin,destination)
    if edge is None:
        gr.addEdge(graph,origin,destination,length)
    return None

def getCountry(LandingPoint):
    info = LandingPoint["name"].split(", ")
    return info[-1].lower()

def addCableInMap(connection,mapa_paises,mapa_LP):
    LP_Origin = connection["\ufefforigin"]
    LP_destination = connection["destination"]
    entryO, entryD = mp.get(mapa_LP, LP_Origin), mp.get(mapa_LP, LP_destination)
    PaisO, PaisD = getCountry(me.getValue(entryO)), getCountry(me.getValue(entryD))
    entry_O1, enrty_D1 = mp.get(mapa_paises,PaisO), mp.get(mapa_paises,PaisD)
    mapa_LPO, mapa_LPD = me.getValue(entry_O1), me.getValue(enrty_D1)
    entry_O2, entry_D2 = mp.get(mapa_LPO,LP_Origin), mp.get(mapa_LPD,LP_destination)
    cablesOrigin, cablesDestination = me.getValue(entry_O2), me.getValue(entry_D2)
    lt.addLast(cablesOrigin,formatCableInfo(connection))
    lt.addLast(cablesDestination,formatCableInfo(connection))
    return None

# Funciones de consulta
def consulta_carga_datos(catalog):
    """
    Consulta las propiedades de los datos y las estructuras cargadas
    """
    grafo = catalog["connections"]
    mapa_paises= catalog["countries_info"]
    mapa_LP_info = catalog["LandingPoints"]
    FirstLDId = "3316"
    LastCountryId = "chuuk"

    LandingPoints = gr.numVertices(grafo)
    conexiones = gr.numEdges(grafo)
    paises = mp.size(mapa_paises)
    LandingPoints_unique = mp.size(mapa_LP_info)

    entry_LP = mp.get(mapa_LP_info,FirstLDId)
    entryCountry = mp.get(mapa_paises,LastCountryId)
    FirstLP = me.getValue(entry_LP)
    LastCountry = me.getValue(entryCountry)

    return (LandingPoints,conexiones,paises,FirstLP,LastCountry,LandingPoints_unique)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

#Funciones de comparación
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareCables(cable1,cable2):
    if cable1 > cable2:
        return 1
    elif cable1 < cable2:
        return -1
    else:
        return 0

def compareBandas(cable1,cable2):
    ancho_1 = cable1["banda"]
    ancho_2 = cable2["banda"]
    if ancho_1 > ancho_2:
        return 1
    elif ancho_2 > ancho_1:
        return -1
    else:
        return 0

def compareDistance(distance1,distance2):
    if distance1 > distance2:
        return 1
    elif distance1 < distance2:
        return -1
    else:
        return 0