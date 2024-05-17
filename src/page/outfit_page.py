from flet import Container, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, InputBorder, MainAxisAlignment, CrossAxisAlignment, ScrollMode, FilePicker, Switch, IconButton
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
            new_outfit = Outfit(self.outfit_name_field.value,
                                self.cloth_picker.get_selected_cloths())
            new_outfit.save()
            self.main_dialog.close()
            self.update_outfit_card_list()
        except Exception as e:
            self.main_dialog.close()
            print(str(e))

    def on_edit_outfit(self, e):
        try:
            self.current_outfit.name = self.outfit_name_field.value
            self.current_outfit.cloth_list = self.cloth_picker.get_selected_cloths()
            self.current_outfit.edit()
            self.detail_dialog.close()
            self.outfit_name_title.content = StyledText(self.outfit_name_field.value, size=20, weight=800)
            self.update_cloth_card_list()

        except Exception as e:
            self.detail_dialog.close()
            print(str(e))
            pass

    def on_delete_outfit(self, e):
        try:
            self.current_outfit.delete()
            self.detail_dialog.close()
            self.back(e)
        except Exception as e:
            # self.error_dialog.show("Error", StyledText(str(e), 16))
            self.detail_dialog.close()
            print(str(e))

    def show_edit_dialog(self, e):
        self.outfit_name_field = StyledTextField(
            "Outfit Name", placeholder=self.current_outfit.name)
        self.outfit_name_field.value = self.current_outfit.name
        self.cloth_picker = ClothPicker(self.current_outfit.cloth_list)
        self.detail_dialog.show("Edit Outfit",
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
                                    NiceButton("Confirm", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_edit_outfit,
                                               bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
                                ]
                                )

    def show_insert_dialog(self, e):
        self.outfit_name_field = StyledTextField(
            "Outfit Name", placeholder="Enter Outfit Name")
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
                                  NiceButton("Insert Outfit", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_add_outfit,
                                             bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
                              ]
                              )

    def back(self, e):
        self.content = self.main_page
        self.update()
        self.update_outfit_card_list()

    def show_detail_page(self, e, outfit: Outfit):
        self.current_outfit = outfit
        self.cloth_list = self.current_outfit.get_cloth_list()

        self.cloth_card_list = [
            ClothCard(
                cloth=cloth,
            ) for cloth in self.cloth_list
        ]

        self.outfit_name_title = Container(
            content=StyledText(value=outfit.name, size=20, weight=800))
        self.cloth_list_row.controls = self.cloth_card_list
        self.detail_outfit_page = Stack(
            controls=[
                Container(
                    padding=padding.all(15),
                    content=Column(
                        scroll=ScrollMode.ADAPTIVE,
                        controls=[
                            Row(controls=[
                                IconButton(icons.ARROW_BACK, icon_color=Themes.slate500,
                                           icon_size=20, tooltip="Back", on_click=self.back),
                                self.outfit_name_title
                            ]),
                            self.cloth_list_row
                        ]
                    )
                ),
                Container(
                    content=Row(
                        controls=[
                            NiceButton("Delete Outfit", Icon(icons.ADD, Themes.slate50, size=21), on_click=self.on_delete_outfit,
                                       bgcolor=Themes.rose600, bg_overlay_color=Themes.rose500, text_color=Themes.slate50),
                            NiceButton("Edit Outfit", Icon(icons.ADD, Themes.slate50, size=21), on_click=self.show_edit_dialog,
                                       bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50)
                        ]
                    ),
                    right=0, bottom=0,
                    margin=margin.all(15),
                ),
                self.detail_dialog
            ],
            expand=True
        )
        self.content = self.detail_outfit_page
        self.update()

    def update_cloth_card_list(self):
        self.cloth_list = self.current_outfit.get_cloth_list()

        self.cloth_card_list = [
            ClothCard(
                cloth=cloth,
            ) for cloth in self.cloth_list
        ]

        self.cloth_list_row.controls = self.cloth_card_list
        self.cloth_list_row.update()
        self.update()

    def update_outfit_card_list(self):
        self.outfit_list = Outfit.get_all_by_search(self.current_search)
        self.outfit_card_list = [
            OutfitCard(
                outfit=outfit,
                on_click=lambda e, outfit=outfit: self.show_detail_page(
                    e, outfit),
            ) for outfit in self.outfit_list
        ]
        self.outfit_list_row.controls = self.outfit_card_list
        self.outfit_list_row.update()
        self.update()

    def on_search(self, e):
        self.current_search = e
        self.update_outfit_card_list()

    def __init__(self):
        self.outfit_list = Outfit.get_all_outfit()
        self.outfit_card_list = [
            OutfitCard(
                outfit=outfit,
                on_click=lambda e, outfit=outfit: self.show_detail_page(
                    e, outfit),
            ) for outfit in self.outfit_list
        ]

        # insert form
        self.cloth_picker = ClothPicker()
        self.outfit_name_field = StyledTextField(
            "Outfit Name", placeholder="Enter Outfit Name")
        self.outfit_list_row = Row(
            vertical_alignment=CrossAxisAlignment.START,
            controls=self.outfit_card_list,
            wrap=True
        )
        self.main_dialog = Dialog(title="Insert Outfit",
                                  bottom_controls=[
                                      NiceButton("Insert Outfit", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_add_outfit,
                                                 bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
                                  ],
                                  margin=margin.symmetric(60, 170),
                                  )

        self.detail_dialog = Dialog(title="Edit Outfit",
                                    bottom_controls=[
                                        NiceButton("Insert Outfit", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_edit_outfit,
                                                   bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
                                    ],
                                    margin=margin.symmetric(60, 170),
                                    )

        self.current_search = ""
        self.current_outfit = None
        self.cloth_list = []
        self.cloth_card_list = []
        self.cloth_list_row = Row(
            vertical_alignment=CrossAxisAlignment.START,
            controls=self.cloth_card_list,
            wrap=True,
        )

        self.main_page = Stack(
            controls=[
                Container(
                    padding=padding.all(15),
                    content=Column(
                        scroll=ScrollMode.ADAPTIVE,
                        controls=[
                            StyledSearchBar(on_change=self.on_search),
                            self.outfit_list_row,
                        ]
                    )
                ),
                Container(
                    content=NiceButton("Add Outfit", Icon(icons.ADD, Themes.slate50, size=21), on_click=self.show_insert_dialog,
                                       bgcolor=Themes.rose600, bg_overlay_color=Themes.rose500, text_color=Themes.slate50),
                    right=0, bottom=0,
                    margin=margin.all(15),
                ),
                self.main_dialog
            ],
            expand=True
        )

        self.detail_outfit_page = None

        super().__init__(
            margin=margin.all(0),
            padding=padding.all(0),
            expand=True,

            content=self.main_page
        )
