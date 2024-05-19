from flet import Text, Page, TextAlign
from theme.themes import Themes

class StyledText(Text):
    def init_font_family(page: Page):
        page.fonts = {
            "Outfit-Thin": "./font/Outfit-Thin.ttf",
            "Outfit-ExtraLight": "./font/Outfit-ExtraLight.ttf",
            "Outfit-Light": "./font/Outfit-Light.ttf",
            "Outfit-Regular": "./font/Outfit-Regular.ttf",
            "Outfit-Medium": "./font/Outfit-Medium.ttf",
            "Outfit-SemiBold": "./font/Outfit-SemiBold.ttf",
            "Outfit-Bold": "./font/Outfit-Bold.ttf",
            "Outfit-ExtraBold": "./font/Outfit-ExtraBold.ttf",
            "Outfit-Black": "./font/Outfit-Black.ttf",
        }

    def __init__(self, value: str, size: int = 14, color: str = Themes.slate950, weight: int = 700, text_align: str = None):
        font_family = ""
        if weight < 200: font_family = "Outfit-Thin"
        elif weight < 300: font_family = "Outfit-ExtraLight"
        elif weight < 400: font_family = "Outfit-Light"
        elif weight < 500: font_family = "Outfit-Regular"
        elif weight < 600: font_family = "Outfit-Medium"
        elif weight < 700: font_family = "Outfit-SemiBold"
        elif weight < 800: font_family = "Outfit-Bold"
        elif weight < 900: font_family = "Outfit-ExtraBold"
        else: font_family = "Outfit-Black"
        super().__init__(value=value, size=size, color=color, font_family=font_family, text_align=text_align)