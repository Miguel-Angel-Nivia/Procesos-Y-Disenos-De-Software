import reflex as rx


border_radius = "0.375rem"
border = f"1px solid {rx.color('gray', 6)}"
text_color = rx.color("gray", 11)
accent_text_color = rx.color("accent", 10)
accent_color = rx.color("accent", 1)
hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_color}}
content_width_vw = "90vw"
navbar_width = "20em"
sidebar_witdh = "20em"

template_page_style = {"padding_top": "5em", "padding_x": ["auto", "2em"], "flex": "1"}

template_content_style = {
    "align_items": "flex-start",
    "border_radius": border_radius,
    "padding": "1em",
    "margin_bottom": "2em",
    "min_height":"90vh",
}

link_style = {
    "color": accent_text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border_radius": border_radius,
}


# style login
style_login = {
    "height" :"90vh",
    "width" : "80%",
    "margin":"auto",
}