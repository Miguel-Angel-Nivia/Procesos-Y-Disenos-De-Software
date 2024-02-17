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

# Funcion para seguridad del sistema
def verificacion(identificacion, op = 'No_validar'):
    busqueda = None
    cursor.execute(f"SELECT * FROM USUARIOS WHERE cc = '{identificacion}'")
    busqueda  = cursor.fetchone()
    print(busqueda)
    if op == 'validar':
        cursor.execute(f"SELECT id_R FROM ROLES WHERE Nombre = 'Administrador'")
        rol = cursor.fetchone()
        if busqueda[2] == rol[0]:
            busqueda = True
        else:
            busqueda = False
    return busqueda

def login():
    info = None
    print('****Digite 0 para salir****')
    identificacion = int(input("Ingrese identificacion: "))
    if identificacion != 0:
        busqueda = verificacion(identificacion)
        if busqueda:
            identificacion, nombre, id = busqueda
            if id >2 or id < 1:
                info = None, None, -1 
            else:
                info = identificacion, nombre, id
        else:
            info = None, None, -2
    else:
        info = None, None, 0
    return info


# Funcion para tener las funcionalidades basicas respectivo a la base de datos sqlit3.
def funcionalidades(entrada, identificacion):
    conexion = sqlite3.connect("dataOlimpica.db")
    cursor = conexion.cursor()
    if entrada == 1 and verificacion(identificacion, 'validar'): # Agregar Productos
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

    elif entrada == 2 and verificacion(identificacion,'validar'): # Eliminar productos.
        dato = input("Nombre o id del producto a eliminar: ")
        try:
            dato = int(dato)
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE id_Prod = {dato}")
        except ValueError:
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE Nombre = '{dato}'")
        conexion.commit()
        print("Producto Eliminado Exitosamente")

    elif entrada == 3 and verificacion(identificacion,'validar'): # Modificar productos.
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

    
def inicio():
    opcion = -1
    while opcion > 1 or opcion <0:
        print('(1) Login')
        print('(0) Salir')
        opcion = int(input('Opcion: '))
    if opcion == 1:
        identificacion, Nombre, id_R = login()
        while id_R<0:
            if id_R==-1:
                print('Usuario invalido')
            elif id_R==-2:
                print('Usuario no encontrado')
            identificacion, nombre, id_R = login()
        if id_R == 0:
            inicio()
        else:
            opcion = None
            while opcion != 0:
                if id_R ==1:
                    opcion = menu(id_R)
                elif id_R == 2:
                    opcion = menu(id_R)
                else:
                    opcion = menu()
                if opcion !=0:
                    funcionalidades(opcion, identificacion)
            inicio()
    elif opcion == 0:
        print("Muchas Gracias Por Usar El Sistema, Hasta Pronto!")

def menu(opcion = 0):
    ans = -1
    if opcion == 0:
        print("**Error, Permiso Denegado")
        ans = 0
    elif opcion == 1:
        print("\n-----------Bienvenido Jefe-----------")
        print("Que desea hacer:\n (1) Agregar Producto\n (2) Eliminar Producto\n (3) Modificar Producto\n (4) Consultar Producto\n (5) Agregar Vendedor\n (6) Agregar Cliente\n (0) Salir")
    elif opcion == 2:

        print("\n-----------Bienvenido Vendedor-----------")
        print("\nQue desea hacer:\n (3) Modificar Producto\n (4) Consultar Producto\n (6) Agregar Cliente\n (7) Generar Venta\n (0) Salir")
    else:
        print("ROL INVALIDO")
    while ans>7 or ans <0:
        ans = int(input("Opcion: "))
    return ans

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
    inicio()
    # Se cierra la base de datos.
    conexion.close()
    return 0

main()