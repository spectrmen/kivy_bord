from kivy.core.text import LabelBase
KIVY_FONTS = [
    {
        "name": "Alegreya",
        "fn_regular": "fonts/Alegrea/Alegreya-Regular.otf",
        "fn_bold": "fonts/Alegrea/Alegreya-Bold.otf",
        "fn_italic": "fonts/Alegrea/Alegreya-Italic.otf",
        "fn_bolditalic": "fonts/Alegrea/Alegreya-BoldItalic.otf"
    },
    {
        "name":"Aston",
        "fn_regular":"fonts/ASTONISHED.ttf"
    },
    {
        "name":"Alice",
        "fn_regular": "fonts/Alice-Regular.ttf"
    },
    {
        "name": "Charis",
        "fn_regular": "fonts/Charis/CharisSILR.ttf",
        "fn_bold": "fonts/Charis/CharisSILB.ttf",
        "fn_italic": "fonts/Charis/CharisSILI.ttf",
        "fn_bolditalic": "fonts/Charis/CharisSILBI.ttf"
    },
    {
        "name": "icons",
        "fn_regular": "fonts/Font Awesome 5 Free-Solid-900.otf"
    }

]
def import_fonts():
    global KIVY_FONTS
    for font in KIVY_FONTS:
        LabelBase.register(**font)
    print("добавил")
