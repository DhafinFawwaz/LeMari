import flet as ft
from flet import Container, Row, Column, Icon, Stack
from components.styled_text import StyledText
from theme.themes import Themes
from components.dialog import Dialog
from components.error_dialog import ErrorDialog
from components.styled_text_field import StyledTextField
from components.nice_button import NiceButton
from components.styled_search_bar import StyledSearchBar
from database.tag import Tag
from typing import List
from sqlite3 import IntegrityError


class PillTag(Row):
    def __init__(self, tag: Tag = Tag("Title"), on_click=None):
        self.background = NiceButton(
            text=tag.name,
            on_click=on_click,
            bgcolor=Themes.slate950,
            overlay_scale=Themes.scalemd,
            tap_scale=Themes.scalesm,
            text_color=Themes.slate50,
            text_overlay_color=Themes.slate950,
            bg_overlay_color=Themes.slate200,
            content_padding=ft.padding.symmetric(7, 15),
        )
        super().__init__(
            [self.background],
            tight=True
        )


class TagPage(Stack):
    def changehandler(self, e):
        self.pills.controls.clear()
        if len(e) == 0:
            for tags in Tag.get_all():
                self.pills.controls.append(PillTag(tags, on_click=lambda e, tag=tags: self.show_edit_dialog(e, tag)))
        else:
            for tags in Tag.get_all():
                if e.lower() in tags.name.lower():
                    self.pills.controls.append(
                        PillTag(tags, on_click=lambda e, tag=tags: self.show_edit_dialog(e, tag)))
        self.update()

    def input_change_handler(self, e):
        self.string_tag = e

    def input_submit_handler(self, e):
        try:
            if self.string_tag is None or len(self.string_tag) == 0:
                raise Exception("Please fill the tag name")
            
            tag_name = self.string_tag.strip()
            tag_name_list = [tag.name for tag in Tag.get_all()]
            if tag_name in tag_name_list:
                raise Exception(f"Tag with name {tag_name} already exists")
            
            new_tag = Tag(tag_name)
            new_tag.save()
            self.pills.controls.clear()
            self.pills.controls = [
                PillTag(tag, on_click=lambda e, tag =tag: self.show_edit_dialog(e, tag)) for tag in
                Tag.get_all()]
            self.update()
            self.main_dialog.close()
            self.string_tag = ""
            
        except Exception as e:
            self.show_error_dialog(str(e))

    def show_add_dialog(self, e):
        text_field = StyledTextField(
                placeholder="Insert new tag name",
                on_change=self.input_change_handler,
                initial_value=self.string_tag
            )
        self.main_dialog.show(
            title="Add Tag",
            content=Column(
                controls=[
                    text_field
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bottom_controls=[
                NiceButton(
                    "Insert Tag",
                    Icon(
                        ft.icons.CREATE,
                        color=Themes.slate50,
                        size=15
                    ),
                    on_click=self.input_submit_handler,
                    bgcolor=Themes.green500,
                    bg_overlay_color=Themes.green600,
                    text_color=Themes.slate50
                ),
            ],
        )
        text_field.focus()

    def show_error_dialog(self, message):
        self.error_dialog.show(title="Oops!", content=StyledText(str(message), 16))

    def edit_handler(self, tag: Tag, new_name):
        try:
            if len(new_name.strip()) != 0:
                tag.update(new_name)
                self.pills.controls.clear()
                self.pills.controls = [
                    PillTag(tag, on_click=lambda e, tag=tag: self.show_edit_dialog(e, tag)) for tag in
                    Tag.get_all()]
                self.update()
                self.main_dialog.close()
                self.string_tag = ""
            else:
                self.show_error_dialog(f"Cannot set into an empty tag")
        except IntegrityError as e:
            self.show_error_dialog(f"Tag {new_name} already exists")
        except Exception as e:
            self.show_error_dialog(str(e))

    def delete_handler(self, tag: Tag):
        try:
            tag.delete()
            self.pills.controls.clear()
            self.pills.controls = [
                PillTag(tag, on_click=lambda e, tag=tag: self.show_edit_dialog(e, tag)) for tag in
                Tag.get_all()]
            self.update()
            self.main_dialog.close()
            self.string_tag = ""
        except IntegrityError as e:
            self.show_error_dialog(f"Tag {tag.name} is being used")
        except Exception as e:
            self.show_error_dialog(str(e))

    def on_change_edit(self, e):
        print(f"On change: {e}")
        self.current_change = e

    def show_edit_dialog(self, e, tag: Tag):
        text_field = StyledTextField(
            placeholder=tag.name,
            initial_value=tag.name,
            on_change=self.on_change_edit,
        )
        self.main_dialog.show(
            title=f"Edit {tag.name} Tag",
            content=Column(
                controls=[
                    text_field
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bottom_controls=[
                NiceButton(
                    "Delete Tag",
                    Icon(
                        ft.icons.DELETE,
                        color=Themes.slate50,
                        size=15
                    ),
                    on_click=lambda e: self.delete_handler(tag),
                    bgcolor=Themes.rose500,
                    bg_overlay_color=Themes.rose600,
                    text_color=Themes.slate50
                ),
                NiceButton(
                    "Edit Tag",
                    Icon(
                        ft.icons.CREATE,
                        color=Themes.slate50,
                        size=15
                    ),
                    on_click=lambda e: self.edit_handler(tag, self.current_change),
                    bgcolor=Themes.green500,
                    bg_overlay_color=Themes.green600,
                    text_color=Themes.slate50
                )
            ],
        )
        text_field.focus()

    def __init__(self):
        self.current_change = None
        self.string_tag = None
        self.main_dialog = Dialog(height=220, width=500)
        self.error_dialog = ErrorDialog()
        self.pills = Row(
            controls=[PillTag(tag, on_click=lambda e, tag=tag: self.show_edit_dialog(e, tag)) for tag in
                      Tag.get_all()],
            wrap=True,
            auto_scroll=True,
            tight=True
        )
        self.dialog = Dialog()
        self.warning = Container(
            content=StyledText("Error!"),
            padding=5,
            bgcolor=ft.colors.RED_200,
            visible=False
        )

        super().__init__(
            controls=[
                Container(
                    content=Column(
                        controls=[StyledSearchBar(on_change=self.changehandler), self.pills],
                        auto_scroll=True,
                    ),
                    padding=ft.padding.all(15)
                ),
                Container(
                    content=NiceButton(
                        "Add Tag",
                        Icon(
                            ft.icons.ADD,
                            Themes.slate50,
                            size=21
                        ),
                        on_click=self.show_add_dialog,
                        bgcolor=Themes.rose600,
                        bg_overlay_color=Themes.rose500,
                        text_color=Themes.slate50
                    ),
                    right=0, bottom=0,
                    margin=ft.margin.all(15),
                ),
                self.main_dialog,
                self.error_dialog
            ],
            expand=True
        )
