import reflex as rx
from ...template import template



@template(route= "/home", title="home")
def home_page() -> rx.Component:
    return rx.container(
        rx.text("home"),
    )