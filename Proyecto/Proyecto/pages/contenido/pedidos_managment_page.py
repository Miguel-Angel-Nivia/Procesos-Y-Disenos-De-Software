import reflex as rx
from ...services.pedidos_service import PedidoManagment
from ...template import template
from ...services.conexion_db import Comunicacion
from ...styles.style_page import style_login, accent_color 

manager = PedidoManagment()
conexion = Comunicacion()

class PedidosState(rx.State):
    loader: bool = False
    error = False
    response = False
    id_usuario_envio: int
    id_usuario_receptor: int
    id_dispositivo: str
    tipo_encargo :str
    descripcion: str
    fecha_temporal_recepcion:str
    hora_entrega:str
    lugar_recepcion:str
    peso:float
    @rx.background
    async def PedidoService(self, data: dict):
        async with self:
            self.loader = True
            self.error = False
            response = manager.crear_pedido(data)
            #response = True
            #print(data)
            if response:
                self.response = response
                self.loader = False
            else:
                self.loader = False
                self.error = True
    @rx.var
    def validate_fields(self) -> bool:
        return (not self.tipo_encargo.strip() and
                not self.descripcion.strip() and
                not self.fecha_temporal_recepcion.strip() and
                not self.hora_entrega.strip() and
                not self.fecha_temporal_recepcion.strip() and
                not self.lugar_recepcion.strip())

@template(route = "/Administracion_pedidos", title="Administracion_Pedidos")
def pedidos_managment_page() -> rx.Component:
    return rx.box(
        rx.text("Crear Encargo"),
        rx.flex(
            rx.form.root(
                rx.flex(
                    pedido_form("id_usuario emisor", "Ingrese id cliente",
                                "id_usuario_envio",
                                PedidosState.set_id_usuario_envio,"text"),
                    pedido_form("id_usuario receptor", "Ingrese id cliente",
                                "id_usuario_receptor",
                                PedidosState.set_id_usuario_receptor,"text"),
                    desplegable("Tipo de Encargo",["PEDIDO","GRABACION"], "tipo_encargo", PedidosState.set_tipo_encargo),
                    rx.cond(PedidosState.tipo_encargo == "PEDIDO",
                            desplegable("Peso paquete", ["-1.5","+1.5"],"peso", PedidosState.set_peso),
                            rx.text("GRABACION")),
                    rx.cond(PedidosState.tipo_encargo == "PEDIDO",
                            rx.cond(PedidosState.peso < 1.5,
                                desplegable("Dispositivo Disponible", manager.get_all_free_device(), "id_dispositivo"),
                                desplegable("Dispositivo Disponible", manager.obtener_dispositivo_disponible("ROBOT"), "id_dispositivo"),
                            ),
                            desplegable("Dispositivo Disponible", manager.obtener_dispositivo_disponible("DRON"), "id_dispositivo"),
                    ),
                    # rx.select(rx.cond(PedidosState.tipo_encargo == "PEDIDO",
                    #             rx.cond(PedidosState.peso == "+1.5",
                    #                     manager.obtener_dispositivo_disponible("ROBOT"),
                    #                     manager.get_all_free_device()),
                    #             manager.obtener_dispositivo_disponible("DRON")
                    # ),
                    # name = "id_dispositivo"),
                    pedido_form("Descripcion", "Ingrese una breve descripcion del pedido",
                                "descripcion", PedidosState.set_descripcion,"text"),
                    pedido_form("Fecha Entrega", "Seleccione fecha", "fecha_temporal_recepcion",
                                PedidosState.set_fecha_temporal_recepcion, "date"),
                    pedido_form("Hora_entrega", "Seleccione hora", "hora_entrega",
                                PedidosState.set_hora_entrega, "time"),
                    desplegable("Lugar Entrega",["Cedro Rosado", "Palmas", "El lago", "Guayacanes","Almendros"], "lugar_recepcion"),
                    rx.form.submit(
                        rx.cond(
                            PedidosState.loader,
                            rx.chakra.spinner(color = "red", size = "xs"),
                            rx.button(
                                "Crear Pedido",
                                disabled = PedidosState.validate_fields,
                                width = "30vm"
                            ),
                        ),
                        as_child= True,
                    ),
                    direction="column",
                    justify="between",
                    align="center",
                    wrap="wrap",
                    spacing="2",
                ),
                rx.cond(
                    PedidosState.error,
                    rx.callout(
                        "Campos invalidos",
                        icon = "triangle_alert",
                        color_scheme = "red",
                        role = "alert",
                        style = {"margin_top":"10px"},
                    ),
                ),
                rx.cond(
                    PedidosState.response,
                    rx.callout(
                        "Pedido Creado",
                        color_scheme = "green",
                        role = "info",
                        style = {"margin_top":"10px"},
                    ),
                ),
                on_submit=PedidosState.PedidoService,
                reset_on_submit=True,
                width = "80%",
            ),
            width = "100%",
            direction = "column",
            align = "center",
            justify="between",
            wrap= "wrap"
        ),
        style = style_login,
        justify = "center",
        width = "100%",
    )

def desplegable(label, lista, name_var, on_change = None):
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.select( lista, name= name_var,
                       on_change=on_change,
                       color = accent_color,
                       variant="soft",
                       radius="full"),
            direction="row",
            wrap="nowrap",
            align = "baseline",
        ),
        name=name_var,
        width = "30vw"
    )
def pedido_form(label:str, placeholder: str, name_var: str,
               on_change_function, type_field:str) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder = placeholder,
                    on_change = on_change_function,
                    name = name_var,
                    type = type_field,
                    required =True,
                ),
                as_child=True,
            ),
            rx.form.message(
                "El campo no puede ser nulo",
                match = "valueMissing",
                color = "red",
            ),
            direction="column",
            align = "stretch",      
        ),
        name=name_var,
        width = "30vw"
    )
