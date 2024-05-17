from smtplib import SMTP
from .QRcode_service import QRGenerator
from email.message import EmailMessage
from io import BytesIO
import time
class MailManagment:
    def __init__(self) -> None:
        self.sender_email = 'cuentaprocesospp@outlook.com'
        self.password ='NiviaVazquezChapid69$'
    def send_mail(self,receiver_email, message):
        message['From'] = self.sender_email
        message['To'] = receiver_email 
        try:
            server = SMTP(host = "smtp.office365.com", port = 587)
            server.ehlo()  # Identificar al cliente en el servidor SMTP
            server.starttls()  # Iniciar cifrado TLS
            server.ehlo()  # Reidentificar después de iniciar TLS
            server.login(self.sender_email, self.password)
            server.send_message(message)
            server.quit()
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
    def send_qr(self, code, receiver_email):
        #Generacion de Qr envio
        qr = QRGenerator()
        qr_temp = BytesIO()
        qr_code = qr.generate_code(code)
        qr_code.save(qr_temp)
        qr_temp.seek(0)

        #Creacion mensaje correo
        message = EmailMessage()
        email_subject = "Codigo QR para recepcion pedido Universidad"
        email_body = "Hola ya llego el dispositivo, este es tu codigo para reclamar"
        message.set_content(email_body)
        message['subject'] = email_subject
        message.add_attachment(qr_temp.read(), maintype="image", subtype="png", filename="CodigoQR.png")
        self.send_mail(receiver_email, message)

    def send_notification(self,option = None, receiver_email = None,  fecha_entrega = None, dispositivo = None, pedido = None, lugar = None):
        message = EmailMessage()

        match option:
            case "reserva":
                email_subject = "Reserva pedido dron/robot"
                email_body = (f"Se ha realizado una reservacion de un pedido de {pedido} con {dispositivo}"
                              f"para {fecha_entrega} en {lugar}")
            case "salida":
                email_subject = "Pedido se ha despachado"
                email_body = (f"Su pedido ha salido, recuerde retirarlo en {lugar}")
            case "proximidad":
                email_subject = "Su pedido esta cerca"
                email_body = (f"Su pedido esta alrededor de 5 minutos de llegar a {lugar}")
            case "llegada":
                email_subject = "Su pedido ya ha llegado a destino"
                email_body = (f"Su pedido se encuentra en {lugar}")
            case "entrega":
                email_subject = "Pedido entregado"
                email_body = (f"Su pedido ha sido entregado exitosamente\n"
                                "Por favor realice la siguiente encuesta de satisfaccion\n\n"
                                "https://forms.office.com/r/3J59pttrzJ?origin=lprLink")
            case _:
                email_subject = "Prueba de envio "
                email_body = "Prueba de envio"
        message.set_content(email_body)
        message['subject'] = email_subject
        self.send_mail(receiver_email, message)

    def send_notification_loop(self, interval, receiver_email, datos, code):
        messages = ["salida", "proximidad", "llegada","codigo", "entrega"]
        for i in messages:
            if i == "codigo":
                self.send_qr(code, receiver_email)
                time.sleep(interval*2)
            else:
                self.send_notification(i, receiver_email, datos[0], datos[1], datos[2], datos[3])
                time.sleep(interval)
            
mail = MailManagment()

#mail.send_notification(option = "entrega", receiver_email = "williandavidchicho@gmail.com")
#tasks = [mail.send_notification_loop(10, "williandavidchicho@gmail.com", ["2024","dron","domicilio","Cedro Rosado"],11111),
#         mail.send_notification_loop(10, "willian17ch@gmail.com", ["2024","dron","domicilio","Cedro Rosado"],222222),
#         mail.send_notification_loop(10, "miguelangelnivia@gmail.com", ["2024","dron","domicilio","Cedro Rosado"],"Hola nivea")]
#mail.send_qr("Hola nisvia",'will1an@javerianacali.edu.co')
#for task in tasks:
#    task()

#mail.send_notification_loop(10, "evelynbermeovalencia@gmail.com", ["2024","dron","domicilio","Cedro Rosado"],11111)

#msg = EmailMessage()
#mail.send_mail("evelynbermeovalencia@gmail.com", msg)