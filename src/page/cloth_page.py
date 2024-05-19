from flet import Container, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, InputBorder, MainAxisAlignment, CrossAxisAlignment, ScrollMode, FilePicker, Switch
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
from components.image_picker import ImagePicker
import time
import os

class ClothPage(Container):
    # Insert cloth in database
    def on_add_cloth(self, e):
        try:
            # If user didn't select any image, raise an exception
            if (self.image_picker.choosen_image == None):
                raise Exception("No image selected", "Please select an image.")

            # If somehow the selected image is a directory, raise an exception
            if (os.path.isdir(self.image_picker.choosen_image.path)):
                raise Exception("A directory?", "The selected image is a directory, please select a file.")
            
            # If somehow the selected image extension is not jpg, jpeg, or png, raise an exception
            if (not self.image_picker.choosen_image.name.lower().endswith(('.jpg', '.jpeg', '.png'))):
                raise Exception("Invalid format", "The selected image must be a jpg, jpeg, or png file.")
            
            # OK image's fine, but how about the name?
            if (self.cloth_name_field.value == ""):
                raise Exception("Insert name", "Please enter the cloth name.")
            
            # If no tag has been selected, raise an exception
            if (len(self.tag_picker.choosen_tags) == 0):
                raise Exception("No tag selected", "Please select at least one tag.")
            
            # OK, image's fine, let's continue
            new_cloth = Cloth(self.cloth_name_field.value, self.image_picker.choosen_image.name, self.tag_picker.choosen_tags)
            new_cloth.save()
            Cloth.save_image(self.image_picker.choosen_image)
            self.main_dialog.close()
            self.update()
        except Exception as e:
            self.error_dialog.show(e.args[0], StyledText(e.args[1], 16))
            print(str(e))

    # Edit cloth in database
    def on_edit_cloth(self, e):
        try:
            # If somehow the selected image is a directory, raise an exception
            if (os.path.isdir(self.image_picker.choosen_image.path)):
                raise Exception("A directory?", "The selected image is a directory, please select a file.")
            
            # If somehow the selected image extension is not jpg, jpeg, or png, raise an exception
            if (not self.image_picker.choosen_image.name.lower().endswith(('.jpg', '.jpeg', '.png'))):
                raise Exception("Invalid format", "The selected image must be a jpg, jpeg, or png file.")
            
            # If no tag has been selected, raise an exception
            if (len(self.tag_picker.choosen_tags) == 0):
                raise Exception("No tag selected", "Please select at least one tag.")
            
            

            # OK, image's fine, let's continue
            old_image_path = self.current_cloth.get_image_path()
            new_image_path = self.image_picker.choosen_image.path
            if old_image_path != new_image_path:
                Cloth.delete_image_by_name(self.current_cloth.image_name)
            self.current_cloth.name = self.cloth_name_field.value
            self.current_cloth.image_name = self.image_picker.choosen_image.name
            self.current_cloth.tag_list = self.tag_picker.choosen_tags
            self.current_cloth.edit()
            if old_image_path != new_image_path:
                Cloth.save_image(self.image_picker.choosen_image)
            self.main_dialog.close()
            self.update()
        except Exception as e:
            self.error_dialog.show(e.args[0], StyledText(e.args[1], 16)) 
            print(str(e))
            
    # Delete cloth in database
    def on_delete_cloth(self, e):
        try:
            self.current_cloth.delete()
            self.update()
            self.main_dialog.close()
        except Exception as e:
            self.error_dialog.show("Error", StyledText(str(e), 16)) 
            print(str(e))



    # Show insert dialog pop up
    def show_insert_dialog(self, e):
        self.cloth_name_field = StyledTextField("Cloth Name", placeholder="Enter Cloth Name")
        self.tag_picker = TagPicker()
        self.image_picker = ImagePicker(file_picker=self.file_picker)

        self.main_dialog.show("Insert Cloth", 
            Column(
                spacing=5,
                controls=[
                    StyledText("Cloth Name", 13),
                    self.cloth_name_field,
                    Container(height=7),
                    self.tag_picker,
                    Container(height=7),
                    self.image_picker,
                ],
                expand=True
            ),

            [
                NiceButton("Insert Cloth", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_add_cloth, bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ]
        )

    # Show edit dialog pop up
    def show_edit_dialog(self, e, cloth: Cloth):
        self.current_cloth = cloth
        self.cloth_name_field = StyledTextField(placeholder=cloth.name)
        self.cloth_name_field.value = cloth.name
        self.tag_picker = TagPicker()
        self.tag_picker.set_choosen_tags(cloth.tag_list)
        self.image_picker = ImagePicker(file_picker=self.file_picker)
        self.image_picker.set_choosen_image(cloth.image_name, cloth.get_image_path())


        self.main_dialog.show("Edit Cloth", 
            Column(
                spacing=5,
                controls=[
                    StyledText("Cloth Name", 13),
                    self.cloth_name_field,
                    Container(height=7),
                    self.tag_picker,
                    Container(height=7),
                    self.image_picker,
                ],
                expand=True
            ),
            
            [
                NiceButton("Delete Cloth", Icon(icons.DELETE, color=Themes.slate50, size=15), on_click=self.on_delete_cloth, bgcolor=Themes.rose500, bg_overlay_color=Themes.rose600, text_color=Themes.slate50),
                NiceButton("Edit Cloth", Icon(icons.EDIT, color=Themes.slate50, size=15), on_click=lambda e: self.on_edit_cloth(self.current_cloth), bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ]
        )
        
        self.image_picker.update()

    # Update the card list GUI
    def update_cloth_card_list(self):
        self.cloth_list = Cloth.find_all_by_search_and_tags(self.current_search, self.search_bar_tag_picker.choosen_tags)

        self.cloth_card_list = [
            ClothCard(
                cloth=cloth,
                on_click=lambda e, cloth=cloth: self.show_edit_dialog(e, cloth),
                on_tag_clicked=lambda tag: self.search_bar_tag_picker.add_choosen_tag(tag)
            ) for cloth in self.cloth_list
        ]

        self.cloth_list_row.controls = self.cloth_card_list
        self.cloth_list_row.update()

    # Update the whole GUI
    def update(self):
        self.update_cloth_card_list()
        super().update()      

    # update the GUI when search bar is used
    def on_search(self, e):
        self.current_search = e
        self.update()   

    def __init__(self, file_picker: FilePicker):
        # Error dialog
        self.error_dialog = ErrorDialog(title="Error", content=StyledText("You made an error", 16))
        
        # Insert dialog
        self.main_dialog = Dialog(title="Insert Cloth",
            bottom_controls=[
                NiceButton("Insert Cloth", Icon(icons.CREATE, color=Themes.slate50, size=15), on_click=self.on_add_cloth, bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ],
            margin=margin.symmetric(60, 170),                        
        )

        # Edit dialog
        self.main_dialog = Dialog(title="Edit Cloth",
            bottom_controls=[
                NiceButton("Delete Cloth", Icon(icons.DELETE, color=Themes.slate50, size=15), on_click=self.on_delete_cloth, bgcolor=Themes.rose500, bg_overlay_color=Themes.rose600, text_color=Themes.slate50),
                NiceButton("Edit Cloth", Icon(icons.EDIT, color=Themes.slate50, size=15), on_click=lambda e: self.on_edit_cloth(self.current_cloth), bgcolor=Themes.green500, bg_overlay_color=Themes.green600, text_color=Themes.slate50),
            ],
            margin=margin.symmetric(60, 170),                        
        )
        
        self.search_bar_tag_picker = TagPicker(on_change=lambda e: self.update_cloth_card_list())
        self.file_picker = file_picker
        self.cloth_card_list = []
        self.current_search = ""
        self.current_cloth = None

        # form
        self.cloth_name_field = StyledTextField("Cloth Name", placeholder="Enter Cloth Name")
        self.tag_picker = TagPicker()
        self.image_picker = ImagePicker(file_picker=self.file_picker)
        self.cloth_list_row = Row(
            vertical_alignment=CrossAxisAlignment.START,
            controls=self.cloth_card_list,
            wrap=True,
        )

        super().__init__(
            margin=margin.all(0),
            padding=padding.all(0),
            expand=True,

            content = Stack(
                controls=[
                    # Actual content
                    Container(
                        padding=padding.all(15),
                        content=Column(
                            scroll=ScrollMode.ADAPTIVE,
                            controls=[
                                # search bar
                                StyledSearchBar(on_change=self.on_search),
                                self.search_bar_tag_picker,

                                # Cloth list
                                self.cloth_list_row
                            ]
                        )
                    ), 

                    # Button bottom right
                    Container(
                        content=NiceButton("Add Cloth", Icon(icons.ADD, Themes.slate50, size=21), on_click=self.show_insert_dialog, bgcolor=Themes.rose600, bg_overlay_color=Themes.rose500, text_color=Themes.slate50),
                        right=0, bottom=0,
                        margin=margin.all(15),
                    ),
            
                    self.main_dialog,

                    self.error_dialog,

                ],
                expand=True,
            )
        )

        


