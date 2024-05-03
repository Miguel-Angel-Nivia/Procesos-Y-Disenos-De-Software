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
        #self.conexion.close()

    def datos_base(self):
        self.cursor.execute("INSERT INTO DISPOSITIVOS VALUES (1, 'ROBOT', 'ACTIVO')")
        self.cursor.execute("INSERT INTO DISPOSITIVOS VALUES (2, 'ROBOT', 'MANTEMIENTO')")
        self.cursor.execute("INSERT INTO DISPOSITIVOS VALUES (3, 'DRON', 'ACTIVO')")
        self.cursor.execute("INSERT INTO DISPOSITIVOS VALUES (4, 'DRON', 'ACTIVO')")
        self.cursor.execute("INSERT INTO DISPOSITIVOS VALUES (5, 'DRON', 'INACTIVO')")
        self.cursor.execute("INSERT INTO USUARIOS VALUES (100, 'Miguel', 'Nivia', 'miguelangelnivia@gmail.com', '1111111111')")
        self.cursor.execute("INSERT INTO USUARIOS VALUES (101, 'Willian', 'Chapid', 'wilian17ch@gmail.com', '1111111112')")
        self.cursor.execute("INSERT INTO USUARIOS VALUES (102, 'Daniel', 'Vazquez', 'danielvasquez2004@javerianacali.edu.co', '1111111113')")
        self.cursor.execute("INSERT INTO USUARIOS VALUES (103, 'Jhon', 'Gomez', 'jhon.gomezt@javerianacali.edu.co', '1111111114')")
        self.cursor.execute("INSERT INTO ADMINISTRADORES VALUES (100, 100, 'ultrablue','UltraKinGGai$777')")
        self.cursor.execute("INSERT INTO ADMINISTRADORES VALUES (101, 101, 'wislian','Sharkespeare1975;$')")
        self.cursor.execute("INSERT INTO ADMINISTRADORES VALUES (102, 102, 'dok','SteamPoDjug@r999&Cafe')")
        self.conexion.commit()
        
    def registrar_cambio(self, mensaje:str) -> None:
        fecha = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.cursor.execute(f"INSERT INTO LOGSISTEMA (fecha, mensaje) values ({fecha},'{mensaje}'')")
          
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM USUARIOS")
        return self.cursor.fetchall()
    
    def get_all_orders(self):
        self.cursor.execute("SElECT * FROM PEDIDOS")
        return self.cursor.fetchall()
    
    def get_similar_users(self, field, name, name2 = None):
        if (field == "fecha_solicitud" or field == "fecha_recepcion") and name2 != None:
            self.cursor.execute(f"SELECT * FROM PEDIDOS WHERE {field} BETWEEN {name} AND {name2}")
            result = self.fetchall()
        else:
            self.cursor.execute(f"SELECT * FROM PEDIDOS WHERE {field} = {name}")
    
    def get_field(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '<nombre_tabla>'")
        return self.cursor.fetchall()
#comunicacion.inicio_base()
#comunicacion.datos_base()