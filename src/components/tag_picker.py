from flet import Container, Stack, Icon, icons, alignment, margin, padding, Column, ResponsiveRow, GridView, Row, TextField, ClipBehavior, CrossAxisAlignment, ScrollMode, StackFit, SearchBar, CircleBorder
from flet_core import RoundedRectangleBorder, BorderSide, TextStyle, ListTile, Text, ListView
from components.small_button import SmallButton
from components.styled_text import StyledText
from components.styled_search_bar import StyledSearchBar
from theme.themes import Themes
from typing import Optional, List, Callable
from database.tag import Tag
from flet_core.form_field_control import FormFieldControl, InputBorder
from flet_core.control_event import ControlEvent
from database.tag import Tag
import time

class TagButton(Container):

    def __init__(
        self,
        text: Optional[str] = "Tag",
        # icon: Optional[Icon] = Icon(icons.LOCAL_OFFER, size=12, color=Themes.slate50),
        icon: Optional[Icon] = None,
        on_click=None,
        on_hover=None,
        bgcolor: Optional[str] = Themes.slate900,
        bg_overlay_color: Optional[str] = Themes.slate200,
        text_color: Optional[str] = Themes.slate50,
        text_overlay_color: Optional[str] = Themes.slate950,
        text_weight: int = 800,
        text_size: int = 12,
        corner_radius: int = Themes.roundedmd,
        disabled_bgcolor: Optional[str] = Themes.indigo600,
        text_padding = padding.symmetric(3, 7),
        width=None,
        icon_bg_color=Themes.slate800,
    ):
        self.text_content = StyledText(text, color=text_color, weight=text_weight, size=text_size)
        self.icon_content = icon
        if icon: 
            self.icon_container = Container(
                content=self.icon_content,
                bgcolor=icon_bg_color,
                border_radius=corner_radius,
                padding=padding.all(2)
            )
        super().__init__(
            bgcolor=bgcolor,
            content=Row(
                spacing=4,
                controls=[
                    self.icon_container,
                    self.text_content,
                ], expand=False,
                tight=True
            ) if icon else self.text_content
            ,
            padding=text_padding,
            on_click=on_click,
            on_hover=self.on_button_hover,
            border_radius=corner_radius,
            width=width,
            expand=False
        )
        self.on_hover_from_outside = on_hover
        self.disabled_bgcolor = disabled_bgcolor
        self.default_bgcolor = bgcolor
        self.bg_overlay_color = bg_overlay_color
        self.text_overlay_color = text_overlay_color
        self.text_color = text_color
        self.icon_bg_color = icon_bg_color

    def on_button_hover(self, e):
        if e.data == "true":
            self.text_content.color = self.text_overlay_color
            self.bgcolor = self.bg_overlay_color
            if self.icon_content: 
                self.icon_content.color = self.text_overlay_color
                self.icon_container.bgcolor = self.bg_overlay_color
        else:
            self.text_content.color = self.text_color
            self.bgcolor = self.default_bgcolor
            if self.icon_content: 
                self.icon_content.color = self.text_color
                self.icon_container.bgcolor = self.icon_bg_color
            
        if self.on_hover_from_outside: self.on_hover_from_outside(e)
        self.update()
        self.style_disabled = False

    def set_disabled(self, is_disabled: bool):
        self.style_disabled = is_disabled
        # self.disabled = is_disabled
        if self.style_disabled:
            self.bgcolor = self.disabled_bgcolor
            self.text_content.color = self.text_color
            if(self.icon_content): self.icon_content.color = self.text_color
        else:
            self.bgcolor = self.default_bgcolor
            self.text_content.color = self.text_color
            if(self.icon_content): self.icon_content.color = self.text_color
        self.update()


class TagPicker(Row):

    def get_choosen_tags(self):
        return self.choosen_tags
    
    def add_choosen_tag(self, tag: Tag):
        # check if tag already exist
        for t in self.choosen_tags:
            if t.id == tag.id:
                return
            
        self.choosen_tags.append(tag)
        self.flex_box.insert(-2, TagButton(tag.name, Icon(icons.CLOSE, size=12, color=Themes.slate50), on_click=lambda e, tag=tag: self.on_remove_tag(tag)))
        self.search_text = ""
        self.floating_search_bar.close_view(self.search_text)
        self.floating_search_bar.update()
        self.update_floating_search_bar()

    def on_choose_tag(self, tag: Tag):
        # check if tag already exist
        for t in self.choosen_tags:
            if t.id == tag.id:
                return

        self.choosen_tags.append(tag)
        self.flex_box.insert(-2, TagButton(tag.name, Icon(icons.CLOSE, size=12, color=Themes.slate50), on_click=lambda e, tag=tag: self.on_remove_tag(tag)))
        self.search_text = ""
        self.floating_search_bar.close_view(self.search_text)
        self.floating_search_bar.update()
        self.update_floating_search_bar()

        time.sleep(0.01) # have to do this to make the floating search move to the right
        self.floating_search_bar.open_view()

    def set_choosen_tags(self, tag_list: List[Tag]):
        self.choosen_tags.clear()
        for tag in tag_list:
            self.choosen_tags.append(tag)
            self.flex_box.insert(-2, TagButton(tag.name, Icon(icons.CLOSE, size=12, color=Themes.slate50), on_click=lambda e, tag=tag: self.on_remove_tag(tag)))
        self.search_text = ""

    def on_remove_tag(self, tag: Tag):
        poped_idx = -1
        for i in range(len(self.choosen_tags)):
            if self.choosen_tags[i].id == tag.id:
                self.choosen_tags.pop(i)
                poped_idx = i
                break                
        self.flex_box.pop(poped_idx)
        self.update_floating_search_bar()
    
    def open_floating_search_bar(self, e):
        fsb = self.floating_search_bar
        fsb.visible = True
        self.update_floating_search_bar()
        fsb.open_view()

    # return list of tags that are not in choosen_tags and match the search_text
    def get_all_tags_filtered(self):
        tag_list = Tag.get_all()
        for t in self.choosen_tags:
            for i in range(len(tag_list)):
                if tag_list[i].id == t.id:
                    tag_list.pop(i)
                    break
        if self.search_text == None or self.search_text == "": return tag_list

        filtered_tag_list = []
        for t in tag_list:
            if self.search_text.lower() in t.name.lower():
                filtered_tag_list.append(t)
        return filtered_tag_list

    def update_floating_search_bar(self):
        tag_list = self.get_all_tags_filtered()

        self.floating_search_bar_controls.clear()
        for i in range(len(tag_list)):
            self.floating_search_bar_controls.append(
                Container(
                    content=TagButton(tag_list[i].name, on_click=lambda e, i=i: self.on_choose_tag(tag_list[i]), width=self.search_content_width, text_size=14, text_padding=padding.symmetric(10, 20), bgcolor=Themes.slate800),
                    padding=padding.symmetric(5, 10)
                )
            )
        self.suggestion_view.update()
        # self.floating_search_bar.update()
        self.update()
        if self.on_change:
            self.on_change(self.choosen_tags)
    
    def on_search_changed(self, e: ControlEvent):
        self.search_text: str = e.data
        self.update_floating_search_bar()

    def __init__(
        self,
        on_change: Callable[[Tag], None]=None,
        ):
        self.on_change = on_change

        # the following have absolute positioning, so the values here are set fixed
        self.search_text = ""
        floating_search_bar_width = 160
        floating_search_bar_height = 200
        right_padding = 40
        self.search_content_width = floating_search_bar_width - right_padding # handle scrollbar
        self.unchoosen_tags_comp = [
            TagButton("Blue",  width=self.search_content_width), 
            TagButton("Green", width=self.search_content_width), 
            TagButton("Black", width=self.search_content_width),
            TagButton("Black", width=self.search_content_width),
            TagButton("Black", width=self.search_content_width),
            TagButton("Black", width=self.search_content_width),
            TagButton("Blue",  width=self.search_content_width),
            TagButton("Red",   width=self.search_content_width),
        ]


        self.floating_search_bar_controls = []
        self.suggestion_view = ListView(
            controls=self.floating_search_bar_controls,
        )
        self.floating_search_bar = SearchBar(
            width=floating_search_bar_width,
            height=0,
            on_change=self.on_search_changed,
            view_shape=RoundedRectangleBorder(radius=Themes.roundedmd),
            view_header_text_style=TextStyle(font_family="Outfit-SemiBold"),
            view_hint_text_style=TextStyle(font_family="Outfit-SemiBold"),
            view_surface_tint_color=Themes.slate950,
            bar_overlay_color=Themes.slate950,
            controls=[self.suggestion_view],
            view_bgcolor=Themes.slate900,
        )

        # self.floating_search_bar = Container(
        #     border_radius=Themes.roundedxl,
        #     width=floating_search_bar_width,
        #     height=floating_search_bar_height,
        #     bgcolor=Themes.slate950,
        #     padding=padding.all(10),
        #     # left=0,
        #     # top=0,
        #     content=Column(
        #         width=floating_search_bar_width,
        #         height=floating_search_bar_height,
        #         controls=[
        #             StyledSearchBar(
        #                 width=search_content_width
        #             ),
        #             Column(
        #                 controls=self.unchoosen_tags_comp
        #             )
        #         ],
        #         scroll=ScrollMode.ADAPTIVE,
        # )
        # )

        self.flex_box = [
            TagButton(text="Tag", icon=Icon(icons.ADD, size=12, color=Themes.slate50), icon_bg_color=Themes.green400, on_click=self.open_floating_search_bar, bgcolor=Themes.green500, bg_overlay_color=Themes.slate50),
            self.floating_search_bar
        ]

        self.choosen_tags: List[Tag] = []
        self.choosen_tags_row = Row(
            vertical_alignment=CrossAxisAlignment.START,
            controls=self.flex_box,
            spacing=10,
            wrap=True,
            run_spacing=10
        )

        
        super().__init__(
            controls=[
                self.choosen_tags_row, 
            ],
            wrap=True,
            spacing=3,
            run_spacing=3

        )