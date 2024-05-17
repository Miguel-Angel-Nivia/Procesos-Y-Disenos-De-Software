import reflex as rx
from datetime import datetime
from ...template import template
from typing import List, Dict, Tuple
from ...services.pedidos_service import PedidoManagment
from ...styles.style_page import accent_color

manager = PedidoManagment()

class PedidoState(rx.State):
    pedidos: List[tuple] = []
    state:bool = True
    selected_pedido = ''
    @rx.background
    async def cargar_pedidos(self):
        async with self:
            self.pedidos, self.state = manager.obtener_pedidos()
    @rx.background
    async def select_pedido(self, id):
            response = await manager.activacion(id["selected_pedido"])

    @rx.var
    def id_pedido_empty(self) -> bool:
        return not self.selected_pedido.strip()
    
    def set_selected_pedido( self, id: str):
        set_selected_pedido = id
    

@template(route="/pedidos", title="Pedidos")
def pedidos_page() -> rx.Component:
    return rx.box(rx.cond(PedidoState.state,
                        rx.section(
                            rx.heading("Lista de Pedidos"),
                            rx.flex(
                                rx.foreach(PedidoState.pedidos, generar_tarjeta),
                                display="flex",
                                flex_direction="row",
                                align_items="center",
                                wrap="wrap"
                            ),
                            rx.flex(
                                rx.form(
                                    rx.vstack(
                                    rx.input(
                                        placeholder="ID Encargo",
                                        name = "selected_pedido",
                                    ),
                                    rx.button("Activar", type = "submit"),
                                    ),
                                    on_submit=PedidoState.select_pedido,
                                    reset_on_submit=True,
                                ),
                            )       
                        ),

                        rx.text("Aun no hay pedidos", color_scheme="red")
                    ),
        on_mount=PedidoState.cargar_pedidos
    )


def generar_tarjeta(pedido) -> rx.Component:
    color = {
        "activo" : "green",
        "reserva" : "gray",
        "salida" :"yellow",
        "proximidad" : "yellow",
        "llegada" : "blue",
        "codigo" : "blue",
        "entrega" : "green"
    }.get(pedido[7], "gray")
    return rx.card(
        rx.text(f"fecha_solicitud: {pedido[0]}"),
        rx.text(f"fecha_recepcion: {pedido[1]}"),
        rx.text(f"De:{pedido[2]}"),
        rx.text(f"Para:{pedido[3]}"),
        rx.text(f"Dispositivo:{pedido[4]}"),
        rx.text(f"Recepcion:{pedido[5]}"),
        rx.text(f"ID: {pedido[6]}"),
        rx.text(f"Estado: {pedido[7]}"),
        bg=color,
        style={
            "border": "1px solid #ccc",
            "padding": "10px",
            "margin": "10px",
            "borderRadius": "5px",
            "cursor": "pointer"
        },
        on_click = PedidoState.set_selected_pedido(pedido[6]),
    )