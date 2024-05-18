import reflex as rx
from .conexion_db import Comunicacion
from datetime import datetime
from ..services.correo_service import MailManagment
import time


conexion = Comunicacion()
correo = MailManagment()
class PedidoManagment:
    def obtener_pedidos(self):
        state = False
        pedidos = conexion.get_state_orders()
        if len(pedidos) != 0:
            state = True
        return pedidos, state
    def crear_pedido(self, data):
        verificacion = False
        data["url"] = "https://Drive.com"
        data["fecha_solicitud"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["fecha_recepcion"] = f"{data['fecha_temporal_recepcion']} {data['hora_entrega']}"
        dispositivo = data["id_dispositivo"]
        data["id_dispositivo"] = int(data["id_dispositivo"].split('-')[0])
        print(data["id_usuario_envio"])
        verificacion = conexion.verification_user(data["id_usuario_envio"])
        print(verificacion)
        verificacion = conexion.verification_user(data["id_usuario_receptor"])
        print(verificacion)
        if verificacion != None:
            correo.send_notification("reserva", verificacion, data["fecha_recepcion"],dispositivo, data["tipo_encargo"], data["lugar_recepcion"])
            conexion.set_device_state("reserva",data["id_dispositivo"])
            return conexion.crear_pedido(data)
        else:
            return False
        #correo.send_notification("reserva", "willian17ch@gmail.com", data["fecha_recepcion"],dispositivo, data["tipo_encargo"], data["lugar_recepcion"])
        
        ##correo.send_notification("reserva", "willian17ch@gmail.com", data["fecha_recepcion"],dispositivo, data["tipo_encargo"], data["lugar_recepcion"])
        #conexion.set_device_state("reserva",data["id_dispositivo"])
        #return conexion.crear_pedido(data)
    def eliminar_pedido(self, data):
        pass
    def obtener_dispositivo_disponible(self, tipo):
        busqueda = conexion.get_device_type(tipo)
        consulta = []
        for fila in busqueda:
            temp = f"{fila[0]}-{fila[1]}"
            consulta.append(temp)
        return consulta
    def get_all_free_device(self):
        busqueda = conexion.get_all_of(["id","tipo"], "dispositivos")
        consulta = []
        for fila in busqueda:
            temp = f"{fila[0]}-{fila[1]}"
            consulta.append(temp)
        return consulta
    rx.background
    async def activacion(self, id):
        data = conexion.get_one_orders(id)[0]
        print(data)
        interval = 2
        states = ["SALIDA", "PROXIMIDAD", "LLEGADA", "CODIGO", "ENTREGA"]
        for i in states:
            conexion.set_device_state(i,data[6])
            if i == "CODIGO":
                correo.send_qr("Codigo Entrega", data[2])
                print("codigo")
                time.sleep(interval*2)
            else:
                correo.send_notification(i, data[8], data[1], data[4], data[6], data[5])
                print(i)
                time.sleep(interval)
        conexion.set_device_state('ACTIVO',data[6])
        return True

p = PedidoManagment()