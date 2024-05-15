from flet import Container, Image, Column, ButtonStyle, RoundedRectangleBorder, padding, alignment, ImageFit, Container, MainAxisAlignment, CrossAxisAlignment, Animation, AnimationCurve, Row, Stack, StackFit, ResponsiveRow
from database.cloth import Cloth
from database.tag import Tag
from theme.themes import Themes
from components.styled_text import StyledText
from components.normal_button import NormalButton
from components.small_button import SmallButton
from typing import Callable

class ClothCard(Container):
    def __init__(
        self,
        cloth: Cloth,
        width: int = 170,
        height: int = 200,
        image_height: int = 130,
        on_click=None,
        bgcolor: str = Themes.slate100,
        text_color: str = Themes.slate950,
        corner_radius: str = Themes.roundedxl,
        content_padding: int = 12,
        on_tag_clicked: Callable[[Tag], None]=None
    ):
        self.on_tag_clicked = on_tag_clicked
        super().__init__(
            bgcolor=bgcolor,
            margin=padding.all(0),
            padding=padding.all(0),
            content=Column(
                controls=[
                    
                    Container(
                        content=Image(cloth.get_image_path(), fit=ImageFit.COVER),
                        height=image_height,
                        width=width,
                    ),
                    Container(
                        padding=padding.only(content_padding, 0, content_padding, content_padding),
                        content= Column(
                            spacing=5,
                            controls=[
                                Container(
                                    content=StyledText(cloth.name, weight=800, size=18),
                                ),
                                Row(
                                    controls=[
                                        SmallButton(tag.name, 
                                                    text_padding=padding.symmetric(2, 6), 
                                                    corner_radius=Themes.roundedmd, 
                                                    text_weight=700,
                                                    text_size=11,
                                                    on_click=lambda e, tag=tag: self.on_tag_button_clicked(e, tag)
                                                    )
                                        for tag in cloth.tag_list
                                    ],
                                    spacing=3,
                                    wrap=True,
                                    width=width-content_padding*2,
                                    run_spacing=3,
                                )
                            ],
                        ),                    

                    )
                    
                ],
            ),
            
            border_radius=corner_radius,
            on_click=on_click,
            on_hover=self.on_card_hover,
            animate_scale=Animation(
                duration=150,
                curve=AnimationCurve.EASE_OUT_BACK,
            ),
            width=width,
            on_tap_down=self.on_card_tap,
        )

    def on_card_hover(self, e):
        if(e.data == "true"): self.scale = 1.1
        else: self.scale = 1

        self.update()

    def on_tag_button_clicked(self, e, tag):
        if self.on_tag_clicked:
            self.on_tag_clicked(tag)

    def on_card_tap(self, e):
        self.scale = 1.2
        self.update()