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
 """

from os import read
import tracemalloc as tr
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def comunica_iniciador():
    return model.InitCatalog()

# Funciones para la carga de datos
def comunica_carga_datos(catalog):
    file_countries = cf.data_dir + "countries.csv"
    data_countries = csv.DictReader(open(file_countries, encoding= "utf-8"), delimiter= ",")
    for country in data_countries:
        model.carga_CountryAsKey(catalog,country)
        model.carga_Countries_cap(catalog,country)

    file_LD = cf.data_dir + "landing_points.csv"
    data_LD = csv.DictReader(open(file_LD, encoding= "utf-8"), delimiter= ",")
    for LD in data_LD:
        model.carga_LandingPointsAsKeys(catalog,LD)

    file_connect = cf.data_dir + "connections.csv"
    data_connections = csv.DictReader(open(file_connect, encoding= "utf-8"), delimiter= ",")
    for connect in data_connections:
        model.carga_connections(catalog,connect)
        model.carga_CablesInfo(catalog,connect)

    model.connect_CableSameLP(catalog)
    model.SortCablesList(catalog)
    model.connect_capital(catalog)
    return None

def comunica_consulta_carga(catalog):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_carga_datos(catalog)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result

def comunica_req1(catalog,LP1,LP2):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_cantidad_clusters(catalog,LP1,LP2)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result

def comunica_req2(catalog):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_landing_points(catalog)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result

def comunica_req3(catalog,pais_1,pais_2):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_ruta_minima_paises(catalog,pais_1,pais_2)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result

def comunica_req4(catalog):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_red_expansion_minima(catalog)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result

def comunica_req5(catalog,LandingPoint_name):
    tr.start()
    start_memory = getMemory()
    result = model.consulta_paises_afectados(catalog,LandingPoint_name)
    stop_memory = getMemory()
    print(f"MEMORIA USADA: {deltaMemory(start_memory,stop_memory)}")
    tr.stop()
    return result


def getMemory():
    """
    Devuelve una 'pantallazo' de la memoria usada
    """
    return tr.take_snapshot()

def deltaMemory(star_memory, stop_memory):
    """
    Devuelve la diferencia entre dos magnitudes de memoria tomadas
    en dos diferentes instantes. Las devuelve en KB
    """
    memory_diff = stop_memory.compare_to(star_memory, 'filename')
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory /= 1024.0
    return delta_memory

