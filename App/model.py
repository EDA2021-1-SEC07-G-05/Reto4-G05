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
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def InitCatalog():
    catalog = {"connections":None,
               "connections_directed":None,
               "countries":None,
               "LandingPoints": None,
               "LandingPoints_names": None,
               "countries_info": None,
               "cables":None}
    
    catalog["connections"] = gr.newGraph(datastructure= "ADJ_LIST", directed= False, size=14000, comparefunction= compareStopIds)
    catalog["connections_directed"] = gr.newGraph(datastructure= "ADJ_LIST", directed= True, size= 14000, comparefunction= compareStopIds)
    catalog["countries"] = mp.newMap(numelements= 50, maptype="PROBING")
    catalog["LandingPoints"] = mp.newMap(numelements= 100, maptype="PROBING")
    catalog["LandingPoints_names"] = mp.newMap(numelements= 100, maptype="PROBING")
    catalog["countries_info"] = mp.newMap(numelements= 100, maptype="PROBING")
    catalog["cables"] = mp.newMap(numelements= 100, maptype="PROBING")
    return catalog

# Funciones para agregar informacion al catalogo
def carga_connections(catalog,connection):
    graph = catalog["connections"]
    graph_dirigido = catalog["connections_directed"]
    mapa_paises = catalog["countries"]
    mapa_LP = catalog["LandingPoints"]
    origin = formatOriginVertex(connection)
    destination = formatDestinationVertex(connection)
    addLandingPoint(origin, graph)
    addLandingPoint(destination,graph)
    addLandingPoint(origin, graph_dirigido)
    addLandingPoint(destination,graph_dirigido)
    length = find_distance(catalog,connection)
    addConnection(graph,origin,destination,length)
    addConnection(graph_dirigido,origin,destination,length)
    addConnection(graph_dirigido,destination,origin,length)
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
    mapaLPNames = catalog["LandingPoints_names"]
    mp.put(mapaLPNames,getName(LandingPointData),LandingPointData["landing_point_id"])
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
    grafo_dirigido = catalog["connections_directed"]
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
                    gr.addEdge(grafo,LastVertex,CurrentVertex,0.1)
                    gr.addEdge(grafo_dirigido,LastVertex,CurrentVertex,0.1)
                    gr.addEdge(grafo_dirigido,CurrentVertex,LastVertex,0.1)
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
    grafo_dirigido = catalog["connections_directed"]
    info_LandingPoints = catalog["LandingPoints"]
    info_paises = catalog["countries_info"]
    mapa_paises = catalog["countries"]
    paises = mp.keySet(mapa_paises)
    for pais in lt.iterator(paises):
        entry_capital = mp.get(info_paises,pais)
        entry_LandingPoints_mapa = mp.get(mapa_paises,pais)
        info_capital = me.getValue(entry_capital)
        LandingPoints_mapa = me.getValue(entry_LandingPoints_mapa)
        lat = float(info_capital["CapitalLatitude"])
        long = float(info_capital["CapitalLongitude"])
        name_capital = info_capital["CapitalName"]
        addCapitalLP_info(catalog,name_capital,pais)
        LandingPoints = mp.keySet(LandingPoints_mapa)
        for LandingPoint_individual in lt.iterator(LandingPoints):
            entry_listaCables = mp.get(LandingPoints_mapa,LandingPoint_individual)
            ListaCables = me.getValue(entry_listaCables)
            if not lt.isEmpty(ListaCables):
                cable_menor_banda = lt.firstElement(ListaCables)
                vertexCap = formatVertex(name_capital,cable_menor_banda)
                vertex = formatVertex(LandingPoint_individual,cable_menor_banda)
                LP_info_entry = mp.get(info_LandingPoints,LandingPoint_individual)
                LP_info = me.getValue(LP_info_entry)
                coordenadas_LP = (float(LP_info["latitude"]),float(LP_info["longitude"]))
                peso = hs.haversine((lat,long),coordenadas_LP)
                gr.insertVertex(grafo,vertexCap)
                gr.insertVertex(grafo_dirigido,vertexCap)
                gr.addEdge(grafo,vertex,vertexCap,peso)
                gr.addEdge(grafo_dirigido,vertex,vertexCap,peso)
                gr.addEdge(grafo_dirigido,vertexCap,vertex,peso)
                addCapitalLP(pais,name_capital,cable_menor_banda["Id"],mapa_paises)
            else:
                AllLandingPoints = mp.valueSet(info_LandingPoints)
                menor = 1E16
                for LP_in_mapa_completo in lt.iterator(AllLandingPoints):
                    LP_lat = float(LP_in_mapa_completo["latitude"])
                    LP_long = float(LP_in_mapa_completo["longitude"])
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
                gr.insertVertex(grafo_dirigido,vertexCap)
                gr.addEdge(grafo,vertex,vertexCap,menor)
                gr.addEdge(grafo_dirigido,vertex,vertexCap,menor)
                gr.addEdge(grafo_dirigido,vertexCap,vertex,menor)
                addCapitalLP(pais,name_capital,cable_menor_banda["Id"],mapa_paises)
    return None

def find_distance(catalog,connection):
    map = catalog["LandingPoints"]
    origin_id = connection["\ufefforigin"]
    destination_id = connection["destination"]
    origin_entry = mp.get(map,origin_id)
    dest_entry = mp.get(map,destination_id)
    origin_info = me.getValue(origin_entry)
    dest_info = me.getValue(dest_entry)
    coordinates_origin = (float(origin_info["latitude"]),float(origin_info["longitude"]))
    coordinates_dest = (float(dest_info["latitude"]),float(dest_info["longitude"]))
    peso = hs.haversine(coordinates_dest,coordinates_origin)
    return peso

def connect_capital_cables(catalog):
    mapa_conexiones = catalog["countries"]
    info_paises = catalog["countries_info"]
    grafo = catalog["connections"]
    grafo_dirigido = catalog["connections_directed"]
    lista_paises = mp.keySet(mapa_conexiones)
    for pais in lt.iterator(lista_paises):
        entry_mapLP = mp.get(mapa_conexiones,pais)
        entry_info_pais = mp.get(info_paises,pais)
        mapLP, info_pais = me.getValue(entry_mapLP), me.getValue(entry_info_pais)
        cap_name = info_pais["CapitalName"]
        entry_capital_cables_list = mp.get(mapLP,cap_name)
        capital_cables_list = me.getValue(entry_capital_cables_list)
        i = 0
        for cable in lt.iterator(capital_cables_list):
            if i != 0:
                LastVertex = formatVertex(cap_name,anterior)
                CurrentVertex = formatVertex(cap_name,cable)
                gr.addEdge(grafo,LastVertex,CurrentVertex,0.1)
                gr.addEdge(grafo_dirigido,LastVertex,CurrentVertex,0.1)
                gr.addEdge(grafo_dirigido,CurrentVertex,LastVertex,0.1)
            anterior = cable
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

def getName(LandingPoint):
    info = LandingPoint["name"].split(", ")
    return info[0]

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

def addCapitalLP(country,cap_name,cable_name,mapa_paises):
    entry_LP_map = mp.get(mapa_paises,country)
    LP_map = me.getValue(entry_LP_map)
    mp.put(LP_map,cap_name,cable_name)
    mp.put(mapa_paises,country,LP_map)
    return None

def addCapitalLP_info(catalog, cap_name, country):
    mapa_LP_info = catalog["LandingPoints"]
    mp.put(mapa_LP_info,cap_name,{"name": "default"+", "+country})
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

def consulta_cantidad_clusters(catalog,LP1_name,LP2_name):
    mismo_cluster = False
    grafo_dirigido = catalog["connections_directed"]
    mapa_paises = catalog["countries"]
    mapa_LP = catalog["LandingPoints"]
    mapa_LPNames = catalog["LandingPoints_names"]
    estructura_scc = scc.KosarajuSCC(grafo_dirigido)
    cantidad_clusters = estructura_scc["components"]

    Id_1_entry = mp.get(mapa_LPNames,LP1_name)
    Id_2_entry = mp.get(mapa_LPNames,LP2_name)
    LP1 = me.getValue(Id_1_entry)
    LP2 = me.getValue(Id_2_entry)
    entry_LP1 = mp.get(mapa_LP,LP1)
    entry_LP2 = mp.get(mapa_LP,LP2)
    LP1_info = me.getValue(entry_LP1)
    LP2_info = me.getValue(entry_LP2)
    country_LP1 = getCountry(LP1_info)
    country_LP2 = getCountry(LP2_info)
    entry_LandingPoints_mapa_1 = mp.get(mapa_paises,country_LP1)
    entry_LandingPoints_mapa_2 = mp.get(mapa_paises,country_LP2)
    LandingPoints_mapa_1 = me.getValue(entry_LandingPoints_mapa_1)
    LandingPoints_mapa_2 = me.getValue(entry_LandingPoints_mapa_2)
    entry_cables_lista_1 = mp.get(LandingPoints_mapa_1,LP1)
    entry_cables_lista_2 = mp.get(LandingPoints_mapa_2,LP2)
    cables_lista_1 = me.getValue(entry_cables_lista_1)
    cables_lista_2 = me.getValue(entry_cables_lista_2)
    cable_1 = lt.firstElement(cables_lista_1)
    cable_2 = lt.firstElement(cables_lista_2)
    vertex_1 = LP1+"-"+cable_1["Id"]
    vertex_2 = LP2+"-"+cable_2["Id"]
    estructura_dfs = dfs.DepthFirstSearch(grafo_dirigido,vertex_1)
    entry_consulta_req1 = mp.get(estructura_dfs["visited"],vertex_2)
    if entry_consulta_req1 is not None:
        mismo_cluster = True
    return cantidad_clusters, mismo_cluster

def consulta_ruta_minima_paises(catalog,pais_1,pais_2):
    grafo = catalog["connections"]
    mapa_info_paises = catalog["countries_info"]
    mapa_paises = catalog["countries"]
    entry_info_pais_1 = mp.get(mapa_info_paises,pais_1)
    entry_info_pais_2 = mp.get(mapa_info_paises,pais_2)
    info_pais_1 = me.getValue(entry_info_pais_1)
    info_pais_2 = me.getValue(entry_info_pais_2)
    cap_name_1 = info_pais_1["CapitalName"]
    cap_name_2 = info_pais_2["CapitalName"]

    entry_LP_mapa_1 = mp.get(mapa_paises,pais_1)
    entry_LP_mapa_2 = mp.get(mapa_paises,pais_2)
    LP_mapa_1 = me.getValue(entry_LP_mapa_1)
    LP_mapa_2 = me.getValue(entry_LP_mapa_2)
    entry_cable_name_1 = mp.get(LP_mapa_1,cap_name_1)
    entry_cable_name_2 = mp.get(LP_mapa_2,cap_name_2)
    cable_name_1 = me.getValue(entry_cable_name_1)
    cable_name_2 = me.getValue(entry_cable_name_2)

    vertex_1 = cap_name_1+"-"+cable_name_1
    vertex_2 = cap_name_2+"-"+cable_name_2
    estructura_dijkstra = djk.Dijkstra(grafo,vertex_1)
    ruta = ruta_encontrada(estructura_dijkstra,vertex_1,cap_name_2)
    return ruta

def ruta_encontrada(estructura,vertex_1,cap_name):
    ruta = lt.newList("SINGLE_LINKED")
    mapa_visitados = estructura["visited"]
    keys = mp.keySet(mapa_visitados)
    for key in lt.iterator(keys):
        entry = mp.get(mapa_visitados,key)
        info = me.getValue(entry)
        if cap_name in key and info["marked"] == True:
            current = key
            break
    while current != vertex_1:
        lista = [None,None,None]
        entry_info_current = mp.get(mapa_visitados,current)
        info_current = me.getValue(entry_info_current)
        lista[1] = current
        current = info_current["edgeTo"]["vertexA"]
        lista[2] = info_current["distTo"]
        lista[0] = current
        lt.addFirst(ruta,lista)
    return ruta

def consulta_paises_afectados(catalog,LandingPoint_name):
    grafo = catalog["connections"]
    mapa_names_ID = catalog["LandingPoints_names"]
    mapa_conexiones = catalog["countries"]
    mapa_LP_info = catalog["LandingPoints"]
    mapa_paises_afectados = mp.newMap(numelements=50, maptype="PROBING")

    entry_LP = mp.get(mapa_names_ID,LandingPoint_name)
    LandingPoint = me.getValue(entry_LP)
    entry_LP_info = mp.get(mapa_LP_info,LandingPoint)
    LP_info = me.getValue(entry_LP_info)
    country = getCountry(LP_info)

    entry_mapa_LP = mp.get(mapa_conexiones,country)
    mapa_LP = me.getValue(entry_mapa_LP)
    entry_lista_cables = mp.get(mapa_LP,LandingPoint)
    lista_cables = me.getValue(entry_lista_cables)

    for cable in lt.iterator(lista_cables):
        current_vertex = formatVertex(LandingPoint,cable)
        adyacentes = gr.adjacents(grafo,current_vertex)
        for vertex in lt.iterator(adyacentes):
            adyacente_LP = vertex.split("-")[0]
            entry_LP = mp.get(mapa_LP_info,adyacente_LP)
            info_LP_adyacente = me.getValue(entry_LP)
            country_afectado = getCountry(info_LP_adyacente)
            mp.put(mapa_paises_afectados,country_afectado,"default")
    lista_paises_afectados = mp.keySet(mapa_paises_afectados)
    return lista_paises_afectados
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
    ancho_1 = float(cable1["banda"])
    ancho_2 = float(cable2["banda"])
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