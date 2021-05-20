"""
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
        print(f"\nTiempo de ejecución: {time_2-time_1}\n")


    else:
        sys.exit(0)
sys.exit(0)
