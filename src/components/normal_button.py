from flet import ElevatedButton, ButtonStyle, UrlTarget, Ref, OptionalNumber, Control, Text, RoundedRectangleBorder, MaterialState, BorderSide, padding, AnimatedSwitcher, AnimatedSwitcherTransition, AnimationCurve, Row, FilledButton, CupertinoButton, Icon
from typing import Optional, Any, Union
from theme.themes import Themes
from components.styled_text import StyledText

class NormalButton(ElevatedButton):
    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[Icon] = None,
        on_click=None,
        on_hover=None,
        bgcolor: Optional[str] = Themes.slate900,
        bg_overlay_color: Optional[str] = Themes.slate50,
        text_color: Optional[str] = Themes.slate50,
        text_overlay_color: Optional[str] = Themes.slate50,
        text_weight: int = 800,
        text_size: int = 16,
        corner_radius: OptionalNumber = Themes.roundedlg,
        disabled_bgcolor: Optional[str] = Themes.indigo600,
        height = 43,
        text_padding = padding.symmetric(15, 25),
    ):
        self.text_content = StyledText(text, color=text_color, weight=text_weight, size=text_size)
        self.icon_content = icon
        self.icon_content.scale = 0.85
        super().__init__(
            bgcolor=bgcolor,
            content=Row(
                spacing=6,
                controls=[
                    self.icon_content,
                    self.text_content,
                ]
            ) if icon else self.text_content
            ,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=corner_radius),
                overlay_color=bg_overlay_color,
                animation_duration=150,
                padding=padding.only(15, 15, 25, 15) if icon else text_padding,
                elevation=0,
            ),
            elevation=0,
            on_click=on_click,
            on_hover=self.on_button_hover,
            icon=icon,
            height=height,
        )
        self.on_hover_from_outside = on_hover
        self.disabled_bgcolor = disabled_bgcolor
        self.default_bgcolor = bgcolor
        self.bg_overlay_color = bg_overlay_color
        self.text_overlay_color = text_overlay_color
        self.text_color = text_color
        self.style_disabled = False

    def on_button_hover(self, e):
        if self.style_disabled: return
        if e.data == "true":
            self.text_content.color = self.text_overlay_color
            if self.icon_content: self.icon_content.color = self.text_overlay_color
        else:
            self.text_content.color = self.text_color
            if self.icon_content: self.icon_content.color = self.text_color
            
        if self.on_hover_from_outside: self.on_hover_from_outside(e)
        self.update()
        # self.text_content.update()
        # if self.icon_content: self.icon_content.update()

    def set_disabled(self, is_disabled: bool):
        self.style_disabled = is_disabled
        # self.disabled = is_disabled
        if self.style_disabled:
            self.bgcolor = self.disabled_bgcolor
            self.style.overlay_color = self.disabled_bgcolor
            self.text_content.color = self.text_color
            if(self.icon_content): self.icon_content.color = self.text_color
        else:
            self.bgcolor = self.default_bgcolor
            self.style.overlay_color = self.bg_overlay_color
            self.text_content.color = self.text_color
            if(self.icon_content): self.icon_content.color = self.text_color
        self.update()
        # self.text_content.update()
        # if self.icon_content: self.icon_content.update()
