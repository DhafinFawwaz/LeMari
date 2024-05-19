from flet import Container, Stack, alignment, margin, padding, Column, Row, Text, Image, MainAxisAlignment, ScrollMode
from theme.themes import Themes
from components.normal_button import NormalButton
from components.styled_text import StyledText

class AboutPage(Container):

    def __init__(self):
        super().__init__(
            margin=margin.all(0),
            padding=padding.all(0),
            expand=True,
            content=Stack(
                controls=[
                    # Actual content
                    Container(
                        padding=padding.all(80),
                        content=Row(
                            controls=[
                                Container(
                                    content=Image(
                                        src="../assets/our_image.png",  # Update this path as needed
                                        fit="contain",
                                    ),
                                    expand=True,
                                    alignment=alignment.center,
                                    padding=padding.all(10),
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Container(
                                                content=StyledText(
                                                    "Le Mari",
                                                    size=48,
                                                    weight=800,
                                                    color=Themes.slate900,
                                                ),
                                                alignment=alignment.center, 
                                                padding=padding.only(bottom=10),
                                            ),
                                            Container(
                                                content=Column(
                                                    scroll=ScrollMode.AUTO,
                                                    controls=[
                                                        StyledText(
                                                            "Le Mari is a wardrobe app that helps you organize and manage your clothing items. Easily add new clothes, categorize them with tags, and keep track of your wardrobe. Our app makes it simple to find the perfect outfit for any occasion.\n\n Here is a simple information that you might want to know before using the app: \n1. Each cloth must have atlast one tag, to make the tag, navigate to the tag page first.\n2. Cloth (or its combinations) can be grouped into outfit.",
                                                            size=24,
                                                            color=Themes.slate700,
                                                            weight=400,

                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.START,
                                                    spacing=10,
                                                ),
                                                padding = padding.only(bottom=20),
                                                height=400,
                                            ),
                                        ],
                                        expand=True,
                                        alignment=MainAxisAlignment.CENTER,
                                        spacing=10,
                                    ),
                                    expand=True,
                                    alignment=alignment.center,
                                    padding=padding.all(10),
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ),
                ],
                expand=True,
            )
        )

