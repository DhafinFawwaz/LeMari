from flet import ElevatedButton, ButtonStyle, UrlTarget, Ref, OptionalNumber, Control, Text, RoundedRectangleBorder, MaterialState, BorderSide, padding, AnimatedSwitcher, AnimatedSwitcherTransition, AnimationCurve, Container, Animation
from typing import Optional, Any, Union
from theme.themes import Themes
from components.normal_button import NormalButton

class NiceButton(Container):
    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[str] = None,
        on_click=None,
        bgcolor: Optional[str] = Themes.slate900,
        overlay_color: Optional[str] = Themes.slate50,
        text_color: Optional[str] = Themes.slate50,
        text_overlay_color: Optional[str] = Themes.slate50,
        text_weight: int = 800,
        corner_radius: OptionalNumber = Themes.roundedlg,
        disabled_bgcolor: Optional[str] = Themes.indigo600,
    ):
        self.button = NormalButton(
            text=text,
            icon=icon,
            on_click=on_click,
            on_hover=self.on_hover,
            bgcolor=bgcolor,
            bg_overlay_color=overlay_color,
            text_color=text_color,
            text_overlay_color=text_overlay_color,
            text_weight=text_weight,
            corner_radius=corner_radius,
            disabled_bgcolor=disabled_bgcolor
        )
        super().__init__(
            content=self.button,
            animate_scale=Animation(
                duration=150,
                curve=AnimationCurve.EASE_OUT_BACK,
            ),
            on_click=self.on_tap,
            on_tap_down=self.on_tap,
        )

    def on_hover(self, e):
        if e.data == "true": self.scale = Themes.scalelg
        else: self.scale = Themes.scaledefault
        self.update()

    def on_tap(self, e):
        self.scale = Themes.scalexl
        self.update()

    def set_on_click(self, on_click):
        self.button.on_click = on_click
    