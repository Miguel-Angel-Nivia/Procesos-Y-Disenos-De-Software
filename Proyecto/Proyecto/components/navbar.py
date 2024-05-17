import reflex as rx
from ..styles import style_page


def navbar_header() -> rx.Component:
   return rx.box(
        # The logo.
        rx.center(rx.image(src=rx.color_mode_cond("/pujc-logo.svg","/pujc-logo-dark.jpg"),
                             height="100px", width = "100px", align = "center")),
                            
        align="center",
        width="100%",
        border_bottom=style_page.border,
        padding_x="1em",
        padding_y="2em"
        
    )


def navbar_footer() -> rx.Component:
    return rx.hstack(
        rx.spacer(),
        rx.link(
            rx.text("GitHub"),
            href="https://github.com/Miguel-Angel-Nivia/Procesos-Y-Disenos-De-Software/tree/main/Proyecto",
            is_external=True,
        )
    )

def navbar_content(text:str, url:str) -> rx.Component:
    active = (rx.State.router.page.path == f"/{text.lower()}")|(
        (rx.State.router.page.path == "/") & text == "Home")
    return rx.link(
        rx.hstack(
            rx.text(
                text,
            ),
            bg = rx.cond(
                active,
                rx.color("accent", 2),
                "transparent",
            ),
            border = rx.cond(
                active,
                f"1px solid {rx.color('accent',6)}",
                f"1px solid {rx.color('gray',6)}",
            ),
            color = rx.cond(
                active,
                #estilos
                style_page.accent_text_color,
                style_page.text_color,
            ),
            align = "center",
            border_radius = style_page.border_radius,
            width = "100%",
            padding = "1em",
        ),
        href = url,
        width = "100%",
    )

def navbar() -> rx.Component:
    from reflex.page import get_decorated_pages
    paginas_disponibles = ["home","dashboard","settings","pedidos", "Administracion_pedidos"]
    return rx.box(
        rx.vstack(
            navbar_header(),
            rx.vstack(
                *[
                    navbar_content(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        url= page["route"],
                    )
                    for page in get_decorated_pages()
                    if page["route"].strip("/") in paginas_disponibles
                ],
                width = "100%",
                overflow_y = "auto",
                align_items = "flex_start",
                padding = "1em",
            ),
            rx.spacer(),
            navbar_footer(),
            height = "100dvh",
        ),
        display = ["none","none","block"],
        min_width = style_page.navbar_width,
        height = "100%",
        position = "sticky",
        top = "0px", 
        border_right = style_page.border,
    )