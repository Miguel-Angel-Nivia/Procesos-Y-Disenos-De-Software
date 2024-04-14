import reflex as rx



@rx.page(route="/login",title="login")
def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.text("Aqui va el login")
                ),
                rx.image(src="/pujc-logo.svg"),
            ),
            rx.text("Aqui sigue lo demas"),
            rx.button("Vamos al menu principal", on_click=rx.redirect("/home")),
        )
    )