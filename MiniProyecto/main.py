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
from datetime import datetime
# Primero ejectuamos conexion con la base de dato, debe existir y sino entonces se crea.
conexion = sqlite3.connect("dataOlimpica.db")
# Luego se necesita un cursor para navegar en la base de datos.
cursor = conexion.cursor()
# Se crea inicialmente la tablas necesarias.

def inicioSesion():
    cursor.execute("CREATE TABLE IF NOT EXISTS VENTAS (id_Venta INTEGER PRIMARY KEY, CC_Cliente INTEGER, Fecha TEXT NOT NULL, Total_$ INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ROLES (id_R INTEGER PRIMARY KEY, Nombre TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS (CC INTEGER PRIMARY KEY,Contrasena TEXT NOT NULL, Nombre TEXT NOT NULL, id_R)")
    cursor.execute("CREATE TABLE IF NOT EXISTS PRODUCTOS (id_Prod INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Cantidad INTEGER, Precio_$ INTEGER)")
    # Roles default
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (1, 'Administrador')")
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (2, 'Vendedor')")
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (3, 'Cliente')")
    # Agregacion Del Administrador
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1245711933, 'Dorime69!', 'Mike Ross', 1)")
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1225700032, 'Jijija44$', 'Ana Maria', 2)")
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1003314411, 'None', 'Mauricio Torres', 3)")
    # Productos Basicos
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (1, 'Papa', 40, 450)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (2, 'Zanahoria', 20, 500)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (3, 'Banano', 25, 600)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (4, 'Tomate', 32, 300)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (5, 'Cebolla', 27, 550)")
    # cursor.execute("DELETE FROM PRODUCTOS")
    # Guardamos cualquier dato modificado.
    conexion.commit()
    return 0

# Funcion para seguridad del sistema
def verificacion(info, op = 'No_validar'):
    busqueda = None
    cursor.execute(f"SELECT * FROM USUARIOS WHERE cc = '{info[0]}'and Contrasena = '{info[1]}'")
    busqueda  = cursor.fetchone()
    if op == 'validar':
        cursor.execute(f"SELECT id_R FROM ROLES WHERE Nombre = 'Administrador'")
        rol = cursor.fetchone()
        if busqueda[3] == rol[0]:
            busqueda = True
        else:
            busqueda = False
    return busqueda

def verificar_cliente(identificacion, op = 'No_validar'):
    busqueda = None
    cursor.execute(f"SELECT * FROM USUARIOS WHERE cc = '{identificacion}'")
    busqueda  = cursor.fetchone()
    print(busqueda[2], )
    if op == 'validar':
        cursor.execute(f"SELECT id_R FROM ROLES WHERE Nombre = 'Cliente'")
        rol = cursor.fetchone()
        if busqueda[2] == rol[0]:
            busqueda = True
        else:
            busqueda = False
    return busqueda

def mostrar_productos_disponibles():
    cursor.execute("SELECT * FROM PRODUCTOS")
    productos_disponibles = cursor.fetchall()
    print("\nProductos Disponibles:")
    for producto in productos_disponibles:
        id_prod, nombre_prod, cantidad_prod, precio_prod = producto
        print(f"ID: {id_prod}, Nombre: {nombre_prod}, Cantidad: {cantidad_prod}, Precio: {precio_prod}")

def login():
    info = None
    print('****Digite 0 para salir****')
    identificacion = int(input("Ingrese identificacion (CC): "))
    #no se puede ocultar la contrasenia en el entorno de desarrollo
    if identificacion != 0:
        contrasena = input("Ingrese contrasenia: ")
        busqueda = verificacion((identificacion, contrasena))
        if busqueda:
            if busqueda[3] >2 or busqueda[3] < 1:
                info = None, None, None, -1
            else:
                info = busqueda
        else:
            info = None, None, None, -2
    else:
        info = None, None, None, 0
    return info


# Funcion para tener las funcionalidades basicas respectivo a la base de datos sqlit3.
def funcionalidades(entrada,info):

    conexion = sqlite3.connect("dataOlimpica.db")
    cursor = conexion.cursor()

    if entrada == 1 and verificacion(info, 'validar'): # Agregar Productos
        mostrar_productos_disponibles()
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

    elif entrada == 2 and verificacion(info,'validar'): # Eliminar productos.
        mostrar_productos_disponibles()
        dato = input("Nombre o id del producto a eliminar: ")
        try:
            dato = int(dato)
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE id_Prod = {dato}")
        except ValueError:
            cursor.execute(f"DELETE FROM PRODUCTOS WHERE Nombre = '{dato}'")
        conexion.commit()
        print("Producto Eliminado Exitosamente")

    elif entrada == 3 and verificacion(info,'validar'): # Modificar productos.
        mostrar_productos_disponibles()
        print("\nQue desea cambiar: \n (1) Cantidad del producto\n (2) Precio del producto\n (3) Nombre del producto")
        cambio = int(input("Opcion: "))
        if cambio == 1:
            id = str(input("\nID del producto a cambiar: "))
            nuevaCantidad = int(input("Nueva cantidad: "))
            cursor.execute(f"UPDATE PRODUCTOS SET Cantidad = {nuevaCantidad} WHERE id_Prod = {id}")
        elif cambio == 2:
            nombreP = str(input("\nID del producto a cambiar: "))
            nuevoPrecio = int(input("Nuevo precio: "))
            cursor.execute(f"UPDATE PRODUCTOS SET Precio_$ = {nuevoPrecio} WHERE id_Prod = {id}")
        else:
            nombreP = str(input("\nID del producto a cambiar: "))
            nuevoNombre = input("Nuevo nombre: ")
            cursor.execute(f"UPDATE PRODUCTOS SET Nombre = '{nuevoNombre}' WHERE id_Prod = {id}")

        conexion.commit()
        print("Dato Modificado Exitosamente")

    elif entrada == 4: # Consulta de producto.
        print("\nQue desea ver: \n (1) Todos los productos\n (2) Un producto")
        cambio = int(input("Opcion: "))
        if cambio == 1:
            mostrar_productos_disponibles()
        else:
            nombreP = str(input("Nombre del producto a buscar: "))
            cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = '{nombreP}'")
            busqueda = cursor.fetchone()
            if busqueda:
                id, Nombre, Cantidad, Precio = busqueda
                print(f"\nid: {id}, Nombre: {Nombre}, Cantidad: {Cantidad}, Precio: {Precio}")
            else:
                print("\nError, producto no encontrado.")
            
    elif entrada == 5 and verificacion(info,'validar'): # Agregar Vendedor
        print("Complete el siguiente formato sobre el vendedor")
        cedula = int(input("CC: "))
        nombreV = int(input("Nombre: "))
        contrasena = int(input("Contraseña: "))
        try:
            cursor.execute(f"INSERT INTO USUARIOS VALUES ({cedula}, '{contrasena}' , '{nombreV}',{2})")
            conexion.commit()
            print("\nAgregado Exitosamente")
        except sqlite3.IntegrityError:
            print("\nError: La cedula proporcionada ya existe en la base de datos.")
    
    elif entrada == 6 and verificacion(info,'validar'): # Eliminar Vendedor
        dato = input("Nombre o CC del vendedor a eliminar: ")
        try:
            dato = int(dato)
            cursor.execute(f"DELETE FROM USUARIOS WHERE CC = {dato}")
        except ValueError:
            cursor.execute(f"DELETE FROM USUARIOS WHERE Nombre = '{dato}'")
        conexion.commit()
        print("Vendedor Eliminado Exitosamente")
    
    elif entrada == 7 and verificacion(info,'validar'): # Modificar vendedor.
        print("\nQue desea cambiar: \n (1) Rango\n (2) Contraseña del vendedor\n (3) Nombre del vendedor")
        cambio = int(input("Opcion: "))
        if cambio == 1:
            id = str(input("\nCC del vendedor a cambiar: "))
            nuevaCantidad = int(input("Nuevo Rango: "))
            cursor.execute(f"UPDATE USUARIOS SET id_R = {nuevaCantidad} WHERE CC = {id}")
        elif cambio == 2:
            id = str(input("\nCC del vendedor a cambiar: "))
            nuevoPrecio = int(input("Nueva contraseña: "))
            cursor.execute(f"UPDATE USUARIOS SET Precio_$ = {nuevoPrecio} WHERE CC = {id}")
        else:
            id = str(input("\nCC del vendedor a cambiar: "))
            nuevoNombre = input("Nuevo nombre: ")
            cursor.execute(f"UPDATE USUARIOS SET Nombre = '{nuevoNombre}' WHERE CC = {id}")

    elif entrada == 8: # Generar Venta y Agregar cliente si no existe
        print("\nGenerar Venta")
        
        cc_cliente = 0000000000
        print("\nEl cliente desea que sus datos sean almacenados en la base de datos: \n (1) Si\n (2) No")
        cambio = int(input("Opcion: "))
        
        if cambio == 1:
            cc_cliente = int(input("Ingrese la identificación del cliente (CC): "))

            # Verificar si el cliente ya existe en la base de datos
            cliente_existente = verificar_cliente(cc_cliente)
            if not cliente_existente:
                nombre_cliente = input("Ingrese el nombre del cliente: ")
                # Agregar cliente a la base de datos
                cursor.execute(f"INSERT INTO USUARIOS VALUES ({cc_cliente}, '{"None"}','{nombre_cliente}', {3})")
                conexion.commit()

        # Seleccionar productos a comprar
        productos_comprados = []
        total_venta = 0
        bandera = 0
        while bandera == 0:
            # Mostrar productos disponibles
            mostrar_productos_disponibles()
            id_producto = int(input("Ingrese el ID del producto a comprar (0 para finalizar): "))
            if id_producto == 0:
                bandera = 1
            else:
                cantidad_comprar = int(input("Ingrese la cantidad a comprar: "))

                # Verificar si hay suficiente cantidad del producto
                cursor.execute(f"SELECT Cantidad, Precio_$ FROM PRODUCTOS WHERE id_Prod = {id_producto}")
                producto_seleccionado = cursor.fetchone()
                if producto_seleccionado and producto_seleccionado[0] >= cantidad_comprar:
                    total_producto = cantidad_comprar * producto_seleccionado[1]
                    total_venta += total_producto
                    productos_comprados.append((id_producto, cantidad_comprar, total_producto))
                    # Actualizar la cantidad en la base de datos
                    nueva_cantidad = producto_seleccionado[0] - cantidad_comprar
                    cursor.execute(f"UPDATE PRODUCTOS SET Cantidad = {nueva_cantidad} WHERE id_Prod = {id_producto}")
                else:
                    print("Error: Cantidad insuficiente o producto no encontrado.")

        # Registrar la venta en la base de datos
        fecha_venta = datetime.now().date()
        cursor.execute(f"INSERT INTO VENTAS (CC_Cliente, Fecha, Total_$) VALUES ({cc_cliente}, '{fecha_venta}', {total_venta})")
        venta_id = cursor.lastrowid
        conexion.commit()

        # Mostrar detalles de la venta
        print("\nDetalles de la Venta:")
        print(f"ID de Venta: {venta_id}")
        print(f"Cliente: {cc_cliente}")
        print("Productos Comprados:")
        for producto_comprado in productos_comprados:
            id_prod, cantidad_comprar, total_producto = producto_comprado
            print(f"ID Producto: {id_prod}, Cantidad: {cantidad_comprar}, Total por Producto: {total_producto}")
        print(f"Total de la Venta: {total_venta}")

    elif entrada == 9 and verificacion(info,'validar'): # Historial de ventas
        print("\nQue desea ver: \n (1) Todas las ventas\n (2) Las ventas de un dia especifico")
        cambio = int(input("Opcion: "))
        if cambio == 1:
            cursor.execute("SELECT * FROM VENTAS")
            ventas = cursor.fetchall()
            print("\nVentas:")
            for venta in ventas:
                id_venta, cc_cliente, fecha, total = venta
                print(f"ID: {id_venta}, CC cliente: {cc_cliente}, Fecha: {fecha}, Total: {total}")
        else:
            fecha = (input("Fecha que desea ver (AA-MM-DD): "))
            cursor.execute(f"SELECT * FROM VENTAS WHERE Fecha = '{fecha}'")
            ventas = cursor.fetchall()
            print("\nVentas:")
            if ventas:
                for venta in ventas:
                    id_venta, cc_cliente, fecha, total = venta
                    print(f"ID: {id_venta}, CC cliente: {cc_cliente}, Fecha: {fecha}, Total: {total}")
            else:
                print("\nError, producto no encontrado.")

    else:
        print("\nError, entrada no aceptada, vuelva a intentarlo.")
    conexion.close()
    return 0

    
def inicio():
    usuario = None
    print('(1) Login')
    print('(0) Salir')
    opcion = int(input('Opcion: '))
    while opcion == 1:
        usuario = login()
        opcion = None
        while opcion != 0:
            if usuario[3] == 1:
                opcion = menu(usuario[3])
            elif usuario[3] == 2:
                opcion = menu(usuario[3])
            else:
                opcion = menu()
            if opcion !=0:
                funcionalidades(opcion, usuario[:2])
        print('(1) Login')
        print('(0) Salir')
        opcion = int(input('Opcion: '))
    print("Muchas Gracias Por Usar El Sistema, Hasta Pronto!")

def menu(opcion = 0):
    ans = -1
    if opcion == 0:
        print("**Error, Permiso Denegado")
        ans = 0
    elif opcion == 1:
        print("\n-----------Bienvenido Jefe-----------")
        print("Que desea hacer:\n (1) Agregar Producto\n (2) Eliminar Producto\n (3) Modificar Producto\n (4) Consultar Productos\n (5) Agregar Vendedor\n (6) Eliminar Vendedor\n (7) Modificar Vendedor \n (8) Generar Venta \n (9) Generar Reporte\n (0) Salir")
    elif opcion == 2:

        print("\n-----------Bienvenido Vendedor-----------")
        print("\nQue desea hacer:\n (4) Consultar Productos\n (8) Generar Venta\n (0) Salir")
    else:
        print("ROL INVALIDO")
    while ans > 9 or ans < 0:
        ans = int(input("Opcion: "))
    return ans

# Funcion principal que imprime y muestra resultados respecto a los productos en la base de datos.
def main():
    inicioSesion()
    print(".--------------------------------------------------------------------.")
    print("|---------------Bienvenido Al Sistema Tec De Olimpica----------------|")
    print("|--------------------------------------------------------------------|")
    print("|-----------------------  ___            ___  -----------------------|")
    print("|----------------------- |   |          |   | -----------------------|")
    print("|----------------------- |___|   __|    |___| -----------------------|")
    print("|-----------------------        |__         _ -----------------------|")
    print("|-----------------------              ______| -----------------------|")
    print("|-----------------------                      -----------------------|")
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