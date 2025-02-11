﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import time as tm
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada

ENTREGA FINAL
"""

def execute_consulta_carga(catalog):
    return controller.comunica_consulta_carga(catalog)

def view_consulta_carga_datos(tupla_info):
    LandingPoint = tupla_info[3]
    pais = tupla_info[4]
    print("\nRESULTADOS DE LA CARGA DE DATOS")
    print(f"Número de landing points registrados (# de vertices del grafo): {tupla_info[0]}")
    print(f"Número de landing points únicos registrados (# de vertices con el mismo id de LP): {tupla_info[-1]}")
    print(f"Número de conexiones registradas: {tupla_info[1]}")
    print(f"Número de paises registrados: {tupla_info[2]}")

    print("\nINFORMACIÓN DEL PRIMER LANDING POINT CARGADO")
    identificador = LandingPoint["landing_point_id"]
    nombre = LandingPoint["name"]
    latitud = LandingPoint["latitude"]
    longitud = LandingPoint["longitude"]
    print(f"Identificador: {identificador}")
    print(f"Nombre: {nombre}")
    print(f"Latitud: {latitud}")
    print(f"Longitud: {longitud}")

    print("\nINFORMACIÓN DEL ÚLTIMO PÁIS CARGADO")
    nombre_pais = pais["CountryName"]
    pop = pais["Population"]
    users = pais["Internet users"]
    print(f"Pais: {nombre_pais}")
    print(f"Población: {pop}")
    print(f"Usuarios de internet: {users}")
    return None

def view_req1(result):
    print("\nRESULTADOS REQUERIMIENTO 1")
    print(f"Cantidad de Clusters encontrados: {result[0]}")
    print(f"¿Están en el mismo Cluster?: {result[1]}")
    return None

def view_req2(result):
    
    print("\nRESULTADOS REQUERIMIENTO 2\n")
    i=1
    for LP in lt.iterator(result):
        identificador = LP['LP']
        pais = LP['country']
        num_cables = LP['num_cables']
        name = LP['name']
        print(f'Identificador landing point #{i}: {identificador}')
        print(f'Nombre: {name}')
        print(f'País: {pais}')
        i +=1
    print(f'Total de cables conectados: {num_cables}\n')
    return None

def view_req3(result):
    print("\nRESULTADOS REQUERIMIENTO 3")
    last_element = lt.lastElement(result)
    distancia_total = last_element[2]
    distancia_anterior = 0
    for lista in lt.iterator(result):
        print(f"Origen: {lista[0]}, Destino: {lista[1]}, Distancia: {lista[2]-distancia_anterior:.2f} km")
        distancia_anterior = lista[2]
    print(f"Distancia total: {distancia_total:.2f} km")
    return None

def view_req4(result):

    print("\nRESULTADOS REQUERIMIENTO 4\n")
    num_nodos = result[1]
    distance = result[2]
    vertexA_max = result[3]['vertexA']
    vertexB_max = result[3]['vertexB']
    weight_max= result[3]['weight']
    vertexA_min = result[4]['vertexA']
    vertexB_min = result[4]['vertexB']
    weight_min = result[4]['weight']
    rama_mas_larga = result[0]
    print(f'Número de nodos conectados: {num_nodos}')
    print(f'Distancia total de la red de expansión mínima: {distance:.2f} Km')
    print(f'Conexión más larga: {vertexA_max} - {vertexB_max}, distancia: {weight_max:.2f} Km')
    print(f'Conexión más corta: {vertexA_min} - {vertexB_min}, distancia: {weight_min:.2f} Km')
    print('Rama más larga de la red de expansión mínima: \n')
    for entry in lt.iterator(rama_mas_larga):
        vertexA = entry['key']
        vertexB = entry['value']
        print(f'{vertexA} - {vertexB}')

    return None

def view_req5(result):
    print("\nRESULTADOS REQUERIMIENTO 5")
    print(f"Número de paises directamente afectados por el fallo: {lt.size(result[0])}")
    i = 1
    for pais in lt.iterator(result[0]):
        print(f"{i} {pais.capitalize()}, Distancia: {lt.getElement(result[1],i):.2f} km")
        i += 1
    return None

def printMenu():
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando catálogo...")
        catalog = controller.comunica_iniciador()

    elif int(inputs[0]) == 2:
        print("Cargando los datos...")
        time_1 = tm.perf_counter()
        controller.comunica_carga_datos(catalog)
        time_2 = tm.perf_counter()
        result = execute_consulta_carga(catalog)
        view_consulta_carga_datos(result)
        print(f"\nTiempo de ejecución: {time_2-time_1}")

    elif int(inputs[0]) == 3:
        LP1 = input("Ingrese el nombre del primer Landing Point: ")
        LP2 = input("Ingrese el nombre del segundo Landing Point: ")
        print("Buscando, por favor espere...")
        time_1 = tm.perf_counter()
        result = controller.comunica_req1(catalog,LP1,LP2)
        time_2 = tm.perf_counter()
        view_req1(result)
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")

    elif int(inputs[0]) == 4:
        print("Buscando, por favor espere...")
        time_1 = tm.perf_counter()
        result = controller.comunica_req2(catalog)
        time_2 = tm.perf_counter()
        view_req2(result)
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")

    elif int(inputs[0]) == 5:
        country_1 = input("Ingrese el nombre del país A: ").lower()
        country_2 = input("Ingrese el nombre del país B: ").lower()
        time_1 = tm.perf_counter()
        result = controller.comunica_req3(catalog,country_1,country_2)
        view_req3(result)
        time_2 = tm.perf_counter()
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")

    elif int(inputs[0]) == 6:
        time_1 = tm.perf_counter()
        result = controller.comunica_req4(catalog)
        view_req4(result)
        time_2 = tm.perf_counter()
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")

    elif int(inputs[0]) == 7:
        LandingPoint = input("Ingrese el nombre del Landing Point que quiere simular como afectado: ")
        print("Calculando daños, por favor espere...")
        time_1 = tm.perf_counter()
        result = controller.comunica_req5(catalog,LandingPoint)
        time_2 = tm.perf_counter()
        view_req5(result)
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")

    else:
        sys.exit(0)
sys.exit(0)
