from flet import Container, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, InputBorder, MainAxisAlignment, CrossAxisAlignment, ScrollMode, FilePicker, Switch
from components.nice_button import NiceButton
from components.dialog import Dialog
from components.styled_text import StyledText
from components.clothcard import ClothCard
from database.cloth import Cloth
from database.outfit import Outfit
from database.tag import Tag
from theme.themes import Themes
from components.styled_search_bar import StyledSearchBar
from components.tag_picker import TagPicker
from components.error_dialog import ErrorDialog
from components.styled_text_field import StyledTextField
from components.tag_picker import TagPicker
from components.small_button import SmallButton
from components.image_picker import ImagePicker
from components.outfitcard import OutfitCard
from components.cloth_picker import ClothPicker
from typing import List


class OutfitPage(Container):
    def on_add_outfit(self, e):
        try:
            new_outfit = Outfit(self.outfit_name_field.value, self.cloth_picker.get_selected_cloths())
            new_outfit.save()
            self.main_dialog.close()
            self.update()
        except Exception as e:
            self.main_dialog.close()
            print(str(e))
            pass

    def show_insert_dialog(self, e):
        self.outfit_name_field = StyledTextField("Outfit Name", placeholder="Enter Outfit Name")
        self.cloth_picker = ClothPicker()
        self.main_dialog.show("Insert Outfit",
            Column(
                spacing=5,
                controls=[
                    StyledText("Outfit Name", 13),
                    self.outfit_name_field,
                    Container(height=7),
                    self.cloth_picker
                ],
                expand=True
            ),
            [
                NiceButton("Insert Outfit", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_add_outfit, bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ]
        )

    def update_outfit_card_list(self):
        self.outfit_list = Outfit.get_all_outfit()
        self.outfit_card_list = [
            OutfitCard(
                outfit=outfit,
                on_click=None,
            ) for outfit in self.outfit_list
        ]

        self.outfit_list_row.controls = self.outfit_card_list
        self.outfit_list_row.update()
    
    def update(self):
        self.update_outfit_card_list()
        super().update()

    def __init__(self):
        self.outfit_list = Outfit.get_all_outfit()
        self.outfit_card_list = [
            OutfitCard(
                outfit=outfit,
                on_click=None,
            ) for outfit in self.outfit_list
        ]
        self.outfit_name_field = StyledTextField("Outfit Name", placeholder="Enter Outfit Name")
        self.outfit_list_row = Row(
            vertical_alignment=CrossAxisAlignment.START,
            controls=self.outfit_card_list,
            wrap=True
        )

        self.main_dialog = Dialog(title="Insert Outfit",
            bottom_controls=[
                NiceButton("Insert Outfit", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=None, bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ],
            margin=margin.symmetric(60, 170),                        
        )

        self.cloth_picker = ClothPicker()

        super().__init__(
            margin=margin.all(0),
            padding=padding.all(0),
            expand=True,

            content=Stack(
                controls=[
                    Container(
                        padding=padding.all(15),
                        content=Column(
                            scroll=ScrollMode.ADAPTIVE,
                            controls=[
                                StyledSearchBar(),
                                self.outfit_list_row,
                            ]
                        )
                    ),
                    Container(
                        content=NiceButton("Add Outfit", Icon(icons.ADD, Themes.slate50, size=21), on_click=self.show_insert_dialog, bgcolor=Themes.rose600, bg_overlay_color=Themes.rose500, text_color=Themes.slate50),
                        right=0, bottom=0,
                        margin=margin.all(15),
                    ),    
                    self.main_dialog                
                ],
                expand=True
            )
        )
