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
from conexionSQL import Comunicacion

"""
def inicio():
    usuario = None
    print('(1) Login')
    print('(0) Salir')
    opcion = int(input('Opcion: '))
    while opcion == 1:
        usuario = Comunicacion.login()   # FALTA EL LOGIN
        opcion = None
        while opcion != 0:
            if usuario[3] == 1:
                opcion = menu(usuario[3])
            elif usuario[3] == 2:
                opcion = menu(usuario[3])
            else:
                opcion = menu()
            if opcion !=0:
                Comunicacion.funcionalidades(opcion, usuario[:2])
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
"""

# Funcion principal que imprime y muestra resultados respecto a los productos en la base de datos.
def main():
	conexion = Comunicacion()
	conexion.inicio_sesion()
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
	print("En este sistema podras, agregar, eliminar y modificar datos respectivos al inventario del supermercado")
	# inicio()
	# Se cierra la base de datos.
	conexion.cerrar()
	return 0

main()