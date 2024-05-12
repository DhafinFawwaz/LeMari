import flet as ft
from flet import Column, Row, Text, Icon, Container, Image, FilePicker
from components.normal_button import NormalButton
from components.nice_button import NiceButton
from components.navbar import Navbar
from theme.themes import Themes
from database.database import DB
from flet import Image
from components.styled_text import StyledText 

def main(page: ft.Page):
    DB.init()
    StyledText.init_font_family(page)

    page.padding = ft.margin.all(0)
    page.add(Navbar(
            [
                NormalButton("Outfit", ft.Icon(ft.icons.SPACE_DASHBOARD, "white"), text_overlay_color=Themes.slate950),
                NormalButton("Cloth", ft.Icon(ft.icons.CHECKROOM, "white"), text_overlay_color=Themes.slate950),
                NormalButton("Tags", ft.Icon(ft.icons.LOCAL_OFFER, "white"), text_overlay_color=Themes.slate950),
                NormalButton("About", ft.Icon(ft.icons.INFO, "white"), text_overlay_color=Themes.slate950),
            ], [
                StyledText("Outfit"),
                StyledText("Cloth"),
                StyledText("Tag"),
                StyledText("About"),
            ],
            sidebar_content= Column(
                controls=[
                    Container(height=10),
                    Row(
                        controls=[
                            Icon(ft.icons.BENTO, "white", size=38),
                            StyledText("Le Mari.", weight=800, size= 40, color=Themes.slate50),
                        ]
                    ),
                    Container(height=10),
                ]
            ),
            sidebar_width=200
        )
    )

ft.app(target=main, assets_dir="assets")