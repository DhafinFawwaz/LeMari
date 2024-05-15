from flet import TextField, TextStyle, padding, Icon, icons, Container, Stack, Row, colors, margin, Offset, Border, BorderSide, Text
from theme.themes import Themes

class StyledTextField(Container):

    def on_text_focus(self, e):
        self.border.top.color = Themes.indigo600
        self.border.left.color = Themes.indigo600
        self.border.right.color = Themes.indigo600
        self.border.bottom.color = Themes.indigo600
        self.update()
    def on_text_blur(self, e):
        self.border.top.color = colors.TRANSPARENT
        self.border.left.color = colors.TRANSPARENT
        self.border.right.color = colors.TRANSPARENT
        self.border.bottom.color = colors.TRANSPARENT
        self.update()

    def on_text_change(self, e):
        if len(e.data) != 0:
            self.placeholder_text.value = ""
        else:
            self.placeholder_text.value = self.placeholder
        self.placeholder_text.update()
        self.value = e.data
        if self.on_change:
            self.on_change(e.data)

    def __init__(
        self,
        width=None,
        height=50,
        text_size=14,
        prefix_icon: Icon = None,
        placeholder: str= "Search",
        focused_border_width=2,
        on_change=None,
    ):
        self.focused_border_width = focused_border_width
        self.on_change = on_change
        self.value = ""
        self.placeholder = placeholder
        self.placeholder_text = Text(
            size=text_size,
            style=TextStyle(font_family="Outfit-SemiBold"),
            color=Themes.slate400,
            expand=True,
            value=placeholder
        )

        self.stack_controls = [
            Container(
                content=prefix_icon,
                left=20,
                top=15
            ),

            Container(
                content=self.placeholder_text,
                top=12,
                left=57,
            ),

            Container(
                content=TextField(
                    text_size=text_size,
                    cursor_color=Themes.slate950,
                    bgcolor=colors.TRANSPARENT,
                    focused_bgcolor=colors.TRANSPARENT,
                    focused_color=Themes.slate950,
                    border_color=colors.TRANSPARENT,
                    focused_border_color=colors.TRANSPARENT,
                    height=height,
                    cursor_height=text_size+5,
                    text_style=TextStyle(font_family="Outfit-Bold"),
                    color=Themes.slate500,
                    selection_color=Themes.indigo600,
                    on_focus=self.on_text_focus,
                    on_blur=self.on_text_blur,
                    expand=True,
                    on_change=self.on_text_change,
                ),
                top=-4,
                left=45,
            ),
            

        ]
        if prefix_icon is None:
            self.stack_controls.pop(0)
            self.stack_controls[0].top = 13
            self.stack_controls[0].left = 18
            self.stack_controls[1].top = -3
            self.stack_controls[1].left = 6

        super().__init__(
            bgcolor=Themes.slate50,
            height=height,
            border_radius=Themes.roundedlg,
            content=Stack(
                controls=self.stack_controls
            ),
            border = Border(
                top=BorderSide   (width=self.focused_border_width, color=colors.TRANSPARENT),
                left=BorderSide  (width=self.focused_border_width, color=colors.TRANSPARENT),
                right=BorderSide (width=self.focused_border_width, color=colors.TRANSPARENT),
                bottom=BorderSide(width=self.focused_border_width, color=colors.TRANSPARENT),
            ),
        ),
        
