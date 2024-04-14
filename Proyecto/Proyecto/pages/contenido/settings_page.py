import reflex as rx
from ...template import template



@template(route="/settings", title= "Settings")
def settings_page()-> rx.Component:
    return rx.text("settings")