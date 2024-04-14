"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx
from .pages import *

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return index_page()
    


app = rx.App()
app.add_page(index)
