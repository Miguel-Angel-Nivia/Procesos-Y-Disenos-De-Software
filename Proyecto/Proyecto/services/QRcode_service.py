import qrcode
from datetime import datetime
import os
import qrcode.constants

class QRGenerator():
    def generate_code(self, code, name):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qr_code = qrcode.make(f"{code}")
        return qr_code
        #qr_code.save(f"Proyecto/Proyecto/Codigos_Temporales/Codigo_qr_{name}_{fecha}.png")