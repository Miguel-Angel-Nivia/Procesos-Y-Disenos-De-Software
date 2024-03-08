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