import sqlite3
from datetime import datetime
from typing import Union

class Comunicacion():
	def __init__(self):
		self.conexion = sqlite3.connect("dataOlimpica.db")

	def inicio_sesion(self) -> None:
		cursor = self.conexion.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS LOGSISTEMA (fecha TIMESTAMP, mensaje TEXT)")
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
		cursor.execute("INSERT OR IGNORE INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('PAPA', 40, 450)")
		cursor.execute("INSERT OR IGNORE INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('ZANAHORIA', 20, 500)")
		cursor.execute("INSERT OR IGNORE INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('BANANO', 25, 600)")
		cursor.execute("INSERT OR IGNORE INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('TOMATE', 32, 300)")
		cursor.execute("INSERT OR IGNORE INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('CEBOLLA', 27, 550)")
	    # Clientes concurrentes
		cursor.execute("INSERT OR IGNORE INTO CLIENTES VALUES (1004534696, 'Willian', 7100)")
		self.conexion.commit()

	# funcion para llevar el log de las acciones hechas por el administrador
	def registrar_cambio(self, mensaje:str) -> None:
		cursor = self.conexion.cursor()
		fecha = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
		cursor.execute(f"INSERT INTO LOGSISTEMA (fecha, mensaje) values ({fecha},'{mensaje}'')")
		
	# funciones para administrar productos
	def nuevo_producto(self,user:str, producto:str, cantidad:int, precio: int) -> bool:
		ans  = False
		cursor = self.conexion.cursor()
		try:
			cursor.execute(f"SELECT * FROM PRODUCTOS WHERE Nombre = ('{producto}')")
			producto_existente = cursor.fetchone()
			if not producto_existente:
				cursor.execute(f"INSERT INTO PRODUCTOS (Nombre, Cantidad, Precio_$) VALUES ('{producto}',{cantidad},{precio})")
				self.registrar_cambio(f"{user} anadio{producto}, con {cantidad} unidad/s con precio {precio} a productos")
				ans = True
			else:
				self.registrar_cambio(f"{user} intento anadir {producto}, con {cantidad} unidad/s con precio {precio}  a productos pero ya existia en la base de datos")
		except sqlite3.IntegryError:
			self.registrar_cambio(f"{user} intento anadir {producto}, con {cantidad} unidad/s con precio {precio}  a productos")
		return ans

	def eliminar_producto(self, user: str, identificador: Union[int, str]) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		if isinstance(identificador, int):
			try:
				info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = {identificador}")
				cursor.execute(f"DELETE FROM PRODUCTOS WHERE id_Prod = {identificador}")
				self.registrar_cambio(f"{user} elimino el producto {info[1]} con id {0}, cantidad: {info[2]}, precio{info[3]} ")			
				ans = True
			except:
				self.registrar_cambio(f"{user} intento eliminar el producto con id {identificador}")
		elif isinstance(identificador, str):
			try:
				info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE nombre = {identificador}")
				cursor.execute(f"DELETE FROM PRODUCTOS WHERE nombre = {identificador}")
				self.registrar_cambio(f"{user} elimino el producto {info[1]} con id {info[0]}, cantidad: {info[2]}, precio{info[3]} ")
				ans = True
			except:
				self.registrar_cambio(f"{user} intento eliminar el producto con nombre {identificador}")
		self.conexion.commit()
		return ans

	def modificar_producto(self, user:str, identificador:Union[int,str], **kwargs) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		def actualizar_cantidad(self, nueva_cantidad:int, identificador:Union[int, str]) -> None:
			if isinstance(identificador,int):
				try:
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = {identificador}")
					cursor.execute(f"UPDATE PRODUCTOS SET cantidad = {nueva_cantidad} WHERE id_Prod = {identificador}")
					self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su cantidad paso de {info[2]} a {nueva_cantidad}")			
					ans = True
				except:
					self.registrar_cambio(f"{user} intento actualizar la cantidad del  producto con id {identificador}")
			elif isinstance(identificador, str):
				try:
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE nombre = {identificador}")
					cursor.execute(f"UPDATE  PRODUCTOS SET cantidad = {nueva_cantidad} WHERE nombre = {identificador}")
					self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su cantidad paso de {info[2]} a {nueva_cantidad}")	
					ans = True
				except:
					self.registrar_cambio(f"{user} intento actualizar la cantidad del producto con nombre {identificador}")
		
		def actualizar_precio(nueva_cantidad:int, identificador:Union[int, str]) -> None:
			if isinstance(identificador,int):
				try:
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = {identificador}")
					cursor.execute(f"UPDATE PRODUCTOS SET Precio_$ = {nueva_cantidad} WHERE id_Prod = {identificador}")
					self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su precio paso de {info[3]} a {nueva_cantidad}")			
					ans = True
				except:
					self.registrar_cambio(f"{user} intento actualizar el precio del  producto con id {identificador}")
			elif isinstance(identificador, str):
				try:
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE nombre = {identificador}")
					cursor.execute(f"UPDATE  PRODUCTOS SET Precio_$ = {nueva_cantidad} WHERE nombre = {identificador}")
					self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su precio paso de {info[3]} a {nueva_cantidad}")	
					ans = True
				except:
					self.registrar_cambio(f"{user} intento actualizar el precio del  producto con nombre {identificador}")
		def actualizar_nombre(nuevo_nombre:str, identificador:Union[int, str]) -> bool:
			ans = False
			if isinstance(identificador,int):
				try:
					cursor.execute(f"SELECT * FROM PRODUCTOS WHERE Nombre = ('{nuevo_nombre}')")
					producto_existente = cursor.fetchone()
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = {identificador}")
					if not producto_existente:
						cursor.execute(f"UPDATE PRODUCTOS SET Nombre = {nuevo_nombre} WHERE id_Prod = {identificador}")
						self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su nombre paso de {info[1]} a {nuevo_nombre}")			
						ans = True
					else:
						self.registrar_cambio(f"{user}, intento actualizar el producto {info[0]} con nombre {info[1]} por el nombre de un producto ya existente"
							"{producto_existente[1]}")
				except:
					self.registrar_cambio(f"{user} intento actualizar el nombre del  producto con id {identificador}")
			elif isinstance(identificador, str):
				try:
					cursor.execute(f"SELECT * FROM PRODUCTOS WHERE Nombre = ('{nuevo_nombre}')")
					producto_existente = cursor.fetchone()
					info = cursor.execute(f"SELECT * FROM PRODUCTOS WHERE nombre = {identificador}")
					if not producto_existente:
						cursor.execute(f"UPDATE  PRODUCTOS SET nombre = {nuevo_nombre} WHERE nombre = {identificador}")
						self.registrar_cambio(f"{user} actualizo el producto {info[1]} id {info[0]}. Su nombre paso de {info[1]} a {nuevo_nombre}")	
						ans = True
					else:
						self.registrar_cambio(f"{user}, intento actualizar el producto {info[0]} con nombre {info[1]} por el nombre de un producto ya existente"
							"{producto_existente[1]}")
				except:
					self.registrar_cambio(f"{user} intento actualizar el nombre del  producto con nombre {identificador}")
		if 'cantidad' in kwargs:
			actualizar_cantidad(kwargs['cantidad'])
		elif 'precio' in kwargs:
			actualizar_precio(kwargs['precio'])
		elif 'nombre' in kwargs:
			actualizar_nombre(kwargs['nombre'])
		self.conexion.commit()
		return ans

	def consulta_producto(self, identificador:Union[str,int]) -> tuple:
		ans = tuple()
		cursor = self.conexion.cursor()
		if isinstance(identificador,int):
			try:
				cursor.execute(f"SELECT * FROM PRODUCTOS WHERE id_Prod = '{identificador}")
				busqueda = cursor.fetchone()
				ans = busqueda
			except:
				ans = tuple()
		elif isinstance(identificador, str):
			try:
				cursor.execute(f"SELECT * FROM PRODUCTOS WHERE nombre = '{identificador}")
				ans = cursor.fetchone()
			except:
				ans = tuple()
		return ans
	
	def consultar_productos(self) -> list:
		ans = None
		cursor = self.conexion.cursor()
		cursor.execute("SELECT * FROM PRODUCTOS")
		ans = cursor.fetchall()
		return ans

	#funciones para administrar usuarios
	def agregar_vendedor(self, user:str, cc:int, nombre: str, contrasenia: str) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		try:
			cursor.execute(f"INSERT INTO USUARIOS VALUES ({cc},{contrasenia},{nombre},{2})")
			self.registrar_cambio(f"{user}, agrego a vendedores a {nombre} con documento {cc}")
			ans = True
		except sqlite3.IntegryError:
			self.registrar_cambio(f"{user} intento agregar a vendedores a {nombre} con documento {cc}")
		self.conexion.commit()
		return ans

	def eliminar_vendedor(self, user:str, identificador: Union[int, str]) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		if isinstance(identificador, int):
			try:
				cursor.execute(f"SELECT * FROM USUARIOS WHERE CC = '{identificador}'")
				info = cursor.fetchone()
				cursor.execute(f"DELETE FROM USUARIOS WHERE CC = '{identificador}'")
				self.registrar_cambio(f"{user} elimino al vendedor con id {identificador} de nombre i{info[2]}")
				ans = True
			except:
				self.registrar_cambio(f"{user} intento eliminar a un vendedor con id '{identificador}'")
		elif isinstance(identificador, str):
			try:
				cursor.execute(f"SELECT * FROM USUARIOS WHERE Nombre = '{identificador}'")
				info = cursor.fetchone()
				cursor.execute(f"DELETE FROM USUARIOS WHERE Nombre = '{identificador}'")
				self.registrar_cambio(f"{user} elimino al vendedor con nombre {identificador} de id i{info[0]}")
				ans = True
			except:
				self.registrar_cambio(f"{user} intento eliminar a un vendedor con nombre  {identificador}")
		self.conexion.commit()
		return ans

	def modificar_vendedor(self, user:str, identificador:int, **kwargs) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		def modificar_rango(nuevo_rango):
			try:
				cursor.execute(f"SELECT * FROM USUARIOS WHERE CC = '{identificador}")
				info = cursor.fetchone()
				cursor.execute(f"UPDATE  USUARIOS SET id_R = '{nuevo_rango}' where CC = {id}")
				self.registrar_cambio(f'{user} actualizo el rango del vendedor {info[2]} de rango {info[3]} a {nuevo_rango} ')
				ans = True
			except:
				self.registrar_cambio(f"{user} intento actualizar el rango del vendedor {identificador}")

		def modificar_contrasenia(nueva_contrasenia):
			try:
				cursor.execute(f"SELECT * FROM USUARIOS WHERE CC = '{identificador}")
				info = cursor.fetchone()
				cursor.execute(f"UPDATE  USUARIOS SET Contrasena = {nueva_contrasenia} where CC = {id}")
				self.registrar_cambio(f'{user} actualizo la contrasenia del vendedor {info[2]} de  {info[1]} a {nueva_contrasenia} ')
				ans = True
			except:
				self.registrar_cambio(f"{user} intento actualizar la contrasenia del vendedor {identificador}")
		if 'rango' in kwargs:
			modificar_rango(kwargs['rango'])
		elif 'contrasenia' in kwargs:
			modificar_contrasenia(kwargs['contrasenia'])
		self.conexion.commit()
		return ans

	def consultar_usuarios(self) -> list:
		ans = None
		cursor = self.conexion.cursor()
		try:
			cursor.execute("SELECT CC,, usuarios.nombre, roles.nombre from USUARIOS, ROLES whre usuarios.id_R = roles.id_R")
			ans = cursor.fetchall()
		except:
			pass
		return ans
	#funciones con los clientes

	def agregar_cliente(self, CC:int, nombre:str) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		try:
			cursor.execute(f"INSERT INTO CLIENTES VALUES ({CC},'{nombre}',0)")
			ans = True
		except:
			pass
		self.conexion.commit()
		return ans

	def consultar_puntos_cliente(self, cc:int) -> int:
		ans = None
		cursor = self.conexion.cursor()
		try:
			cursor.execute(f"SELECT Puntos FROM CLIENTES WHERE CC = {cc}")
			ans = cursor.fetchone()
		except:
			pass
		return ans[0]

	def modificar_puntos_cliente(self, cc:int, cantidad_puntos:int) -> bool:
		ans = False
		cursor = self.conexion.cursor()
		try:
			puntos = self.consultar_puntos_cliente(cc)
			cursor.execute(f"UPDATE  CLIENTES SET Puntos = {puntos-cantidad_puntos} WHERE CC = {cc}")
			ans = True
		except:
			pass
		return ans

	def consultar_usuarios(self) -> list:
		ans = None
		cursor = self.conexion.cursor()
		try:
			cursor.execute("SELECT * from clientes")
			ans = cursor.fetchall()
		except:
			pass
		return ans

	# funciones de ventas
	def modificar_producto_venta(self, id_producto:int, cantidad:int) -> bool:
		ans = False
		cursor = self. conexion.cursor()
		try:
			cursor.execute(f"SELECT Cantidad FROM PRODUCTOS WHERE id_Prod = {id_producto}")
			producto = cursor.fetchone()
			cursor.execute(f"UPDATE PRODUCTOS SET Cantidad = {producto[2]-cantidad} WHERE id_Prod = {id_producto}")
			ans = True
		except:
			pass
		self.conexion.commit()
		return ans

	def agregar_venta(self, cc:int, fecha: str, total_venta:int )-> bool:
		ans = False
		cursor = self.conexion.cursor()
		try:
			cursor.execute(f"INSERT INTO VENTAS (CC_Cliente, Fecha, Total_$) VALUES ({cc}, '{fecha}',{total_venta}')")
			ans = True
		except:
			pass
		self.conexion.commit()
		return ans
	
	def cerrar(self) -> None:
		self.conexion.close()