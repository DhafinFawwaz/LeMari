from flet import TextField, TextStyle, padding, Icon, icons
from theme.themes import Themes
from components.styled_text_field import StyledTextField

class StyledSearchBar(StyledTextField):
    def __init__(
        self,   
        width=None,
        height=50,
        text_size=16,
        on_change=None
    ):
        super().__init__(
            width,
            height,
            text_size,
            prefix_icon=Icon(icons.SEARCH, size=20, color=Themes.slate400),
            on_change=on_change
        )
        
