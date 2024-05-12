from time import sleep
from flet import Container, Image, Column, margin, Row, alignment, Stack, padding, MainAxisAlignment, Icon, icons, Animation, AnimationCurve
from theme.themes import Themes
from components.nice_button import NiceButton
from components.styled_text import StyledText

class Dialog(Container):
    animation_duration: int = 150

    def show(self, title: str, content: Container):
        self.title_text.value = title
        self.dialog_content.content = content

        self.visible = True
        self.update()

        sleep(0.05)
        self.main_dialog.scale = 1
        self.main_dialog.opacity = 1
        self.background.opacity = 0.5
        self.main_dialog.update()
        self.background.update()

    def close(self, e):
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
    ):
        self.dialog_content: Container = Container()
        self.dialog_content.content = content
        self.title_text = StyledText(title, color=Themes.slate950, weight=800, size=25)
        self.background = Container(
            expand=True,
            bgcolor= Themes.slate950,
            opacity=0,
            animate_opacity=Animation(
                duration=Dialog.animation_duration,
                curve=AnimationCurve.EASE_OUT_QUART,
            ),
        )
        self.main_dialog = Container(
            bgcolor= Themes.slate200,
            padding= padding.all(20),
            border_radius= Themes.rounded2xl,
            width= 360, height= 200,
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
                    Row(
                        controls=[
                            self.title_text,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    self.dialog_content,
                    Container(
                        expand=True
                    ),
                    Row(
                        controls=[
                            NiceButton("OK", on_click=self.close, bgcolor=Themes.rose600, overlay_color=Themes.rose500, text_color=Themes.slate50),
                        ],
                        alignment=MainAxisAlignment.END,
                    ),
                ]
            ),

            
        )
        super().__init__(
            visible=False,
            content=Stack(
                controls=[
                    # background
                    self.background,

                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    # dialog
                                    self.main_dialog
                                ],
                            )
                        ]
                    ),
                ],
            )
        )