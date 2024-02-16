"""
Mini Proyecto Procesos y Diseños de Software
Grupo:
* Willian Chapid Tobar
* Daniel Vasquez Murillo
* Miguel Angel Nivia Ortega

Contexto:
La empresa Olimpica necesita registrar sus ventas en un portal/app, la cual almacene la información en una base de datos. 
Requiere también poder visualizar al finalizar el día un reporte de las ventas del mismo. 
"""

import sqlite3

# Primero ejectuamos conexion con la base de dato, debe existir y sino entonces se crea.
conexion = sqlite3.connect("dataOlimpica.db")
# Luego se necesita un cursor para navegar en la base de datos.
cursor = conexion.cursor()
# Se crea inicialmente la tablas necesarias.

def inicioSesion():
    cursor.execute("CREATE TABLE IF NOT EXISTS ROLES (id_R INTEGER PRIMARY KEY, Nombre TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS (CC INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, id_R)")
    cursor.execute("CREATE TABLE IF NOT EXISTS PRODUCTOS (id_Prod INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Cantidad INTEGER, Precio_$ INTEGER)")
    # Roles default
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (1, 'Administrador')")
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (2, 'Vendedor')")
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (3, 'Cliente')")
    # Agregacion Del Administrador
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1245711933, 'Mike Ross', 1)")
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1225700032, 'Ana Maria', 2)")
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1003314411, 'Mauricio Torres', 3)")
    # cursor.execute("DELETE FROM PRODUCTOS")
    # Guardamos cualquier dato modificado.
    conexion.commit()
    return 0

# Funcion para seguridad del sistema.
def login(): ########################## Chapid
    # Agregar que si no existe el usuario, que se agregue.
    identificacion = str(input("Quien eres? Escribe tu nombre: "))
    return identificacion

# Funcion para tener las funcionalidades basicas respectivo a la base de datos sqlit3.
def funcionalidades(entrada):
    conexion = sqlite3.connect("dataOlimpica.db")
    cursor = conexion.cursor()
    if entrada == 1: # Agregar Productos
        print("Complete el siguiente formato sobre el producto a ingresar:")
        id_Prod = int(input("Id: "))
        cantidad = int(input("Cantidad: "))
        nombreP = str(input("Nombre: "))
        precio = int(input("Precio: "))
        try:
            cursor.execute(f"INSERT INTO PRODUCTOS VALUES ({id_Prod}, '{nombreP}',{cantidad}, {precio})")
            conexion.commit()
            print("\nAgregado Exitosamente")
        except sqlite3.IntegrityError:
            print("\nError: El ID proporcionado ya existe en la base de datos.")

    elif entrada == 2: # Eliminar productos.
        dato = input("Nombre o id del producto a eliminar: ")
        try:
            dato = int(dato)
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE id_Prod = {dato}")
        except ValueError:
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE Nombre = '{dato}'")
        conexion.commit()
        print("Producto Eliminado Exitosamente")

    elif entrada == 3: # Modificar productos.
        print("\nQue desea cambiar: \n (1) Cantidad De Producto\n (2) Precio De Producto")
        cambio = int(input("Opcion: "))
        if cambio == 1:
            nombreP = str(input("\nNombre del producto a cambiar: "))
            nuevaCantidad = int(input("Nueva Cantidad: "))
            cursor.execute(f"UPDATE PRODUCTOS SET Cantidad = {nuevaCantidad} WHERE Nombre = '{nombreP}'")
        else:
            nombreP = str(input("\nNombre del producto a cambiar: "))
            nuevoPrecio = int(input("Nuevo Precio: "))
            cursor.execute(f"UPDATE PRODUCTOS SET Precio_$ = {nuevoPrecio} WHERE Nombre = '{nombreP}'")
        conexion.commit()
        print("Dato Modificado Exitosamente")

    elif entrada == 4: # Consulta de producto.
        nombreP = str(input("Nombre del producto a buscar: "))
        cursor.execute(f"SELECT * FROM PRODUCTOS WHERE Nombre = '{nombreP}'")
        busqueda = cursor.fetchone()
        if busqueda:
            id, Nombre, Cantidad, Precio = busqueda
            print(f"\nid: {id}, Nombre: {Nombre}, Cantidad: {Cantidad}, Precio: {Precio}")
        else:
            print("\nError, producto no encontrado.")

    ##################### Vasquez
            
    elif entrada == 5: # Agregar Vendedor
        print("Aca se vende tamal")

    elif entrada == 6: # Agregar Cliente
        print("Aca se vende pan")

    elif entrada == 7: # Generar Venta
        print("Aca se vende mariscos")

    else:
        print("\nError, entrada no aceptada, vuelva a intentarlo.")
    conexion.close()
    return 0

# Funcion principal que imprime y muestra resultados respecto a los productos en la base de datos.
def main():
    inicioSesion()
    print(".--------------------------------------------------------------------.")
    print("|---------------Bienvenido Al Sistema Tec De Olimpica----------------|")
    print("|--------------------------------------------------------------------|")
    print("|-------------------------___------------___-------------------------|")
    print("|------------------------|---|----------|---|------------------------|")
    print("|------------------------|___|---__|----|___|------------------------|")
    print("|-------------------------------|-----------_------------------------|")
    print("|-------------------------------------______|------------------------|")
    print("|--------------------------------------------------------------------|")
    print("°--------------------------------------------------------------------°")
    print()
    # Aqui deberia haber un login antes de ingresar.
    # return 0
    print("En este sistema podras, agregar, eliminar y modificar datos respectivos al inventario del supermercado")
    identificacion = login()
    cursor.execute(f"SELECT * FROM USUARIOS WHERE Nombre = '{identificacion}'")
    info = cursor.fetchone()
    CC, Nombre, id_R = info
    flag = True
    while flag:
        # Aqui deberia ir un entrada respecto al login que se hizo para saber que puede salir en pantalla o no.
        if id_R == 1:  # Administrador
            print("\n-----------Bienvenido Jefe-----------")
            print("Que desea hacer:\n (1) Agregar Producto\n (2) Eliminar Producto\n (3) Modificar Producto\n (4) Consultar Producto\n (5) Agregar Vendedor\n (6) Agregar Cliente\n (0) Salir")
            entrada = int(input("Opcion: "))
        elif id_R == 2:  # Vendedor
            print("\n-----------Bienvenido Vendedor-----------")
            print("\nQue desea hacer:\n (3) Modificar Producto\n (4) Consultar Producto\n (6) Agregar Cliente\n (7) Generar Venta\n (0) Salir")
            entrada = int(input("Opcion: "))
        else:   # Cliente
            print("**Error, Permiso Denegado**")
            flag = False
        if flag == True:
            if entrada != 0 and flag == True:
                funcionalidades(entrada)
            else:
                flag = False        
    print("Muchas Gracias Por Usar El Sistema, Hasta Pronto!")
    # Se cierra la base de datos.
    conexion.close()
    return 0

main()