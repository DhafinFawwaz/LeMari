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
        )
        super().__init__(
            [self.background],
            tight=True
        )


class TagPage(Stack):
    def changehandler(self, e):
        print(f"hasil perubahan {e}")
        self.pills.controls.clear()
        if len(e) == 0:
            for tags in self.tags_data:
                self.pills.controls.append(PillTag(tags, on_click=lambda e, tag=tags: self.show_edit_dialog(e, tag)))
        else:
            for tags in self.tags_data:
                if e in tags.name:
                    self.pills.controls.append(
                        PillTag(tags, on_click=lambda e, tag=tags: self.show_edit_dialog(e, tag)))
        self.update()

    def input_change_handler(self, e):
        print(f"hasil perubahan {e}")
        self.string_tag = e

    def input_submit_handler(self, e):
        if (self.string_tag is not None) and (len(self.string_tag) > 0) and not (
                self.string_tag.strip() in self.tags_data):
            print(e)
            new_tag = Tag(self.string_tag.strip())
            new_tag.save()
            self.pills.controls.clear()
            self.pills.controls = [
                PillTag(tag, on_click=lambda e, tag=tag: self.show_edit_dialog(e, tag)) for tag in
                Tag.get_all()]
            self.update()
            self.main_dialog.close()
        elif self.string_tag is None or len(self.string_tag) == 0:
            self.show_error_dialog("Input gabole kosong yak 😎")
        elif self.string_tag.strip() in self.tags_data:
            self.show_error_dialog(f"{e} sudah ada")
        else:
            self.show_error_dialog("error mas")

    def show_add_dialog(self, e):
        self.main_dialog.show(
            title="Add Tag",
            content=Column(
                controls=[
                    StyledTextField(
                        placeholder="Insert new tag name",
                        on_change=self.input_change_handler,
                    )
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

    def show_error_dialog(self, message):
        print(f"Show Error: {message}")
        self.error_dialog.show(title="ERROR", content=StyledText(str(message), 16))

    def edit_handler(self, tag: Tag, new_name):
        print(f"Editing {tag.name} to {new_name}")
        tag.update(new_name)
        self.pills.controls.clear()
        self.pills.controls = [
            PillTag(tagz, on_click=lambda e: self.show_edit_dialog(e, tagz)) for tagz in
            Tag.get_all()]
        self.update()
        self.main_dialog.close()

    def delete_handler(self, tag: Tag):
        print(f"Deleting {tag}")
        tag.delete()
        self.pills.controls.clear()
        self.pills.controls = [
            PillTag(tagz, on_click=lambda e: self.show_edit_dialog(e, tagz)) for tagz in
            Tag.get_all()]
        self.update()
        self.main_dialog.close()

    def on_change_edit(self, e, current_change):
        self.current_change = e

    def show_edit_dialog(self, e, tag: Tag):
        self.main_dialog.show(
            title="Edit Tag",
            content=Column(
                controls=[
                    StyledTextField(
                        placeholder=tag.name,
                        on_change=lambda e: self.on_change_edit(e, self.current_change),
                    )
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

    def __init__(self):
        self.current_change = None
        self.string_tag = None
        self.main_dialog = Dialog(height=220, width=500)
        self.error_dialog = ErrorDialog()
        self.tags_data: List[Tag] = Tag.get_all()
        # self.tags_data: List[Tag] = [Tag("Birthday"), Tag("Activity"), Tag("Casual"), Tag("Formal"), Tag("Party")]
        # self.tes_tag = PillTag(Tag(name="tes"))
        self.pills = Row(
            controls=[PillTag(tag, on_click=lambda e, tag=tag: self.show_edit_dialog(e, tag)) for tag in
                      self.tags_data],
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
                    right=30,
                    bottom=20,
                    # width=200
                ),
                self.main_dialog,
                self.error_dialog
            ],
            expand=True
        )
