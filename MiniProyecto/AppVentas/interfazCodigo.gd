extends Node 

var db : SQLite
var user = 0
var vista_activa
var cliente_compra
var total_compra = 0
var lista_compra = []
# Se agrego lista de la venta y el precio acumulador
var lista_venta = []
var total_acumulado = 0
var pantalla_completa = 1

func _ready():
	vista_activa = $Separador/Datos/Login
	db = SQLite.new()
	db.path = "res://data.db"
	#db.verbosity_level = SQLite.VERBOSE
	db.open_db()
	inicioSesion()
	
func mostar_funciones_disponibles(user):
	if user == 1:
		pass
	elif user == 2:
		pass
		
func inicioSesion():
	db.query("CREATE TABLE IF NOT EXISTS VENTAS (id_Venta INTEGER PRIMARY KEY, CC_Cliente INTEGER, Fecha TEXT NOT NULL, Total_$ INTEGER)")
	db.query("CREATE TABLE IF NOT EXISTS ROLES (id_R INTEGER PRIMARY KEY, Nombre TEXT NOT NULL)")
	db.query("CREATE TABLE IF NOT EXISTS EMPLEADOS (CC INTEGER PRIMARY KEY,Contrasena TEXT NOT NULL, id_R)")
	db.query("CREATE TABLE IF NOT EXISTS PRODUCTOS (id_Prod INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Cantidad INTEGER, Precio_$ INTEGER)")
	db.query("CREATE TABLE IF NOT EXISTS USUARIOS (CC INTEGER PRIMARY KEY, Nombre TEXT NOT NULl, Puntos INTEGER)")
	# Roles default
	db.query("INSERT OR IGNORE INTO ROLES VALUES (1, 'Administrador')")
	db.query("INSERT OR IGNORE INTO ROLES VALUES (2, 'Vendedor')")
	# Agregacion Del Administrador
	db.query("INSERT OR IGNORE INTO EMPLEADOS VALUES (123, '123', 1)")
	db.query("INSERT OR IGNORE INTO EMPLEADOS VALUES (321, '321', 2)")
	# Productos Basicos
	db.query("INSERT OR IGNORE INTO PRODUCTOS VALUES (1, 'PAPA', 40, 450)")
	db.query("INSERT OR IGNORE INTO PRODUCTOS VALUES (2, 'ZANAHORIA', 20, 500)")
	db.query("INSERT OR IGNORE INTO PRODUCTOS VALUES (3, 'BANANO', 25, 600)")
	db.query("INSERT OR IGNORE INTO PRODUCTOS VALUES (4, 'TOMATE', 32, 300)")
	db.query("INSERT OR IGNORE INTO PRODUCTOS VALUES (5, 'CEBOLLA', 27, 550)")
	# Clientes concurrentes
	db.query("INSERT OR IGNORE INTO USUARIOS VALUES (1004534696, 'Willian', 7100)")
	db.query("INSERT OR IGNORE INTO USUARIOS VALUES (123, 'Mike Ross', 10000)")
	db.query("INSERT OR IGNORE INTO USUARIOS VALUES (321, 'Ana Maria', 200)")
	return 0

func nuevo_producto(producto, cantidad, precio): # hacer el nombre del producto en mayusculas para no errores de escritura al buscar
		db.query("SELECT * FROM PRODUCTOS WHERE Nombre = '%s'" % producto.to_upper())
		var dato = db.query_result
		#print(dato)
		db.query("SELECT * FROM PRODUCTOS")
		var id = len(db.query_result) + 1
		if not dato:
			db.query("INSERT INTO PRODUCTOS (id_Prod, Nombre, Cantidad, Precio_$) VALUES (%d, '%s', %d, %d)" % [ int(id), producto.to_upper(), int(cantidad), int(precio)])
			$Separador/Datos/NuevoProducto/NuevoP/Label.text = "Exito"
		else:
			$Separador/Datos/NuevoProducto/NuevoP/Label.text = "Error"

func eliminar_producto(identificador):
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador))
	if db.query_result:
		db.query("DELETE FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador) )
		$Separador/Datos/EliminarProducto/EliminarP/Label.text = "Exito"
	else: 
		$Separador/Datos/EliminarProducto/EliminarP/Label.text = "Error"

func consulta_producto( identificador):
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador))
	var producto = db.query_result
	if producto:
		var hbox = HBoxContainer.new()
		var boton_producto = Button.new()
		boton_producto.text = producto[0]["Nombre"]
		hbox.add_child(boton_producto)

		var label_info = Label.new()
		var texto_info = "ID: " + str(producto[0]["id_Prod"]) + "\nCantidad: " + str(producto[0]["Cantidad"]) + "\nPrecio: $" + str(producto[0]["Precio_$"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarProductos/Producto.add_child(hbox)

func consultar_productos():
	db.query("SELECT * FROM PRODUCTOS")
	var productos = db.query_result
	for i in range(len(productos)):
		var hbox = HBoxContainer.new()
		var boton_producto = Button.new()
		boton_producto.text = productos[i]["Nombre"]
		hbox.add_child(boton_producto)

		var label_info = Label.new()
		var texto_info = "ID: " + str(productos[i]["id_Prod"]) + "\nCantidad: " + str(productos[i]["Cantidad"]) + "\nPrecio: $" + str(productos[i]["Precio_$"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarProductos/Productos/Datos.add_child(hbox)

func consultar_productos2():
	db.query("SELECT * FROM PRODUCTOS")
	var productos = db.query_result
	for i in range(len(productos)):
		var hbox = HBoxContainer.new()
		var boton_producto = Button.new()
		boton_producto.text = productos[i]["Nombre"]
		hbox.add_child(boton_producto)
		var label_info = Label.new()
		var texto_info = "ID: " + str(productos[i]["id_Prod"]) + "\nCantidad: " + str(productos[i]["Cantidad"]) + "\nPrecio: $" + str(productos[i]["Precio_$"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/RealizarVenta/Contenedor/Venta/Productos/Datos.add_child(hbox)
		boton_producto.connect("pressed", func(): _on_boton_producto_pressed(boton_producto.text))

func _on_boton_producto_pressed(nombre_producto):
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Nombre.text = str(nombre_producto)

	
func modificar_producto(identificador, nueva_cantidad):
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador))
	if db.query_result:
		db.query("UPDATE PRODUCTOS SET cantidad = %d WHERE id_Prod = %d" % [int(nueva_cantidad), int(identificador)])
		$Separador/Datos/ModificarProducto/Contenedor/Label.text = "Exito"
	
func actualizar_precio(identificador, nuevo_precio):
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador))
	if db.query_result:
		db.query("UPDATE PRODUCTOS SET Precio_$ = %d WHERE id_Prod = %d" % [int(nuevo_precio), int(identificador)])
		$Separador/Datos/ModificarProducto/Contenedor/Label.text = "Exito"

func actualizar_nombre(identificador, nuevo_nombre):
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int(identificador))
	if db.query_result:
		db.query("UPDATE PRODUCTOS SET Nombre = '%s' WHERE id_Prod = %d" % [str(nuevo_nombre).to_upper(), int(identificador)])
		$Separador/Datos/ModificarProducto/Contenedor/Label.text = "Exito"
		
func agregar_vendedor(cc, nombre, contrasenia): 
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int(cc))
	if not db.query_result:
		db.query("INSERT INTO USUARIOS VALUES (%d, '%s', %d)" %  [int(cc),str(nombre), 1000] )
		db.query("INSERT INTO EMPLEADOS VALUES (%d, '%s', %d)" %  [int(cc), str(contrasenia), 2] )
		$Separador/Datos/NuevoVendor/NuevoP/Label.text = "Exito"
	else:
		db.query("SELECT * FROM EMPLEADOS WHERE CC = %d" % int(cc))
		if not db.query_result:
			db.query("INSERT INTO EMPLEADOS VALUES (%d, '%s', '%s', %d)" %  [int(cc), str(contrasenia), str(nombre), 2] )
			$Separador/Datos/NuevoVendor/NuevoP/Label.text = "Exito"
		else:
			$Separador/Datos/NuevoVendor/NuevoP/Label.text = "Error"

func eliminar_vendedor(identificador): 
	db.query("SELECT * FROM EMPLEADOS WHERE CC = %d" % int(identificador))
	if db.query_result:
		db.query("DELETE FROM EMPLEADOS WHERE CC = %d" % int(identificador))
		$Separador/Datos/EliminarVendedor/EliminarV/Label.text = "Exito"
	else:
		$Separador/Datos/EliminarVendedor/EliminarV/Label.text = "Error"

func modificar_rango(nuevo_rango, identificador):
	db.query("SELECT * FROM EMPLEADOS WHERE CC = %d" % int(identificador))
	if db.query_result:
		db.query("UPDATE  EMPLEADOS SET id_R = %d where CC = %d" % [int(nuevo_rango) ,int(identificador)])
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Exito"
	else:
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Error"

func modificar_contrasenia(nueva_contrasena, identificador):
	db.query("SELECT * FROM EMPLEADOS WHERE CC = %d" % int(identificador))
	if db.query_result:
		db.query("UPDATE  EMPLEADOS SET Contrasena = '%s' where CC = %d" % [str(nueva_contrasena) ,int(identificador)])
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Exito"
	else:
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Error"
		
func consulta_vendedor(identificador):
	db.query("SELECT EMPLEADOS.CC, USUARIOS.Nombre, EMPLEADOS.id_R FROM EMPLEADOS, USUARIOS WHERE EMPLEADOS.id_R = 2 AND EMPLEADOS.CC = USUARIOS.CC AND EMPLEADOS.CC = %d" % int(identificador))
	var result = db.query_result
	if result and result.size() > 0 and typeof(result) == TYPE_ARRAY: # Verifica si hay resultados y asegúrate de que el resultado no esté vacío
		var hbox = HBoxContainer.new()
		var boton_vendedor = Button.new()
		boton_vendedor.text = result[0]["Nombre"]
		hbox.add_child(boton_vendedor)

		var label_info = Label.new()
		var texto_info = "CC: " + str(result[0]["CC"]) + "\nRol: " + str(result[0]["id_R"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarVendedores/Producto.add_child(hbox)
	else:
		print("No se encontró ningún vendedor con el identificador proporcionado.")


func consultar_vendedores():
	db.query("SELECT EMPLEADOS.CC, USUARIOS.Nombre, EMPLEADOS.id_R FROM EMPLEADOS, USUARIOS WHERE EMPLEADOS.id_R = 2 AND EMPLEADOS.CC = USUARIOS.CC")
	var vendedores = db.query_result
	for i in range(len(vendedores)):
		var hbox = HBoxContainer.new()
		var boton_vendedor = Button.new()
		boton_vendedor.text = vendedores[i]["Nombre"]
		hbox.add_child(boton_vendedor)

		var label_info = Label.new()
		var texto_info = "CC: " + str(vendedores[i]["CC"]) + "\nRol: " + str(vendedores[i]["id_R"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarVendedores/Productos/Datos.add_child(hbox)

func consultar_cliente(identificador):
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int(identificador))
	var cliente = db.query_result
	if cliente:
		var hbox = HBoxContainer.new()
		var boton_cliente = Button.new()
		boton_cliente.text = cliente[0]["Nombre"]
		hbox.add_child(boton_cliente)

		var label_info = Label.new()
		var texto_info = "CC: " + str(cliente[0]["CC"]) + "\nPuntos: " + str(cliente[0]["Puntos"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarClientes/Producto.add_child(hbox)

func consultar_clientes():
	db.query("SELECT * FROM USUARIOS")
	var clientes = db.query_result
	for i in range(len(clientes)):
		var hbox = HBoxContainer.new()
		var boton_cliente = Button.new()
		boton_cliente.text = clientes[i]["Nombre"]
		hbox.add_child(boton_cliente)

		var label_info = Label.new()
		var texto_info = "CC: " + str(clientes[i]["CC"]) + "\nPuntos: $" + str(clientes[i]["Puntos"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarClientes/Productos/Datos.add_child(hbox)

func agregar_cliente(cc, nombre):
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int(cc))
	if not db.query_result:
		db.query("INSERT INTO USUARIOS VALUES (%d, '%s', %d)" % [int(cc), str(nombre), 0])
		$Separador/Datos/NuevoCliente/NuevoC/Label.text = "Exito"
	else:
		$Separador/Datos/NuevoCliente/NuevoC/Label.text = "Error"

func eliminar_cliente(identificador): 
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int(identificador))
	if  db.query_result:
		db.query("DELETE FROM USUARIOS WHERE CC = %d" % int(identificador))
		$Separador/Datos/EliminarCliente/EliminarC/Label.text = "Exito"
	else:
		$Separador/Datos/EliminarCliente/EliminarC/Label.text = "Error"

func modificar_puntos_cliente(cc, cantidad_puntos):
	db.query("SELECT Puntos FROM USUARIOS WHERE CC = %d" % int(cc))
	if db.query_result:
		db.query("UPDATE USUARIOS SET Puntos = %d WHERE CC = %d" % [int(cantidad_puntos), int(cc)])
		$Separador/Datos/ModificarCliente/Contenedor/Label.text = "Exito"

func agregar_producto(producto, cantidad):
	var total = 0
	db.query("SELECT * FROM PRODUCTOS WHERE Nombre = '%s'" % producto.to_upper())
	var prod = db.query_result
	if prod:
		if prod[0]["Cantidad"] >= int(cantidad):
			total = int(prod[0]["Precio_$"] * int(cantidad))
			db.query("UPDATE PRODUCTOS SET Cantidad = %d WHERE Nombre = '%s'" % [int(prod[0]["Cantidad"]-int(cantidad)), str(producto).to_upper()])
			lista_compra.append({"id":prod[0]["id_Prod"], "Nombre":prod[0]["Nombre"], "cantidad": cantidad, "Precio":prod[0]["Precio_$"], "total_producto":total })

			$Separador/Datos/RealizarVenta/Contenedor/Venta/Confirmacion.text = "Exito"
		else:
			$Separador/Datos/RealizarVenta/Contenedor/Venta/Confirmacion.text = "Error"
	else:
		$Separador/Datos/RealizarVenta/Contenedor/Venta/Confirmacion.text = "Error"
	return total
	
func agregar_venta(cc, fecha, total_venta ):
	var id_venta = 1
	db.query("SELECT * FROM VENTAS")
	if db.query_result:
		id_venta = db.query_result[-1]["id_Venta"] + 1
	db.query("INSERT INTO VENTAS (id_Venta, CC_Cliente, Fecha, Total_$) VALUES (%d, %d, '%s', %d)" % [ id_venta, int(cc), str(fecha), int(total_venta)])

# Agregare el bloque que contenga la informacion de la venta
func mostrar_venta(cc, fecha, producto, cantidad, transaccion):
	# Se limpia la lista si se cambia de opcion
	producto = str(producto).to_upper()
	if int(cc) == 0 or int(cc) != int(cliente_compra):
		lista_venta.clear()
	db.query("SELECT * FROM PRODUCTOS WHERE Nombre = '%s'" % producto)
	var info_producto = db.query_result
	var hbox = HBoxContainer.new()
	var boton_registro = Button.new()
	boton_registro.text = "Compra"
	hbox.add_child(boton_registro)
	if info_producto:
		var total_venta = 0
		if transaccion:
			total_venta = info_producto[0]["Precio_$"] * cantidad
		total_acumulado += total_venta  # Acumular el total de la venta
		
		# Caso donde no se guarda los datos
		if int(cc) == 0:
			var texto_info = "CC: " + str(cc) + "\nFecha: " + str(fecha) + "\nProductos: "
			for item in lista_compra:
				texto_info += "\nID: " + str(item["id"]) + ", PRODUCTO: " + str(item["Nombre"]) + ", CANTIDAD: " + str(item["cantidad"]) + ", PRECIO PRODUCTO: " + str(item["Precio"]) + ", TOTAL_PRODUCTO: " + str(item["total_producto"])
			texto_info += "\nTotal: $"  + str(total_acumulado) + "\nImpuesto IVA 19%: " + str(total_acumulado * 0.19) + "\nTotal Parcial: " + str(total_acumulado + (total_acumulado * 0.19))
			var label_info = Label.new()
			label_info.text = texto_info
			hbox.add_child(label_info)
		# Caso donde si se guarda los datos
		else:
			db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int(cc))    
			var info_cliente = db.query_result
			
			var texto_info = "CC: " + str(cc) + "\nFecha: " + str(fecha) + "\nProductos: "
			for item in lista_compra:
				texto_info += "\nID: " + str(item["id"]) + ", PRODUCTO: " + str(item["Nombre"]) + ", CANTIDAD: " + str(item["cantidad"]) + ", PRECIO PRODUCTO: " + str(item["Precio"]) + ", TOTAL_PRODUCTO: " + str(item["total_producto"])
			texto_info += "\nTotal: $"  + str(total_acumulado) + "\nImpuesto IVA 19%: " + str(total_acumulado * 0.19) + "\nTotal Parcial: " + str(total_acumulado + (total_acumulado * 0.19)) + "\nPuntos Obtenidos: " + str((total_acumulado * 4) / 100) + "\nPuntos Totales: " + str(info_cliente[0]["Puntos"] + (total_acumulado * 4) / 100)
			var label_info = Label.new()
			label_info.text = texto_info
			hbox.add_child(label_info)
	else:
		var texto_info = "CC: " + str(cc) + "\nFecha: " + str(fecha) + "\nProductos: "
		for item in lista_compra:
			texto_info += "\nID: " + str(item["id"]) + ", PRODUCTO: " + str(item["Nombre"]) + ", CANTIDAD: " + str(item["cantidad"]) + ", PRECIO PRODUCTO: " + str(item["Precio"]) + ", TOTAL_PRODUCTO: " + str(item["total_producto"])
		texto_info += "\nTotal: $"  + str(total_acumulado) + "\nImpuesto IVA 19%: " + str(total_acumulado * 0.19) + "\nTotal Parcial: " + str(total_acumulado + (total_acumulado * 0.19))
		var label_info = Label.new()
		label_info.text = texto_info
		hbox.add_child(label_info)
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro/CompraActual.add_child(hbox)

func consultar_ventas():
	db.query("SELECT * FROM VENTAS ORDER BY Fecha")  # Aqui con esto se ordena ascendentemente si se desea descendente se debe poner al lado de fecha "DESC"
	var ventas = db.query_result
	for i in range(len(ventas)):
		var hbox = HBoxContainer.new()
		var boton_venta = Button.new()
		boton_venta.text = str(ventas[i]["id_Venta"])
		hbox.add_child(boton_venta)

		var label_info = Label.new()
		var texto_info = "CC: " + str(ventas[i]["CC_Cliente"]) + "\nFecha: " + str(ventas[i]["Fecha"]) + "\nTotal: $" + str(ventas[i]["Total_$"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarVentas/Productos/Datos.add_child(hbox)

func consultarVenta_fechaEspecifica(fecha_especifica):
	db.query("SELECT * FROM VENTAS WHERE Fecha = '%s'" % [str(fecha_especifica)])
	var ventasEs = db.query_result
	for i in range(len(ventasEs)):
		var hbox = HBoxContainer.new()
		var boton_venta = Button.new()
		boton_venta.text = str(ventasEs[i]["id_Venta"])
		hbox.add_child(boton_venta)

		var label_info = Label.new()
		var texto_info = "CC: " + str(ventasEs[i]["CC_Cliente"]) + "\nFecha: " + str(ventasEs[i]["Fecha"]) + "\nTotal: $" + str(ventasEs[i]["Total_$"])
		label_info.text = texto_info
		hbox.add_child(label_info)
		$Separador/Datos/ConsultarVenta/Productos/Datos.add_child(hbox)

###################
func _on_login_pressed():
	var result = 0
	db.query("SELECT id_R FROM EMPLEADOS WHERE CC = (%d) and Contrasena = (%s)" % [int($Separador/Datos/Login/Cedula.text), $"Separador/Datos/Login/Contraseña".text])
	if db.query_result:
		result = db.query_result[0]["id_R"]
		user = result
	$Separador/Datos/Login/Cedula.text = ""
	$"Separador/Datos/Login/Contraseña".text = ""
	if result == 1:
		$Separador/Datos/Login/Label.text = "Administrador"
		mostrar_funciones(user)
		vista_activa.hide()
	elif result == 2:
		$Separador/Datos/Login/Label.text = "Vendedor"
		mostrar_funciones(user)
		vista_activa.hide()
	else:
		$Separador/Datos/Login/Label.text = "Denegado"

	
func mostrar_funciones(user):
	if user == 1 or user == 2:
		$Separador/Opciones/ScrollContainer/Funciones/ConsultarProductos.show()
		$Separador/Opciones/ScrollContainer/Funciones/ConsultarVendedores.show()
		$Separador/Opciones/ScrollContainer/Funciones/ConsultarClientes.show()
		$Separador/Opciones/ScrollContainer/Funciones/NuevoCliente.show()
		$Separador/Opciones/ScrollContainer/Funciones/EliminarCliente.show()
		$Separador/Opciones/ScrollContainer/Funciones/ModificarCliente.show()
		$Separador/Opciones/ScrollContainer/Funciones/RealizarVenta.show()
	if user == 1:
		$Separador/Opciones/ScrollContainer/Funciones/NuevoProducto.show()
		$Separador/Opciones/ScrollContainer/Funciones/EliminarProducto.show()
		$Separador/Opciones/ScrollContainer/Funciones/ModificarProducto.show()
		$Separador/Opciones/ScrollContainer/Funciones/NuevoVendor.show()
		$Separador/Opciones/ScrollContainer/Funciones/EliminarVendedor.show()
		$Separador/Opciones/ScrollContainer/Funciones/ModificarVendedor.show()
		$Separador/Opciones/ScrollContainer/Funciones/ConsultarVentas.show()
		$Separador/Opciones/ScrollContainer/Funciones/ConsultarVenta.show()
		

func _on_salir_pressed():
	get_tree().quit()
	
##################
func _on_productos_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ConsultarProductos
	$Separador/Datos/ConsultarProductos.show()
	
	if $Separador/Datos/ConsultarProductos/Productos/Datos.get_child_count() == 0:
		consultar_productos()
	else:
		for child in $Separador/Datos/ConsultarProductos/Productos/Datos.get_children():
			child.queue_free()
		consultar_productos()
			
func _on_buscar_pressed():
	if $Separador/Datos/ConsultarProductos/Producto.get_child_count() == 1:
		consulta_producto($Separador/Datos/ConsultarProductos/Producto/Busqueda/IdProducto.text)
	else:
		$Separador/Datos/ConsultarProductos/Producto.get_children()[1].queue_free()
		consulta_producto($Separador/Datos/ConsultarProductos/Producto/Busqueda/IdProducto.text)

##################
func _on_agregar_pressed():
	var nombre = $Separador/Datos/NuevoProducto/NuevoP/Nombre.text
	var cantidad = $Separador/Datos/NuevoProducto/NuevoP/Cantidad.text
	var precio = $Separador/Datos/NuevoProducto/NuevoP/Precio.text
	if nombre !="":
		nuevo_producto(nombre, cantidad, precio)
		$Separador/Datos/NuevoProducto/NuevoP/Label.text = "Exito"
	else:
		$Separador/Datos/NuevoProducto/NuevoP/Label.text="Error"
	
func _on_nuevo_p_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/NuevoProducto
	$Separador/Datos/NuevoProducto.show()
	
##################
func _on_eliminar_pressed():
	eliminar_producto($Separador/Datos/EliminarProducto/EliminarP/Id.text)

func _on_eliminar_p_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/EliminarProducto
	$Separador/Datos/EliminarProducto.show()

##################

func _on_modificar_p_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ModificarProducto
	$Separador/Datos/ModificarProducto.show()

func _on_buscar_p_pressed():
	db.query("SELECT * FROM PRODUCTOS WHERE id_Prod = %d" % int($Separador/Datos/ModificarProducto/Contenedor/Id.text))
	var producto = db.query_result
	if producto:
		$Separador/Datos/ModificarProducto/Contenedor/Nombre/Nombre.text = producto[0]["Nombre"]
		$Separador/Datos/ModificarProducto/Contenedor/Cantidad/Cantidad.text = str(producto[0]["Cantidad"])
		$Separador/Datos/ModificarProducto/Contenedor/Precio/Precio.text = str(producto[0]["Precio_$"])
	else:
		$Separador/Datos/ModificarProducto/Contenedor/Serador.text = "Error"

func _on_cambiar_pressed():
	var identificador = $Separador/Datos/ModificarProducto/Contenedor/Id.text
	var nueva_cantidad = $Separador/Datos/ModificarProducto/Contenedor/Cantidad/Cantidad.text
	var nuevo_precio = $Separador/Datos/ModificarProducto/Contenedor/Precio/Precio.text
	var nuevo_nombre = $Separador/Datos/ModificarProducto/Contenedor/Nombre/Nombre.text
	if str(nuevo_nombre) != "" and int(nuevo_precio)>=0 and int(nueva_cantidad)>=0:
		modificar_producto(identificador, nueva_cantidad)
		actualizar_precio(identificador, nuevo_precio)
		actualizar_nombre(identificador, nuevo_nombre)

##################

func _on_agregar_v_pressed():
	var cc = $Separador/Datos/NuevoVendor/NuevoP/CC.text
	var nombre = $Separador/Datos/NuevoVendor/NuevoP/Nombre.text
	var contrasenia = $"Separador/Datos/NuevoVendor/NuevoP/Contraseña".text
	if cc != "" and nombre != "" and contrasenia != "":
		agregar_vendedor(cc, nombre, contrasenia)
	else:
		$Separador/Datos/NuevoVendor/NuevoP/Label.text = "Error"
func _on_nuevo_v_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/NuevoVendor
	$Separador/Datos/NuevoVendor.show()

###################

func _on_eliminar_v_pressed():
	eliminar_vendedor($Separador/Datos/EliminarVendedor/EliminarV/CC.text)

func _on_eliminar_ven_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/EliminarVendedor
	$Separador/Datos/EliminarVendedor.show()

###################
	
func _on_aceptar_v_pressed():
	var identificador = $Separador/Datos/ModificarVendedor/Contenedor/CC.text
	var nuevo_rango = $Separador/Datos/ModificarVendedor/Contenedor/Rol/Rol.text
	var nueva_contrasena = $"Separador/Datos/ModificarVendedor/Contenedor/Contraseña/Contraseña".text
	nuevo_rango = int(nuevo_rango)
	if (nuevo_rango != 0 and nuevo_rango > 0 and nuevo_rango <3) and str(nueva_contrasena)!="":
		modificar_rango(nuevo_rango, identificador)
		modificar_contrasenia(nueva_contrasena, identificador)
	else:
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Error"

func _on_buscar_v_pressed():
	db.query("SELECT * FROM EMPLEADOS WHERE CC = %d" % int($Separador/Datos/ModificarVendedor/Contenedor/CC.text))
	var producto = db.query_result
	if producto:
		$Separador/Datos/ModificarVendedor/Contenedor/Rol/Rol.text = str(producto[0]["id_R"])
		$"Separador/Datos/ModificarVendedor/Contenedor/Contraseña/Contraseña".text = str(producto[0]["Contrasena"])
	else:
		$Separador/Datos/ModificarVendedor/Contenedor/Label.text = "Error"

func _on_modificarven_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ModificarVendedor
	$Separador/Datos/ModificarVendedor.show()

###################

func _on_consultar_ven_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ConsultarVendedores
	$Separador/Datos/ConsultarVendedores.show()
	
	if $Separador/Datos/ConsultarVendedores/Productos/Datos.get_child_count() == 0:
		consultar_vendedores()
	else:
		for child in $Separador/Datos/ConsultarVendedores/Productos/Datos.get_children():
			child.queue_free()
		consultar_vendedores()

func _on_buscar_vent_pressed():
	if $Separador/Datos/ConsultarVendedores/Producto.get_child_count() == 1:
		consulta_vendedor($Separador/Datos/ConsultarVendedores/Producto/Busqueda/CC.text)
	else:
		$Separador/Datos/ConsultarVendedores/Producto.get_children()[1].queue_free()
		consulta_vendedor($Separador/Datos/ConsultarVendedores/Producto/Busqueda/CC.text)

###################

func _on_consultar_cli_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ConsultarClientes
	$Separador/Datos/ConsultarClientes.show()
	
	if $Separador/Datos/ConsultarClientes/Productos/Datos.get_child_count() == 0:
		consultar_clientes()
	else:
		for child in $Separador/Datos/ConsultarClientes/Productos/Datos.get_children():
			child.queue_free()
		consultar_clientes()

func _on_buscar_clien_pressed():
	
	if $Separador/Datos/ConsultarClientes/Producto.get_child_count() == 1:
		consultar_cliente($Separador/Datos/ConsultarClientes/Producto/Busqueda/CC.text)
	else:
		$Separador/Datos/ConsultarClientes/Producto.get_children()[1].queue_free()
		consultar_cliente($Separador/Datos/ConsultarClientes/Producto/Busqueda/CC.text)

###################

func _on_nuevo_c_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/NuevoCliente
	$Separador/Datos/NuevoCliente.show()
	
func _on_agregar_c_pressed():
	var cc = $Separador/Datos/NuevoCliente/NuevoC/CC.text
	var nombre = $Separador/Datos/NuevoCliente/NuevoC/Nombre.text
	if cc != 0 and nombre != "":
		agregar_cliente(cc, nombre)
	else:
		$Separador/Datos/NuevoCliente/NuevoC/Label.text = "Error"
	
###################

func _on_eliminar_c_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/EliminarCliente
	$Separador/Datos/EliminarCliente.show()

func _on_eliminar_cient_pressed():
	var cc = $Separador/Datos/EliminarCliente/EliminarC/CC.text
	eliminar_cliente(cc)

###################

func _on_modificar_cli_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ModificarCliente
	$Separador/Datos/ModificarCliente.show()

func _on_buscarcli_pressed():
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" % int($Separador/Datos/ModificarCliente/Contenedor/CC.text))
	var producto = db.query_result
	if producto:
		$Separador/Datos/ModificarCliente/Contenedor/Puntos/Puntos.text = str(producto[0]["Puntos"])
	else:
		$Separador/Datos/ModificarCliente/Contenedor/Serador.text = "Error"

func _on_aceptarcli_pressed():
	var cc = $Separador/Datos/ModificarCliente/Contenedor/CC.text
	var puntos = $Separador/Datos/ModificarCliente/Contenedor/Puntos/Puntos.text
	if cc != 0 and puntos >=0:
		modificar_puntos_cliente(cc,puntos)
	else:
		$Separador/Datos/ModificarCliente/Contenedor/Label.text = "Error"

###################

func _on_cerrar_sesion_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/Login
	$Separador/Datos/Login.show()

	$Separador/Opciones/ScrollContainer/Funciones/ConsultarProductos.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ConsultarVendedores.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ConsultarClientes.hide()
	$Separador/Opciones/ScrollContainer/Funciones/NuevoCliente.hide()
	$Separador/Opciones/ScrollContainer/Funciones/EliminarCliente.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ModificarCliente.hide()
	$Separador/Opciones/ScrollContainer/Funciones/RealizarVenta.hide()
	$Separador/Opciones/ScrollContainer/Funciones/NuevoProducto.hide()
	$Separador/Opciones/ScrollContainer/Funciones/EliminarProducto.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ModificarProducto.hide()
	$Separador/Opciones/ScrollContainer/Funciones/NuevoVendor.hide()
	$Separador/Opciones/ScrollContainer/Funciones/EliminarVendedor.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ModificarVendedor.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ConsultarVentas.hide()
	$Separador/Opciones/ScrollContainer/Funciones/ConsultarVenta.hide()

###################

func _on_venta_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/RealizarVenta
	$Separador/Datos/RealizarVenta.show()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/MensajeGracias.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Permiso.show()
	$Separador/Datos/RealizarVenta/Contenedor/Opciones.show()
	$Separador/Datos/RealizarVenta/Contenedor/Venta.hide()
	$Separador/Datos/RealizarVenta/Contenedor/CC.hide()
	$"Separador/Datos/RealizarVenta/Contenedor/Aceptar Permiso".hide()
	$Separador/Datos/RealizarVenta/Contenedor/Mensaje.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro/CompraActual.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro/CompraActual.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro.custom_minimum_size.x = 0
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro.custom_minimum_size.y = 120
	$Separador/Datos/RealizarVenta/Contenedor/CC.text = ""

func _on_si_pressed():
	$Separador/Datos/RealizarVenta/Contenedor/Permiso.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Opciones.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/MensajeGracias.hide()
	
	$Separador/Datos/RealizarVenta/Contenedor/CC.show()
	$"Separador/Datos/RealizarVenta/Contenedor/Aceptar Permiso".show()
	
func _on_no_pressed():
	$Separador/Datos/RealizarVenta/Contenedor/Permiso.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Opciones.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta.show()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/MensajeGracias.hide()
	cliente_compra = 0
	$Separador/Datos/RealizarVenta/Contenedor/Venta/puntos_cliente.text = "Cliente: 00000 --- Puntos: 0"
	for children in $Separador/Datos/RealizarVenta/Contenedor/Venta/Productos/Datos.get_children():
		children.queue_free()
	consultar_productos2()

func _on_aceptar_permiso_pressed():
	var cc_cliente = $Separador/Datos/RealizarVenta/Contenedor/CC.text
	db.query("SELECT * FROM USUARIOS WHERE CC = %d" %(int(cc_cliente)))
	var cliente = db.query_result
	if cliente:
		cliente_compra = cc_cliente
		$Separador/Datos/RealizarVenta/Contenedor/CC.hide()
		$"Separador/Datos/RealizarVenta/Contenedor/Aceptar Permiso".hide()
		$Separador/Datos/RealizarVenta/Contenedor/Venta.show()
		$Separador/Datos/RealizarVenta/Contenedor/Mensaje.hide()
		$Separador/Datos/RealizarVenta/Contenedor/Venta/puntos_cliente.text = "CLIENTE: %s --- Puntos: %d" % [str(cliente[0]["Nombre"]),int(cliente[0]["Puntos"])]
		for children in $Separador/Datos/RealizarVenta/Contenedor/Venta/Productos/Datos.get_children():
			children.queue_free()
		consultar_productos2()
	else:
		$Separador/Datos/RealizarVenta/Contenedor/Mensaje.text = "Error"
	
func _on_agregar_com_pressed():
	var producto = $Separador/Datos/RealizarVenta/Contenedor/Venta/Nombre.text
	var cantidad = $Separador/Datos/RealizarVenta/Contenedor/Venta/Cantidad.text
	producto = str(producto)
	cantidad = int(cantidad)
	for children in $Separador/Datos/RealizarVenta/Contenedor/Venta/Productos/Datos.get_children():
		children.queue_free()
	
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Productos/Datos.show()
	for children in $Separador/Datos/RealizarVenta/Contenedor/Venta/Registro/CompraActual.get_children():
		children.queue_free()
	# SE AGREGA LA FUNCION DE REGISTRO
	var fecha = Time.get_date_string_from_system()
	
		
	if cantidad > 0:
		var total_producto = agregar_producto(producto, cantidad)
		if total_producto != 0:
			total_compra = total_compra + total_producto
		mostrar_venta(cliente_compra, fecha, producto, cantidad, total_producto)
		consultar_productos2()
		$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro/CompraActual.show()
		$Separador/Datos/RealizarVenta/Contenedor/Venta/Nombre.text = ""
		$Separador/Datos/RealizarVenta/Contenedor/Venta/Cantidad.text = ""
func actualizar_puntos_cliente(cliente_compra, total_compra):
	db.query("SELECT Puntos from USUARIOS WHERE CC = %d" % int(cliente_compra))
	var puntos = db.query_result
	var nuevos_puntos = (total_compra*0.81)*4/100
	db.query("UPDATE USUARIOS SET Puntos = %d WHERE CC = %d" % [int(puntos[0]["Puntos"]+nuevos_puntos), int(cliente_compra)])

func decrementar_puntos_cliente(cliente_compra, puntos_descontar):
	var ans = false
	db.query("SELECT Puntos from USUARIOS WHERE CC = %d" % int(cliente_compra))
	if db.query_result:
		var puntos = db.query_result
		if puntos[0]["Puntos"]>=puntos_descontar and puntos_descontar>=0:
			db.query("UPDATE USUARIOS SET Puntos = %d WHERE CC = %d" % [int(puntos[0]["Puntos"]-puntos_descontar), int(cliente_compra)])
			ans = true
	return ans
	
func _on_pago_puntos_pressed():
	return true

func _on_terminar_pressed():
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro.custom_minimum_size.x = 800
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Registro.custom_minimum_size.y = 300
	var puntos_descontar = int($Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/cantidad_puntos.text)
	if total_compra != 0:
		if _on_pago_puntos_pressed():
			if (puntos_descontar*100)/4 <= total_compra:
				if decrementar_puntos_cliente(cliente_compra, puntos_descontar):
					var decremento = (puntos_descontar*100)/4
					total_compra-= decremento
		var fecha = Time.get_date_string_from_system()
		if int(cliente_compra) != 0:
			actualizar_puntos_cliente(cliente_compra, total_compra)
		agregar_venta(cliente_compra, fecha, total_compra * 1.19)
		
		print(lista_compra)
		cliente_compra = 0
		total_compra = 0
		lista_venta = []
		lista_compra = []
		$Separador/Datos/RealizarVenta/Contenedor/Venta/MensajeFinal.text = "Se Añadio La Compra"
	else:
		$Separador/Datos/RealizarVenta/Contenedor/Venta/MensajeFinal.text = "Error"
	#$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/pago_puntos.toggled(false)
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Confirmacion.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Nombre.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Cantidad.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Productos.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/AgregarCom.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/MensajeFinal.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/Terminar.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/MensajeGracias.show()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/cantidad_puntos.hide()
	$Separador/Datos/RealizarVenta/Contenedor/Venta/Finalizar/pago_puntos.hide()
func _on_consultar_vs_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ConsultarVentas 
	$Separador/Datos/ConsultarVentas.show()
	
	if $Separador/Datos/ConsultarVentas/Productos/Datos.get_child_count() == 0:
		consultar_ventas()
	else:
		for child in $Separador/Datos/ConsultarVentas/Productos/Datos.get_children():
			child.queue_free()
		consultar_ventas()
	
func _on_consultar_vt_pressed():
	vista_activa.hide()
	vista_activa = $Separador/Datos/ConsultarVenta
	$Separador/Datos/ConsultarVenta.show()
	
func _on_buscar_ventas_pressed():
	var fecha_especifica = $Separador/Datos/ConsultarVenta/Producto/Busqueda/Fecha.text
	if $Separador/Datos/ConsultarVenta/Productos/Datos.get_child_count() == 0:
		consultarVenta_fechaEspecifica(fecha_especifica)
	else:
		for child in $Separador/Datos/ConsultarVenta/Productos/Datos.get_children():
			child.queue_free()
		consultarVenta_fechaEspecifica(fecha_especifica)

func _on_minimizar_pressed():
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_MINIMIZED)

func _on_maximizar_pressed():
	pantalla_completa *= -1
	if pantalla_completa == 1:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
