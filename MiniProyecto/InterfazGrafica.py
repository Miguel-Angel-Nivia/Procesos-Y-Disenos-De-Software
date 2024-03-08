import sys
from conexionSQL import Comunicacion
from PyQt5 import QtWidgets, uic


#Iniciar la aplicacion

app = QtWidgets.QApplication([])

#cargar archivos .ui
inicio = uic.loadUi("ventanas/inicio.ui")
login = uic.loadUi("ventanas/login.ui")

#enlace de funciones

def ejemplo_entrada():
	nombre = login.input_usuario.text()
	contrasenia = login.input_contra.text()
	if nombre == "willian" and contrasenia == "1234":
		login.texto_alerta.setText("Se supone que podes entrar")
	elif len(nombre) == 0 or len(contrasenia) == 0:
		print(len(nombre),len(contrasenia),type(nombre),type(contrasenia))
		login.texto_alerta.setText("Ingrese informacion")
	else:
		login.texto_alerta.setText("No mi rey no le podes entrar")

def ejemplo_cambio_pestania():
	inicio.hide()
	login.show()

def salir():
	app.exit()
inicio.bt_iniciar.clicked.connect(ejemplo_cambio_pestania)
login.bt_ingresar.clicked.connect(ejemplo_entrada)
inicio.bt_salir.clicked.connect(salir)
login.bt_salir.clicked.connect(salir)

#Ejecutable
inicio.show()
app.exec()


