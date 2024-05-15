from flet import Container, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, InputBorder, MainAxisAlignment, CrossAxisAlignment, ScrollMode, FilePicker, Image, ImageFit
from flet_core import FilePickerResultEvent
from flet_core.file_picker import FilePickerFile

from components.nice_button import NiceButton
from components.dialog import Dialog
from components.styled_text import StyledText
from components.clothcard import ClothCard
from database.cloth import Cloth
from database.tag import Tag
from theme.themes import Themes
from components.styled_search_bar import StyledSearchBar
from components.tag_picker import TagPicker
from components.error_dialog import ErrorDialog
from components.styled_text_field import StyledTextField
from components.tag_picker import TagPicker
from components.small_button import SmallButton
from database.database import DB

class ImagePicker(Container):
    ctx: "ImagePicker" = None

    def on_file_selected(e: FilePickerResultEvent):
        if(e.files is None or len(e.files) == 0): return
        ImagePicker.ctx.choosen_image = e.files[0]
        ImagePicker.ctx.content = ImagePicker.ctx.get_content()
        ImagePicker.ctx.update()

    def set_choosen_image(self, image_name: str, image_path: str):
        self.choosen_image = FilePickerFile(name=image_name, path=image_path, size=0)
        self.content = self.get_content()

    def open_image_picker(self, file_picker: FilePicker):
        ImagePicker.ctx = self
        file_picker.pick_files(
            dialog_title="Select an image",
            file_type="image",
            allowed_extensions=["png", "jpg", "jpeg", "webp"],
            allow_multiple=True
        )

    def on_image_hover(self, e):
        if(e.data == "true"):
            self.bgcolor = self.bg_overlay_color
            self.overlay.opacity = 0.4
        else:
            self.bgcolor = self.bg_default_color
            self.overlay.opacity = 0
        self.update()

    def get_content(self):
        if self.choosen_image:
            self.overlay.opacity = 0
            return Stack(
                controls=[
                    Row(
                        controls=[
                            Image(src=self.choosen_image.path, fit=ImageFit.CONTAIN)
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    self.overlay
                ],
                expand=True,
            )
        
        return Row(
            controls=[
                Column(
                    controls=[
                        Icon(icons.UPLOAD_FILE_ROUNDED, size=50, color=Themes.slate400),
                        StyledText("Click to insert image"),
                        StyledText("PNG or JPG"),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            ],
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
    

    def __init__(
        self,
        file_picker: FilePicker,
        width=None,
        height=None,
        bgcolor=Themes.slate100,
        bg_overlay_color=Themes.slate300,
    ):
        self.choosen_image: FilePickerFile = None
        self.bg_default_color = bgcolor
        self.bg_overlay_color = bg_overlay_color
        self.overlay = Container(
            bgcolor=Themes.slate950,
            expand=True,
            opacity=0.4,
            content=Row(
                controls=[
                    Column(
                        controls=[
                            Icon(icons.UPLOAD_FILE_ROUNDED, size=50, color=Themes.slate400),
                            StyledText("Click to insert image", color=Themes.slate50),
                            StyledText("PNG or JPG", color=Themes.slate50),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
            )
        )
        super().__init__(
            bgcolor=self.bg_default_color,
            on_click=lambda e: self.open_image_picker(file_picker),
            border_radius=Themes.roundedlg,
            content=self.get_content(),
            on_hover=self.on_image_hover,
            expand=True,
        )
        