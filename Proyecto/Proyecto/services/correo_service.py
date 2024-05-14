from QRcode_service import QRGenerator
import smtplib
from email.message import EmailMessage


class Mail_managment():
    def send_mail(self, receiver_email, email_subject, email_body, qr = None):
        sender_email = "cuentaprocesospp@outlook.com"
        message = EmailMessage()
        message.set_content(email_body)
        message['subject'] = email_subject
        message['From' ] = sender_email
        message['To'] = receiver_email
        if qr != None:
            message.add_attachment(qr, maintype = "image", subtype = "png", filename = "codigo_qr.png")
        with smtplib.SMTP(host = "smtp-mail.outlook.com", port = 587) as server:
            server.ehlo()
            server.login(sender_email, "NiviaVazquezChapid69$")
            server.sendmail(from_addr= sender_email, to_addrs= receiver_email, msg= message)
            #server.send_message(message)
            server.quit()

    def send_qr(self, code, name, receiver_email):
        qr = QRGenerator()
        qr_code = qr.generate_code(code, name)
        email_subject = "Codigo para recibir pedido"
        email_body = "Tienes 5 minutos para usarlo"
        self.send_mail(receiver_email,email_subject, email_body, qr_code)

mail = Mail_managment()
#mail.send_qr(1111, "willian", "williandavidchicho@gmail.com")
#mail.send_mail("williandavidchicho@gmail.com", "prueba", "texto prueba")


sender_email = 'cuentaprocesospp@outlook.com'
password = 'NiviaVazquezChapid69$'
receiver_email = 'williandavidchicho@gmail.com'

# Crear el mensaje
msg = EmailMessage()
msg.set_content('Este es el contenido del correo')
msg['Subject'] = 'Asunto del correo'
msg['From'] = sender_email
msg['To'] = receiver_email

# Enviar el correo
'''
try:
    # Conectar al servidor SMTP de Outlook
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.ehlo()  # Identificar al cliente en el servidor SMTP
        server.starttls()  # Iniciar cifrado TLS
        server.ehlo()  # Reidentificar después de iniciar TLS
        server.login(sender_email, password)
        server.send_message(msg)
    print('Correo enviado exitosamente')
except smtplib.SMTPNotSupportedError as e:
    print(f'Error de soporte SMTP: {e}')
except smtplib.SMTPAuthenticationError as e:
    print(f'Error de autenticación: {e}')
except Exception as e:
    print(f'Ocurrió un error: {e}')
'''

try:
    with smtplib.SMTP_SSL('smtp.office365.com', 465) as server:
        server.ehlo()  # Identificar al cliente en el servidor SMTP
        server.login(sender_email, password)
        server.send_message(msg)
    print('Correo enviado exitosamente')
except smtplib.SMTPNotSupportedError as e:
    print(f'Error de soporte SMTP: {e}')
except smtplib.SMTPAuthenticationError as e:
    print(f'Error de autenticación: {e}')
except Exception as e:
    print(f'Ocurrió un error: {e}')