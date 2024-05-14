import qrcode


class QRGenerator():
    def generate_code(self, code):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(code)
        qr.make(fit=True)
        imagen_qr = qr.make_image(fill_color="black", back_color="white")
        return imagen_qr