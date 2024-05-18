from flet import Container, Image, ImageFit, Animation, AnimationCurve, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, ClipBehavior, CrossAxisAlignment, ScrollMode, StackFit, SearchBar, CircleBorder, Stack, border, Border, BorderSide, colors
from flet_core import RoundedRectangleBorder, BorderSide, TextStyle, ListTile, Text, ListView
from components.small_button import SmallButton
from components.styled_text import StyledText
from components.styled_search_bar import StyledSearchBar
from theme.themes import Themes
from typing import Optional, List, Callable
from flet_core.form_field_control import FormFieldControl, InputBorder
from flet_core.control_event import ControlEvent
from components.tag_picker import TagPicker
from database.tag import Tag
from database.cloth import Cloth
from database.outfit import Outfit


class CustomCheckBox(Container):
    def __init__(
        self,
        value: bool = False,
        top: int = 10,
        right: int = 10,
        border_width: float = 1,
        border_color: str = Themes.slate900,
        fill_color: str = Themes.slate100,
        check_color: str = Themes.green500,
    ):
        self.border_width = border_width
        self.border_color = border_color
        self.fill_color = fill_color
        self.check_color = check_color
        self.value = value
        super().__init__(
            width=16,
            height=16,
            border=None if value else border.all(
                width=border_width, color=border_color),
            bgcolor=check_color if value else fill_color,
            top=top,
            right=right,
            content=Icon(name=icons.CHECK, color="#ffffff",
                         size=12) if value else None,
            border_radius=3
        )

    def toggle(self):
        self.value = not self.value
        self.border = None if self.value else border.all(
            width=self.border_width, color=self.border_color)
        self.bgcolor = self.check_color if self.value else self.fill_color
        self.content = Icon(name=icons.CHECK, color="#ffffff",
                            size=12) if self.value else None
        self.update()


class ClothButton(Container):
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
        selected: bool = False,
        invoke_func=None
    ):
        self.invoke_func = invoke_func
        self.selected = selected
        self.check_box = CustomCheckBox(selected)
        super().__init__(
            bgcolor=bgcolor,
            margin=padding.all(0),
            padding=padding.all(0),
            content=Stack(
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Image(cloth.get_image_path(
                                ), fit=ImageFit.COVER, width=width, height=image_height),
                            ),
                            Container(
                                padding=padding.only(
                                    content_padding, 0, content_padding, content_padding),
                                content=Column(
                                    spacing=5,
                                    controls=[
                                        Container(
                                            content=StyledText(
                                                cloth.name, weight=800, size=18),
                                        ),
                                        Row(
                                            controls=[
                                                SmallButton(tag.name,
                                                            text_padding=padding.symmetric(
                                                                2, 6),
                                                            corner_radius=Themes.roundedmd,
                                                            text_weight=700,
                                                            text_size=11,
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
                    self.check_box
                ],
            ),
            border_radius=corner_radius,
            border=border.all(2, Themes.green500) if selected else border.all(2, colors.TRANSPARENT),
            on_click=self.toggle_button,
            on_hover=self.on_card_hover,
            animate_scale=Animation(
                duration=150,
                curve=AnimationCurve.EASE_OUT_BACK,
            ),
            width=width,
            on_tap_down=self.on_card_tap,
        )

    def on_card_hover(self, e):
        if (e.data == "true"):
            self.scale = 1.1
        else:
            self.scale = 1
        self.update()

    def on_card_tap(self, e):
        self.scale = 1.1
        self.update()

    def toggle_button(self, e):
        # update checkbox
        self.check_box.toggle()
        # update GUI
        self.selected = not self.selected
        if (self.selected):
            self.border = border.all(2, Themes.green500)
        else:
            self.border = border.all(2, colors.TRANSPARENT)
        self.update()
        # invoke function
        if self.invoke_func != None:
            self.invoke_func(e)


class ClothPicker(Container):
    def get_selected_cloths(self):
        return self.selected_cloth_list

    def set_chosen_cloth(self, cloth_list: List[Cloth]):
        self.selected_cloth_list.clear()
        for cloth in cloth_list:
            self.selected_cloth_list.append(cloth)

    def toggle_cloth(self, cloth: Cloth):
        # check if cloth already exist in selected cloth list
        idx: int = -1

        for i in range(len(self.selected_cloth_list)):
            if (self.selected_cloth_list[i].id == cloth.id):
                idx = i
                break

        if (idx == -1):
            self.selected_cloth_list.append(cloth)
        else:
            # remove from selected cloth list
            self.selected_cloth_list.pop(idx)

    def update_cloth_card_list(self):
        self.cloth_list = Cloth.find_all_by_search_and_tags("", self.search_bar_tag_picker.choosen_tags)
        self.cloth_card_list = []

        for cloth in self.cloth_list:
            # search for cloth in selected cloth list
            found: bool = False
            for selected_cloth in self.selected_cloth_list:
                if selected_cloth.id == cloth.id:
                    found = True
                    break
            if found:
                self.cloth_card_list.append(ClothButton(
                    cloth=cloth, selected=True, invoke_func=lambda e, cloth=cloth: self.toggle_cloth(cloth)))
            else:
                self.cloth_card_list.append(ClothButton(
                    cloth=cloth, selected=False, invoke_func=lambda e, cloth=cloth: self.toggle_cloth(cloth)))
        self.cloth_list_row.controls = self.cloth_card_list
        self.cloth_list_row.update()

    def update(self):
        self.update_cloth_card_list()
        super().update()

    def __init__(self, initial_cloth_list: List[Cloth] = []):
        self.selected_cloth_list: List[Cloth] = initial_cloth_list
        self.cloth_list = Cloth.get_all()
        self.cloth_card_list = []
        for cloth in self.cloth_list:
            # search for cloth in selected cloth list
            found: bool = False
            for selected_cloth in self.selected_cloth_list:
                if selected_cloth.id == cloth.id:
                    found = True
                    break
            if found:
                self.cloth_card_list.append(ClothButton(
                    cloth=cloth, selected=True, invoke_func=lambda e, cloth=cloth: self.toggle_cloth(cloth)))
            else:
                self.cloth_card_list.append(ClothButton(
                    cloth=cloth, selected=False, invoke_func=lambda e, cloth=cloth: self.toggle_cloth(cloth)))
        self.search_bar_tag_picker = TagPicker(on_change=lambda e: self.update_cloth_card_list())
        self.cloth_list_row = Row(
            controls=self.cloth_card_list,
            spacing=10,
            run_spacing=10,
            wrap=True
        )
        super().__init__(
            content=Column(
                controls=[
                    self.search_bar_tag_picker,
                    self.cloth_list_row
                ],
            ),
        )
