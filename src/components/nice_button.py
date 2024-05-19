from flet import ElevatedButton, ButtonStyle, UrlTarget, Ref, OptionalNumber, Control, Text, RoundedRectangleBorder, MaterialState, BorderSide, padding, AnimatedSwitcher, AnimatedSwitcherTransition, AnimationCurve, Container, Animation, Icon, Row, Column, MainAxisAlignment, alignment
from typing import Optional, Any, Union
from theme.themes import Themes
from components.normal_button import NormalButton
from components.styled_text import StyledText

class NiceButton(Container):
    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[Icon] = None,
        on_click=None,
        bgcolor: Optional[str] = Themes.slate900,
        bg_overlay_color: Optional[str] = Themes.slate50,
        text_color: Optional[str] = Themes.slate50,
        text_overlay_color: Optional[str] = Themes.slate50,
        text_weight: int = 800,
        corner_radius: OptionalNumber = Themes.roundedlg,
        disabled_bgcolor: Optional[str] = Themes.indigo600,
        content_padding = padding.symmetric(12, 18),
        height = None,
        text_size = 14,
        expand=False,
        overlay_scale=Themes.scalelg,
        tap_scale=Themes.scalexl,
    ):
        self.text_content = StyledText(text, color=text_color, weight=text_weight, size=text_size)
        self.icon_content = icon
        self.bg_default_color = bgcolor
        self.bg_overlay_color = bg_overlay_color
        self.overlay_scale = overlay_scale
        self.tap_scale = tap_scale
        self.text_overlay_color = text_overlay_color
        self.text_color = text_color

        super().__init__(
            animate_scale=Animation(
                duration=150,
                curve=AnimationCurve.EASE_OUT_BACK,
            ),
            bgcolor=bgcolor,
            content=Row(
                spacing=4,
                controls=[
                    self.icon_content,
                    self.text_content,
                ],
            ) if icon else self.text_content,
            border_radius=corner_radius,
            on_tap_down=self.button_on_tap,
            on_click=on_click,
            height=height,
            on_hover=self.button_on_hover,
            padding=content_padding,
            expand=expand,
            alignment=alignment.center,
        )

    def button_on_hover(self, e):
        if e.data == "true": 
            self.scale = self.overlay_scale
            self.bgcolor = self.bg_overlay_color
            self.text_content.color = self.text_overlay_color
        else: 
            self.scale = Themes.scaledefault
            self.bgcolor = self.bg_default_color
            self.text_content.color = self.text_color
        self.update()

    def button_on_tap(self, e):
        self.scale = self.tap_scale
        self.update()

    