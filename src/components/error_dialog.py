from time import sleep
from flet import Container, Image, Column, margin, Row, alignment, Stack, padding, MainAxisAlignment, Icon, icons, Animation, AnimationCurve
from theme.themes import Themes
from components.nice_button import NiceButton
from components.styled_text import StyledText
from components.dialog import Dialog

class ErrorDialog(Dialog):
    def __init__(
        self,
        title: str = "title",
        content: Container = Container(),
    ):
        super().__init__(
            visible=False,
            bottom_controls=[
                NiceButton("OK", on_click=lambda e: self.close(), bgcolor=Themes.blue600, bg_overlay_color=Themes.blue500, text_color=Themes.slate50, expand=True, tap_scale=1.1, overlay_scale=1.07),
            ],
            title=title,
            content=content,
            width=360,
            height=200,
        )