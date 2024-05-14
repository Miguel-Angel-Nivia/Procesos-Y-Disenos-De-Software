import smtplib
from QRcode_service import QRGenerator
from email.message import EmailMessage
from io import BytesIO

class Mail_managment():
    def send_mail(self,receiver_email, message):
        sender_email = 'cuentaprocesospp@outlook.com'
        password = 'NiviaVazquezChapid69$'
        message['From'] = sender_email
        message['To'] = receiver_email 
        with smtplib.SMTP(host = "smtp.office365.com", port = 587) as server:
            server.ehlo()  # Identificar al cliente en el servidor SMTP
            server.starttls()  # Iniciar cifrado TLS
            server.ehlo()  # Reidentificar después de iniciar TLS
            server.login(sender_email, password)
            server.send_message(message)
            server.quit()

    def send_qr(self, code, receiver_email):
        #Generacion de Qr envio
        qr = QRGenerator()
        qr_temp = BytesIO()
        qr_code = qr.generate_code(code)
        qr_code.save(qr_temp, format = "PNG")
        qr_temp.seek(0)

        #Creacion mensaje correo
        message = EmailMessage()
        email_subject = "Codigo para recibir pedido"
        email_body = "Tienes 5 minutos para usarlo"
        message.set_content(email_body)
        message['subject'] = email_subject
        message.add_attachment(qr_temp.read(), maintype="image", subtype="png", filename="CodigoQR.png")
        self.send_mail(receiver_email, message)
    def send_notification(self,option, receiver_email, name1 = None,name2 = None, fecha_entrega = None, dispositivo, pedido, lugar):
        message = EmailMessage()

        match option:
            case "reserva":
                email_subject = "Reserva pedido dron/robot"
                email_body = (f"Se ha realizado una reservacion de un pedido de {pedido} con {dispositivo}"
                              f"para {fecha_entrega} en {lugar}")
            case _:
                email_subject = "Codigo para recibir pedido"
                email_body = "Tienes 5 minutos para usarlo"


        message.set_content(email_body)
        message['subject'] = email_subject

mail = Mail_managment()
mail.send_qr("hola amigos de youtube", "williandavidchicho@gmail.com")