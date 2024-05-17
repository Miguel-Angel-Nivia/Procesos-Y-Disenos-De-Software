import reflex as rx
from .conexion_db import Comunicacion
import time

conexion = Comunicacion()


def autentication(data:dict):
    verificacion = False
    verificacion = conexion.verification_admin(data)
    time.sleep(3)
    return verificacion


