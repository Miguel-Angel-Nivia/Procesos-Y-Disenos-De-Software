import reflex as rx






@rx.page(route="/", title="Index")
def index_page() -> rx.Component:
    return rx. center(
        rx.vstack(
            rx.text("Bienvenido al proyecto"),
            rx.text("Vamos a editar el proyecto"),
            rx.button("Empezar", on_click=rx.redirect("/login"))
        )
    )