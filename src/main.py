import flet as ft
from flet import Column, Row, Text, Icon, Container, Image, FilePicker
from components.normal_button import NormalButton
from components.nice_button import NiceButton
from components.navbar import Navbar
from theme.themes import Themes
from database.database import DB
from flet import Image
from components.styled_text import StyledText
from page.tag_page import TagPage
from components.styled_text import StyledText
from page.cloth_page import ClothPage
from page.outfit_page import OutfitPage
from components.image_picker import ImagePicker
from page.about_page import AboutPage


def main(page: ft.Page):
    DB.init()
    StyledText.init_font_family(page)

    page.padding = ft.margin.all(0)
    file_picker = ft.FilePicker(on_result=ImagePicker.on_file_selected)
    page.overlay.append(file_picker)

    icon_size = 18
    first_open_button = NormalButton("Outfit", ft.Icon(ft.icons.SPACE_DASHBOARD, "white", size=icon_size), text_overlay_color=Themes.slate950)
    page.add(Navbar(
        [
            first_open_button,
            NormalButton("Cloth", ft.Icon(ft.icons.CHECKROOM, "white", size=icon_size), text_overlay_color=Themes.slate950),
            NormalButton("Tags", ft.Icon(ft.icons.LOCAL_OFFER, "white", size=icon_size), text_overlay_color=Themes.slate950),
            NormalButton("About", ft.Icon(ft.icons.INFO, "white", size=icon_size), text_overlay_color=Themes.slate950),
        ], [
            OutfitPage(),
            ClothPage(file_picker),
            TagPage(),
            AboutPage(),
        ],
        sidebar_content=Column(
            controls=[
                Container(height=10),
                Row(
                    controls=[
                        Icon(ft.icons.BENTO, "white", size=38),
                        StyledText("Le Mari.", weight=800, size=40, color=Themes.slate50),
                    ]
                ),
                Container(height=10),
            ]
        ),
        sidebar_width=200
    ))

    first_open_button.set_disabled(True)


ft.app(target=main, assets_dir="assets")
