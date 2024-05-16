from time import sleep
from flet import Container, Image, Column, margin, Row, alignment, Stack, padding, MainAxisAlignment, Icon, icons, Animation, AnimationCurve, Control, CrossAxisAlignment
from theme.themes import Themes
from components.nice_button import NiceButton
from components.styled_text import StyledText
from components.small_button import SmallButton
from typing import List
class Dialog(Container):
    animation_duration: int = 150

    def show(self, title: str, content: Container = None, bottom_controls: List[Control] = None):
        self.title_text.value = title

        if content:
            self.dialog_content.content = content
        if bottom_controls:
            self.bottom_controls = bottom_controls
            self.bottom_row.controls = bottom_controls
            self.bottom_row.update()

        self.visible = True
        self.update()

        sleep(0.05)
        self.main_dialog.scale = 1
        self.main_dialog.opacity = 1
        self.background.opacity = 0.5
        self.main_dialog.update()
        self.background.update()

    def close(self):
        self.main_dialog.scale = 0.5
        self.main_dialog.opacity = 0
        self.background.opacity = 0
        self.main_dialog.update()
        self.background.update()

        sleep(Dialog.animation_duration / 1000)
        self.visible = False
        self.update()

    def __init__(
        self,
        title: str = "title",
        content: Container = Container(),
        visible=False,
        bottom_controls: list[Control] = [],
        width = None,
        height = None,
        margin = margin.symmetric(50, 100),
    ):
        self.dialog_content: Container = Container()
        self.bottom_controls = bottom_controls
        self.bottom_row = Row(
            controls=bottom_controls,
            alignment=MainAxisAlignment.END,
        )
        self.dialog_content.content = content
        self.title_text = StyledText(title, color=Themes.slate950, weight=800, size=25)
        self.background = Container(
            expand=True,
            bgcolor=Themes.slate950,
            opacity=0,
            animate_opacity=Animation(
                duration=Dialog.animation_duration,
                curve=AnimationCurve.EASE_OUT_QUART,
            ),
            on_click=lambda e: self.close()
        )
        self.main_dialog = Container(
            bgcolor= Themes.slate200,
            padding= padding.all(20),
            border_radius= Themes.rounded2xl,

            width= width if width and height else None, 
            height= height if width and height else None,
            expand=False if width and height else True,

            scale=0.5,
            animate_scale=Animation(
                duration=Dialog.animation_duration,
                curve=AnimationCurve.EASE_OUT_BACK,
            ),
            opacity=0,
            animate_opacity=Animation(
                duration=Dialog.animation_duration,
                curve=AnimationCurve.EASE_OUT_QUART,
            ),
            content=Column(
                controls=[
                    
                    Stack(
                        controls=[
                            Row(
                                controls=[
                                    self.title_text,
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            Container(
                                content=SmallButton(
                                    text="",
                                    icon=Icon(icons.CLOSE_ROUNDED, Themes.slate950, size=20), 
                                    text_color=Themes.slate950,
                                    bgcolor=Themes.slate50,
                                    text_overlay_color=Themes.slate950,
                                    text_padding=padding.all(10),
                                    bg_overlay_color=Themes.slate300,
                                    on_click=lambda e: self.close()
                                ),
                                width=40,
                                height=40,
                                right=0,
                            )
                        ],
                        height=50,
                    ),
                    Container(
                        content=self.dialog_content,
                        expand=True
                    ),
                    self.bottom_row
                    ,
                ]
            ),

            
        )
        self.content_row = Row(
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        # dialog
                        self.main_dialog
                    ],
                    expand=True,
                )
            ],
            expand=True,
        )
        super().__init__(
            visible=visible,
            content=Stack(
                controls=[
                    # background
                    self.background,

                    self.content_row 
                    if width and height else
                    Container(
                        content=self.content_row,
                        margin=margin,
                        expand=True,
                    )

                ],
            )
        )