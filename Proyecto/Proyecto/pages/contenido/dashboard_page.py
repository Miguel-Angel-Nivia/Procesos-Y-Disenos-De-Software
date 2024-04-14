import reflex as rx
from ...template import template



@template(route="/dashboard", title= "Dashboard")
def dashboard_page()-> rx.Component:
    return rx.text("Dashboard")