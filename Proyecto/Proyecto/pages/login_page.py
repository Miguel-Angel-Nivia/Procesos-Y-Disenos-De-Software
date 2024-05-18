import reflex as rx
from ..services.login_service import autentication
from ..styles.style_page import style_login
import re
class LoginState(rx.State):
    loader: bool = False
    username: str = "exampleUser"
    password: str
    error = False
    response = False
    password_invalid_length: bool = False
    password_invalid_upper: bool = False
    password_invalid_digit: bool = False
    password_invalid_symbol: bool = False

    @rx.background
    async def loginService(self, data: dict):
        async with self:
            self.loader = True
            self.error = False
            response =  autentication(data)
            if response == True:
                self.response = response
                self.loader = False
                return rx.redirect("/home")
            else:
                self.loader = False
                self.error = True
    @rx.var
    def user_empty(self) -> bool:
        return not self.username.strip()
    @rx.var
    def password_empty(self) ->bool:
        return not(self.password.strip())
    

    def validate_password(self):
        self.password_invalid_length = len(self.password) < 16
        self.password_invalid_upper = not re.search(r"[A-Z]", self.password)
        self.password_invalid_digit = not re.search(r"[0-9]", self.password)
        self.password_invalid_symbol = not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password)

    @rx.var
    def password_invalid(self) -> bool:
        self.validate_password()
        return (
            self.password_invalid_length
            or self.password_invalid_upper
            or self.password_invalid_digit
            or self.password_invalid_symbol
        )

    @rx.var
    def validate_fields(self) -> bool:
        return(
            self.user_empty
            or self.password_empty
            or self.password_invalid
        )

@rx.page(route="/login",title="login")
def login_page() -> rx.Component:
    return rx.section(
        rx.flex(
            rx.image(src = rx.color_mode_cond("/pujc-logo.svg","/pujc-logo-dark.jpg"), border = "15px", height = "200px", width = "200px"),
            rx.heading("Inicio de sesion"),
            rx.form.root(
                rx.flex(
                    form_login_general("Usuario", "Ingrese su usuario",
                            "Ingrese un usuario valido", "username",
                            LoginState.set_username, LoginState.user_empty),
                    form_login("Contrasenia", "Ingrese su contrasenia", "password",
                               LoginState.set_password, "password"),
                    rx.form.submit(
                        rx.cond(
                            LoginState.loader,
                            rx.chakra.spinner(color = "red", size = "xs"),
                            rx.button(
                                "Iniciar Sesion",
                                disabled = LoginState.validate_fields,
                                width = "30vw"
                            ),
                        ),
                        as_child= True,
                    ),
                    direction="column",
                    justify="center",
                    align="center",
                    spacing="2",
                ),
                rx.cond(
                    LoginState.error,
                    rx.callout(
                        "Credenciales incorrectas",
                        icon = "triangle_alert",
                        color_scheme = "red",
                        role = "alert",
                        style = {"margin_top":"10px"},
                    ),
                ),
                on_submit=LoginState.loginService,
                reset_on_submit=True,
                width = "80%",
            ),
            width = "100%",
            direction = "column",
            align = "center",
            justify="center",
        ),
        style = style_login,
        justify = "center",
        width = "100%",
    )


def form_login(label:str, placeholder: str, name_var: str,
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
            spacing= "2",
            align = "stretch",      
        ),
        name=name_var,
        width = "30vw"
    )
def form_login_general(label:str, placeholder:str, message_validate: str, name: str,
                       on_change_function, show) -> rx. Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder = placeholder,
                    on_change = on_change_function,
                    name = name,
                    required = True
                ),
                as_child= True
            ),
            rx.form.message(
                message_validate,
                name = name,
                match = "valueMissing",
                force_match = show,
                color = "red"
            ),
        direction = "column",
        spacing = "2",
        align = "stretch"
        ),
        name = name,
        width = "30vw"
    )
