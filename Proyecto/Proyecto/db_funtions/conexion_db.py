import sqlite3
from datetime import datetime

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect("db_proyecto.db")
        self.cursor = self.conexion.cursor()

    def inicio_base(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono INTEGER NOT NULL
            )
        """)
        # Create the 'dispositivos' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                estado TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS administradores(
                id INTEGER PRIMARY KEY,
                cc INTEGER NOT NULL,
                usuario TEXT NOT NULL,
                contrasenia TEXT NOT NULL,
                FOREIGN KEY (cc) REFERENCES usuarios(id)
            )
        """
        )
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS LOGSISTEMA ( 
                    fecha TIMESTAMP NOT NULL,
                    usuario TEXT NOT NULL,
                    mensaje TEXT NOT NULL,
                    FOREIGN KEY (usuario) REFERENCES administradores(usuario)
                    )
        """)
        # Create the 'pedidos' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_dispositivo INTEGER NOT NULL,
                id_usuario_envio INTEGER NOT NULL,
                id_usuario_receptor INTEGER NOT NULL,
                tipo_encargo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                fecha_solicitud TIMESTAMP NOT NULL,
                fecha_recepcion TIMESTAMP,
                lugar_recepcion TEXT,
                url TEXT NOT NULL,
                FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id),
                FOREIGN KEY (id_usuario_envio) REFERENCES usuarios(id),
                FOREIGN KEY (id_usuario_receptor) REFERENCES usuarios(id)
                )
        """)

        # Guarda los cambios
        self.conexion.commit()

        # cierra la conexion a la base de datos
        self.conexion.close()
comunicacion = Comunicacion()

comunicacion.inicio_base()