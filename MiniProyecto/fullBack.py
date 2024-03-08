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
    cursor.execute("CREATE TABLE IF NOT EXISTS CLIENTES (CC INTEGER PRIMARY KEY, Nombre TEXT NOT NULl, Puntos INTEGER)")
    # Roles default
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (1, 'Administrador')")
    cursor.execute("INSERT OR IGNORE INTO ROLES VALUES (2, 'Vendedor')")
    # Agregacion Del Administrador
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1245711933, 'Dorime69!', 'Mike Ross', 1)")
    cursor.execute("INSERT OR IGNORE INTO USUARIOS VALUES (1225700032, 'Jijija44$', 'Ana Maria', 2)")
    # Productos Basicos
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (1, 'Papa', 40, 450)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (2, 'Zanahoria', 20, 500)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (3, 'Banano', 25, 600)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (4, 'Tomate', 32, 300)")
    cursor.execute("INSERT OR IGNORE INTO PRODUCTOS VALUES (5, 'Cebolla', 27, 550)")
    # Clientes concurrentes
    cursor.execute("INSERT OR IGNORE INTO CLIENTES VALUES (1004534696, 'Willian', 7100)")
    # cursor.execute("DELETE FROM PRODUCTOS")
    # Guardamos cualquier dato modificado.
    conexion.commit()
    return 0

# Funcion para seguridad del sistema
def verificacion(info, op = 'No_validar', rol = 0):
    busqueda = None
    if rol == 0:
        cursor.execute(f"SELECT * FROM USUARIOS WHERE cc = '{info[0]}'and Contrasena = '{info[1]}'")
        busqueda  = cursor.fetchone()
        if op == 'validar':
            cursor.execute(f"SELECT id_R FROM ROLES WHERE Nombre = 'Administrador'")
            rol = cursor.fetchone()
            if busqueda[3] == rol[0]:
                busqueda = True
            else:
                busqueda = False
    else:
        cursor.execute(f"SELECT * FROM CLIENTES WHERE cc = '{info}'")
        busqueda  = cursor.fetchone()
    return busqueda

def mostrar_usuarios():
    cursor.execute("SELECT CC, usuarios.nombre, roles.nombre from USUARIOS, ROLES where USUARIOS.id_R = roles.id_R")
    usuarios = cursor.fetchall()
    print("Usuarios del sistema")
    encabezado = ["CC","NOMBRE","ROL"]
    print("{:<15} {:<15} {:<10}".format(*encabezado))
    for usuario in usuarios:
        print(f"{usuario[0]:<15} {usuario[1]:<15} {usuario[2]:<10}")

def mostrar_clientes():
    cursor.execute("SELECT * from clientes")
    usuarios = cursor.fetchall()
    print("Usuarios del sistema")
    encabezado = ["ID","NOMBRE","PUNTOS"]
    print("{:<15} {:<15} {:<10}".format(*encabezado))
    for usuario in usuarios:
        print(f"{usuario[0]:<15} {usuario[1]:<15} {usuario[2]:<10}")

def mostrar_productos_disponibles():
    cursor.execute("SELECT * FROM PRODUCTOS")
    productos_disponibles = cursor.fetchall()
    print(type(productos_disponibles))
    print("\nProductos Disponibles:\n")
    encabezado = ["ID","NOMBRE","CANTIDAD","PRECIO"]
    print("{:<10} {:<15} {:<10} {:<10}".format(*encabezado))
    for producto in productos_disponibles:
        print(f"{producto[0]:<10} {producto[1]:<15} {producto[2]:<10} {producto[3]:<10}")

def calculo_puntos(total):
    return (total*4)//100

def calculo_impuestos(total):
    return int(total*0.19)
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
                # rol invalido
                info = None, None, None, -1
            else:
                info = busqueda
        else:
            # no se encontro usuario
            info = None, None, None, -2
    else:
        # Sale del menu
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
        nombreV = input("Nombre: ")
        contrasena = input("Contraseña: ")
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
            nuevoRango = int(input("Nuevo Rango: "))
            cursor.execute(f"UPDATE USUARIOS SET id_R = {nuevoRango} WHERE CC = {id}")
        elif cambio == 2:
            id = str(input("\nCC del vendedor a cambiar: "))
            nuevoContra = int(input("Nueva contraseña: "))
            cursor.execute(f"UPDATE USUARIOS SET Precio_$ = {nuevoContra} WHERE CC = {id}")
        else:
            id = str(input("\nCC del vendedor a cambiar: "))
            nuevoNombre = input("Nuevo nombre: ")
            cursor.execute(f"UPDATE USUARIOS SET Nombre = '{nuevoNombre}' WHERE CC = {id}")

    elif entrada == 8: # Generar Venta y Agregar cliente si no existe
        print("\nGenerar Venta")
        cliente = ("0000000000", "None", 0)
        print("\nEl cliente desea que sus datos sean almacenados en la base de datos: \n (1) Si\n (2) No")
        cambio = int(input("Opcion: "))
        
        if cambio == 1:
            cc_cliente = int(input("Ingrese la identificación del cliente (CC): "))

            # Verificar si el cliente ya existe en la base de datos
            cliente = verificacion(cc_cliente, rol = 2)
            if not cliente:
                nombre_cliente = input("Ingrese el nombre del cliente: ")
                # Agregar cliente a la base de datos
                cursor.execute(f"INSERT INTO CLIENTES VALUES ({cc_cliente},'{nombre_cliente}', 0)")
                conexion.commit()
                cliente = verificacion(cc_cliente,rol = 2)

        # Seleccionar productos a comprar
        productos_comprados = dict()
        total_venta = 0
        bandera = 0
        while bandera == 0:
            # Mostrar productos disponibles
            if cambio == 1:
                print(f'Cliente: {cliente[1]}, puntos acumulados: {cliente[2]}')
            mostrar_productos_disponibles()
            id_producto = int(input("Ingrese el ID del producto a comprar (0 para finalizar): "))
            if id_producto == 0:
                bandera = 1
            else:
                cantidad_comprar = int(input("Ingrese la cantidad a comprar: "))

                # Verificar si hay suficiente cantidad del producto
                cursor.execute(f"SELECT Cantidad, Precio_$, nombre FROM PRODUCTOS WHERE id_Prod = {id_producto}")
                producto_seleccionado = cursor.fetchone()
                if producto_seleccionado and producto_seleccionado[0] >= cantidad_comprar:
                    total_producto = cantidad_comprar * producto_seleccionado[1]
                    total_venta += total_producto
                    if id_producto not in productos_comprados:
                        productos_comprados[id_producto] = [id_producto, cantidad_comprar, producto_seleccionado[2],total_producto]
                    else:
                        productos_comprados[id_producto][1]+=cantidad_comprar
                    # Actualizar la cantidad en la base de datos
                    nueva_cantidad = producto_seleccionado[0] - cantidad_comprar
                    cursor.execute(f"UPDATE PRODUCTOS SET Cantidad = {nueva_cantidad} WHERE id_Prod = {id_producto}")
                    conexion.commit()
                else:
                    print("Error: Cantidad insuficiente o producto no encontrado.")
        if len(productos_comprados)!=0:
            #Pago con puntos
            cantidad_puntos = 0
            if cambio ==1:
                print(f'\n\n\nCliente: {cliente[1]}, puntos acumulados: {cliente[2]}')
                print('Redimir puntos: \n(1)Si\n(2)No')
                redimir = int(input('Opcion: '))
                if redimir == 1:
                    cantidad_puntos  = -1
                    while cantidad_puntos < 0 or cantidad_puntos>cliente[2]:
                        cantidad_puntos = int(input('Digite cantidad a redimir: '))
            print('Valor Bolsa: 60')
            bolsa = int(input('Digite numero de bolsas: '))
            total_venta += bolsa*60
            iva = calculo_impuestos(total_venta)
            total_absoluto = total_venta + iva
            # Registrar la venta en la base de datos
            fecha_venta = datetime.now().date()
            cursor.execute(f"INSERT INTO VENTAS (CC_Cliente, Fecha, Total_$) VALUES ({cliente[0]}, '{fecha_venta}', {total_absoluto})")
            venta_id = cursor.lastrowid
            conexion.commit()
            # Mostrar detalles de la venta
            print("\nDetalles de la Venta:")
            print(f"ID de Venta: {venta_id}")
            print(f"Cliente: {cliente[0]}")
            print("Productos Comprados:")
            encabezado = ["ID","PRODUCTO","CANTIDAD","TOTAL PRODUCTO"]
            print("{:<5}{:<10}{:<10}{:<5}".format(*encabezado))
            for producto_comprado in productos_comprados.values():
                id_prod, cantidad_comprar,nombre, total_producto = producto_comprado
                print(f"{id_prod:<5} {nombre:<10} {cantidad_comprar:<10} {total_producto:<5}")
            print(f"ID Producto: Bolsa Cantidad: {bolsa:<5} Total:{bolsa*60:<5}")
            print(f"Total de la Venta: {total_venta}")
            print(f"Impuestos IVA 19%: {iva}")
            print(f'Total parcial: {total_absoluto}')
            print(f'Total:{total_absoluto - cantidad_puntos}')
            if cambio == 1:
                print(f'Puntos redimidos: {cantidad_puntos}')
                puntos_acumulados = calculo_puntos(total_venta)
                print(f'Puntos en esta compra: {puntos_acumulados}')
                cursor.execute(f"UPDATE CLIENTES SET puntos = {cliente[2]-cantidad_puntos+puntos_acumulados} WHERE CC = {cliente[0]}")
                conexion.commit()
                cursor.execute(f"SELECT puntos from clientes where cc = {cliente[0]}")
                puntos_totales = cursor.fetchone() 
                print(f'Puntos acumulados: {puntos_totales[0]}')
                print('Gracias por su compra!')
        else:
            print('La venta no puede ser cero')

        

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
                print("\nError, en esta fecha no se realizaron ventas.")
    elif entrada == 10 and verificacion(info, 'validar'): # mostrar listado de clientes
        mostrar_clientes()
    elif entrada == 11 and verificacion(info, 'validar'): # mostrar los usuarios del sistema
        mostrar_usuarios()
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
        print("Que desea hacer:\n (1) Agregar Producto\n (2) Eliminar Producto\n (3) Modificar Producto\n"
         "(4) Consultar Productos\n (5) Agregar Vendedor\n (6) Eliminar Vendedor\n (7) Modificar Vendedor\n"
         "(8) Generar Venta \n (9) Generar Reporte\n(10)Mostrar clientes\n(11)mostrar_usuarios\n (0) Salir")
    elif opcion == 2:
        print("\n-----------Bienvenido Vendedor-----------")
        print("\nQue desea hacer:\n (4) Consultar Productos\n (8) Generar Venta\n (0) Salir")
    else:
        print("ROL INVALIDO")
    while ans > 11 or ans < 0:
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