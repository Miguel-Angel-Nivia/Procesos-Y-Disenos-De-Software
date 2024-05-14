import reflex as rx
from ...template import template, ThemeState



@template(route="/settings", title= "Settings")
def settings_page()-> rx.Component:
    def select_color()->rx.Component:
        return rx.block(rx.hstack(
            rx.text("Primary color: "),
            rx.select(
                [
                    "tomato",
                    "red",
                    "ruby",
                    "crimson",
                    "pink",
                    "plum",
                    "purple",
                    "violet",
                    "iris",
                    "indigo",
                    "blue",
                    "cyan",
                    "teal",
                    "jade",
                    "green",
                    "grass",
                    "brown",
                    "orange",
                    "sky",
                    "mint",
                    "lime",
                    "yellow",
                    "amber",
                    "gold",
                    "bronze",
                    "gray",
                ],
                value=ThemeState.accent_color,
                on_change=ThemeState.set_accent_color,
            ),
        ),
        rx.hstack(
            rx.text("Secondary color: "),
            rx.select(
                [
                    "gray",
                    "mauve",
                    "slate",
                    "sage",
                    "olive",
                    "sand",
                ],
                value=ThemeState.gray_color,
                on_change=ThemeState.set_gray_color,
            ),
        )
        )
    return rx.vstack(
        rx.heading("Settings", size="8"),
        rx.hstack(
            rx.text("Dark mode: "),
            rx.color_mode.switch(),
        ),
    )