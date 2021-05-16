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
               "countries":None}
    
    catalog["connections"] = gr.newGraph(datastructure= "ADJ_LIST", directed= True, size=14000, comparefunction= compareStopIds)
    catalog["countries"] = mp.newMap(numelements= 50, maptype="PROBING")
    return catalog

# Funciones para agregar informacion al catalogo
def carga_connections(catalog,connection):
    graph = catalog["connections"]
    length = connection["cable_length"]
    origin = formatOriginVertex(connection)
    destination = formatDestinationVertex(connection)
    addLandingPoint(origin, graph)
    addLandingPoint(destination,graph)
    addConnection(graph,origin,destination,length)
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
    mapa_1 = catalog["countries"]
    country = getCountry(LandingPointData)
    print(country)
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

# Funciones para creacion de datos
def formatOriginVertex(connection):
    return connection["\ufefforigin"]+"-"+connection["cable_id"]

def formatDestinationVertex(connection):
    return connection["destination"]+"-"+connection["cable_id"]

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

# Funciones de consulta

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