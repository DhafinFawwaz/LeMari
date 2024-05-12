from flet import ElevatedButton, ButtonStyle, UrlTarget, Ref, OptionalNumber, Control, Text, RoundedRectangleBorder, MaterialState, BorderSide, padding, AnimatedSwitcher, Container, AnimatedSwitcherTransition, AnimationCurve, Row, Column, margin, alignment
from typing import Optional, Any, Union, List
from theme.themes import Themes
from components.normal_button import NormalButton


# left side bar navigation menu
class Navbar(Container):
    def __init__(self, buttons: List[NormalButton], controls: List[Control], sidebar_content: Container, sidebar_width: OptionalNumber = 350, sidebar_color: str = Themes.slate900, content_color: str = Themes.slate300, padding=padding.only(15, 5, 15, 15)):
        super().__init__(
            content=Row(
                controls=[
                    # Sidebar
                    Container(
                        bgcolor=sidebar_color,
                        padding=padding,
                        content= Column(
                            controls=[
                                sidebar_content,
                                Column(
                                    controls=buttons,
                                )
                            ],
                            spacing=0,
                            width=sidebar_width,
                        ),
                    ),
                    
                    # Page Content
                    Container(
                        bgcolor=content_color,
                        expand=True,
                        content=Column(
                            controls=controls,
                            spacing=0,
                        ),
                    )
                    
                ],
                spacing=0,
                expand=True
            ),
            bgcolor=Themes.slate50,
            margin=margin.all(0),
            expand=True,
        )
        self.controls = controls
        self.buttons = buttons
        for menu in controls:
            menu.visible = False

        for i in range(len(buttons)):
            buttons[i].on_click = lambda e, i=i: self.switch_menu(i)
        controls[0].visible = True
        # buttons[0].disabled = True
        # buttons[0].set_disabled(True)

    def switch_menu(self, index):
        for i in range(len(self.controls)):
            self.controls[i].visible = i == index
            # self.buttons[i].disabled = i == index
            self.buttons[i].set_disabled(i == index)
        self.update()