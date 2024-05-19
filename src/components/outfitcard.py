from typing import Optional, Any, Union, List
from theme.themes import Themes
from components.styled_text import StyledText
from flet import Card, Image, Row, Column, Container, Padding, ImageFit, ImageRepeat, RoundedRectangleBorder, CrossAxisAlignment, ClipBehavior, FilterQuality, padding, Animation, AnimationCurve, margin
from database.cloth import Cloth
from database.outfit import Outfit
from typing import Callable


class OutfitCard(Container):
    def __init__(
        self,
        outfit: Outfit,
        width: int = 170,
        height: int = 200,
        image_height: int = 150,
        on_click=None,
        bgcolor: str = Themes.slate100,
        text_color: str = Themes.slate950,
        corner_radius: str = Themes.roundedxl,
    ):
        if (len(outfit.cloth_list) == 0):
            super().__init__(
                content=Container(
                    bgcolor=bgcolor,
                    margin=padding.all(0),
                    content=Column(
                        controls=[
                            Image(fit=ImageFit.COVER, width=width, height=image_height,
                                  repeat=ImageRepeat.NO_REPEAT, src=f"https://picsum.photos/200/200", filter_quality=FilterQuality.MEDIUM),
                            Container(
                                content=StyledText(outfit.name, size=18, color=text_color, weight=800),
                                margin=margin.symmetric(0, 15)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                border_radius=corner_radius,
                clip_behavior=ClipBehavior.ANTI_ALIAS,
                animate_scale=Animation(
                    duration=150,
                    curve=AnimationCurve.EASE_OUT_BACK,
                ),
                on_click=on_click,
                on_hover=self.on_card_hover,
                on_tap_down=self.on_card_tap,
            )
        elif (len(outfit.cloth_list) == 1):
            super().__init__(
                content=Container(
                    bgcolor=bgcolor,
                    margin=padding.all(0),
                    content=Column(
                        controls=[
                            Image(fit=ImageFit.COVER, width=width, height=image_height,
                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[0].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                            Container(
                                content=StyledText(outfit.name, size=18, color=text_color, weight=800),
                                margin=margin.symmetric(0, 15)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                border_radius=corner_radius,
                clip_behavior=ClipBehavior.ANTI_ALIAS,
                animate_scale=Animation(
                    duration=150,
                    curve=AnimationCurve.EASE_OUT_BACK,
                ),
                on_hover=self.on_card_hover,
                on_tap_down=self.on_card_tap,
                on_click=on_click
            )
        elif (len(outfit.cloth_list) == 2):
            super().__init__(
                content=Container(
                    bgcolor=bgcolor,
                    margin=padding.all(0),
                    content=Column(
                        controls=[
                            Column(
                                tight=True,
                                spacing=0,
                                controls=[
                                    Image(fit=ImageFit.COVER, width=width, height=image_height/2,
                                          repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[0].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                    Image(fit=ImageFit.COVER, width=width, height=image_height/2,
                                          repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[1].get_image_path(), filter_quality=FilterQuality.MEDIUM)
                                ]
                            ),
                            Container(
                                content=StyledText(outfit.name, size=18, color=text_color, weight=800),
                                margin=margin.symmetric(0, 15)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                border_radius=corner_radius,
                clip_behavior=ClipBehavior.ANTI_ALIAS,
                animate_scale=Animation(
                    duration=150,
                    curve=AnimationCurve.EASE_OUT_BACK,
                ),
                on_hover=self.on_card_hover,
                on_tap_down=self.on_card_tap,
                on_click=on_click
            )
        elif (len(outfit.cloth_list) == 3):
            super().__init__(
                content=Container(
                    bgcolor=bgcolor,
                    margin=padding.all(0),
                    content=Column(
                        controls=[
                            Column(
                                tight=True,
                                spacing=0,
                                controls=[
                                    Row(
                                        controls=[
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[0].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[1].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                        ],
                                        spacing=0,
                                        tight=True
                                    ),
                                    Image(fit=ImageFit.COVER, width=width, height=image_height/2,
                                          repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[2].get_image_path(), filter_quality=FilterQuality.MEDIUM)
                                ]
                            ),
                            Container(
                                content=StyledText(outfit.name, size=18, color=text_color, weight=800),
                                margin=margin.symmetric(0, 15)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                border_radius=corner_radius,
                clip_behavior=ClipBehavior.ANTI_ALIAS,
                animate_scale=Animation(
                    duration=150,
                    curve=AnimationCurve.EASE_OUT_BACK,
                ),
                on_hover=self.on_card_hover,
                on_tap_down=self.on_card_tap,
                on_click=on_click
            )
        else:
            super().__init__(
                content=Container(
                    bgcolor=bgcolor,
                    margin=padding.all(0),
                    content=Column(
                        controls=[
                            Column(
                                tight=True,
                                spacing=0,
                                controls=[
                                    Row(
                                        controls=[
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[0].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[1].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                        ],
                                        spacing=0,
                                        tight=True
                                    ),
                                    Row(
                                        controls=[
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[2].get_image_path(), filter_quality=FilterQuality.MEDIUM),
                                            Image(fit=ImageFit.COVER, width=width/2, height=image_height/2,
                                                  repeat=ImageRepeat.NO_REPEAT, src=outfit.cloth_list[3].get_image_path(), filter_quality=FilterQuality.MEDIUM)
                                        ],
                                        spacing=0,
                                        tight=True
                                    )
                                ]
                            ),
                            Container(
                                content=StyledText(outfit.name, size=18, color=text_color, weight=800),
                                margin=margin.symmetric(0, 15)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                border_radius=corner_radius,
                clip_behavior=ClipBehavior.ANTI_ALIAS,
                animate_scale=Animation(
                    duration=150,
                    curve=AnimationCurve.EASE_OUT_BACK,
                ),
                on_hover=self.on_card_hover,
                on_tap_down=self.on_card_tap,
                on_click=on_click
            )

    def on_card_hover(self, e):
        if(e.data == "true"): self.scale = 1.1
        else: self.scale = 1

        self.update()

    def on_card_tap(self, e):
        self.scale = 1.2
        self.update()