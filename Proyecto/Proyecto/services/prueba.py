import smtplib
from email.message import EmailMessage
import qrcode
from io import BytesIO

# Configura los detalles del correo electrónico
sender_email = 'cuentaprocesospp@outlook.com'
password = 'NiviaVazquezChapid69$'
receiver_email = 'williandavidchicho@gmail.com'
email_subject = "Código QR generado"
email_body = "Adjunto encontrarás el código QR generado."

# Genera el código QR con el mensaje deseado
mi_texto = "¡Hola desde Python!"
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(mi_texto)
qr.make(fit=True)
imagen_qr = qr.make_image(fill_color="black", back_color="white")

# Crea un archivo temporal en memoria
qr_temp = BytesIO()
imagen_qr.save(qr_temp, format="PNG")
qr_temp.seek(0)  # Reinicia el puntero del archivo

# Crea el mensaje de correo electrónico
message = EmailMessage()
message.set_content(email_body)
message['Subject'] = email_subject
message['From'] = sender_email
message['To'] = receiver_email

# Adjunta el archivo del código QR desde el archivo temporal
message.add_attachment(qr_temp.read(), maintype="image", subtype="png", filename="mi_codigo_qr.png")


with smtplib.SMTP('smtp.office365.com', 587) as server:
    server.ehlo()  # Identificar al cliente en el servidor SMTP
    server.starttls()  # Iniciar cifrado TLS
    server.ehlo()  # Reidentificar después de iniciar TLS
    server.login(sender_email, password)
    server.send_message(message)

print("Correo enviado con éxito. Código QR adjunto.")
