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
                id INTEGER PRIMARY KEY,
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
        self.cursor.execute("INSERT INTO ADMINISTRADORES VALUES (101, 101, 'wislian','Sharkespeare1975$')")
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
    

    def get_state_orders(self):
        consulta = (
        "SELECT "
        "pedidos.fecha_solicitud AS fecha_envio, "
        "pedidos.fecha_recepcion AS fecha_recepcion,"
        "usuario_envio.nombre AS nombre_usuario_envio, "
        "usuario_receptor.nombre AS nombre_usuario_receptor, "
        "dispositivos.tipo AS tipo_dispositivo, "
        "pedidos.lugar_recepcion, "
        "pedidos.id, "
        "dispositivos.estado, "
        "usuario_receptor.email As email "
        "FROM "
        "pedidos "
        "JOIN "
        "usuarios AS usuario_envio ON pedidos.id_usuario_envio = usuario_envio.id "
        "JOIN "
        "usuarios AS usuario_receptor ON pedidos.id_usuario_receptor = usuario_receptor.id "
        "JOIN "
        "dispositivos ON pedidos.id_dispositivo = dispositivos.id"
        )
        self.cursor.execute(consulta)
        result = self.cursor.fetchall()
        return result

    def get_one_orders(self, id):
        consulta = (
        "SELECT "
        "pedidos.fecha_solicitud AS fecha_envio, "
        "pedidos.fecha_recepcion AS fecha_recepcion,"
        "usuario_envio.nombre AS nombre_usuario_envio, "
        "usuario_receptor.nombre AS nombre_usuario_receptor, "
        "dispositivos.tipo AS tipo_dispositivo, "
        "pedidos.lugar_recepcion, "
        "pedidos.id, "
        "dispositivos.estado, "
        "usuario_receptor.email As email "
        "FROM "
        "pedidos "
        "JOIN "
        "usuarios AS usuario_envio ON pedidos.id_usuario_envio = usuario_envio.id "
        "JOIN "
        "usuarios AS usuario_receptor ON pedidos.id_usuario_receptor = usuario_receptor.id "
        "JOIN "
        "dispositivos ON pedidos.id_dispositivo = dispositivos.id "
        "WHERE "
        "pedidos.id = ? "
        )
        self.cursor.execute(consulta,(id))
        result = self.cursor.fetchall()
        return result

    def crear_pedido(self, nuevo_pedido):
        consulta = """
        INSERT INTO pedidos (
            id_dispositivo,
            id_usuario_envio,
            id_usuario_receptor,
            tipo_encargo,
            descripcion,
            fecha_solicitud,
            fecha_recepcion,
            lugar_recepcion,
            url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

        # Ejecutar la consulta SQL de inserción
        self.cursor.execute(consulta, (
            nuevo_pedido["id_dispositivo"],
            nuevo_pedido["id_usuario_envio"],
            nuevo_pedido["id_usuario_receptor"],
            nuevo_pedido["tipo_encargo"],
            nuevo_pedido["descripcion"],
            nuevo_pedido["fecha_solicitud"],
            nuevo_pedido["fecha_recepcion"],
            nuevo_pedido["lugar_recepcion"],
            nuevo_pedido["url"]
        ))
        self.conexion.commit()
        return True

    def get_device_type(self, tipo):
        consulta = """SELECT id, TIPO
                    FROM dispositivos
                    where tipo = ? AND estado = 'ACTIVO'"""
        self.cursor.execute(consulta,(tipo,))
        busqueda = self.cursor.fetchall()
        return busqueda
    def set_device_state(self, estado, id):
        consulta = """UPDATE dispositivos
                      SET estado = ?
                      WHERE id = ?
                        """
        self.cursor.execute(consulta, (estado, id))
        self.conexion.commit()

    def get_all_of(self, object, table):
        valid_columns = ', '.join(object)
        consulta = f"SELECT {valid_columns} FROM {table} where estado = 'ACTIVO'"
        self.cursor.execute(consulta)
        busqueda = self.cursor.fetchall()
        return busqueda
    

    def get_similar_users(self, field, name, name2 = None):
        if (field == "fecha_solicitud" or field == "fecha_recepcion") and name2 != None:
            self.cursor.execute(f"SELECT * FROM PEDIDOS WHERE {field} BETWEEN {name} AND {name2}")
            result = self.fetchall()
        else:
            self.cursor.execute(f"SELECT * FROM PEDIDOS WHERE {field} = {name}")
    
    def get_field(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '<nombre_tabla>'")
        return self.cursor.fetchall()
    def verification_admin(self, data:dict):
        ans = False
        sql = "SELECT * FROM ADMINISTRADORES WHERE USUARIO = ? AND CONTRASENIA = ?"
        self.cursor.execute(sql, (data['username'], data['password']))
        busqueda = self.cursor.fetchone()
        if busqueda:
            ans = True
        return ans
    def verification_user(self, data):
        ans = False
        sql = "SELECT email FROM usuarios WHERE id  = ?"
        self.cursor.execute(sql, (data))
        busqueda = self.cursor.fetchone()
        if busqueda:
            return busqueda
        else:
            return None
    
#comunicacion = Comunicacion()
#comunicacion.inicio_base()
#comunicacion.datos_base()