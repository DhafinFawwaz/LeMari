from typing import Optional, Any, Union, List
from theme.themes import Themes
from components.styled_text import StyledText
from flet import Card, Image, Row, Column, Container, Padding, ImageFit, ImageRepeat, RoundedRectangleBorder, CrossAxisAlignment, ClipBehavior, FilterQuality, padding
from database.cloth import Cloth
from database.outfit import Outfit
from typing import Callable


class OutfitCard(Card):
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
                            StyledText(
                                outfit.name, size=18, color=text_color, weight=800),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                shape=RoundedRectangleBorder(radius=corner_radius),
                clip_behavior=ClipBehavior.ANTI_ALIAS
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
                            StyledText(
                                outfit.name, size=18, color=text_color, weight=800),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                shape=RoundedRectangleBorder(radius=corner_radius),
                clip_behavior=ClipBehavior.ANTI_ALIAS
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
                            StyledText(
                                outfit.name, size=18, color=text_color, weight=800),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                shape=RoundedRectangleBorder(radius=corner_radius),
                clip_behavior=ClipBehavior.ANTI_ALIAS
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
                            StyledText(
                                outfit.name, size=18, color=text_color, weight=800),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                shape=RoundedRectangleBorder(radius=corner_radius),
                clip_behavior=ClipBehavior.ANTI_ALIAS
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
                            StyledText(
                                outfit.name, size=18, color=text_color, weight=800),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    width=width,
                    padding=Padding(0, 0, 0, 12),
                ),
                shape=RoundedRectangleBorder(radius=corner_radius),
                clip_behavior=ClipBehavior.ANTI_ALIAS
            )