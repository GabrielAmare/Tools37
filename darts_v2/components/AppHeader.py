from tools37.tkfw import *
from ..constants import *


class AppHeader(Row):
    STYLE = style(Color.LIGHT, Border.NULL, Padding.NULL)
    PADDING = 8

    class Title(Label):
        STYLE = style(Color.LIGHT, anchor=tk.W, padx=20, text='Darts', font=Font.XXL)

    class Version(Label, Fill):
        STYLE = style(Color.LIGHT, anchor=tk.SW, padx=0, text='v2.0.0', font=Font.S)

        class MainMenu(Button, IF="menu != 'MAIN_MENU'"):
            STYLE = style(Color.CLICKABLE, Border.BUTTON, **button_style, text="Menu principal", width=16)

            def command(self):
                self.set_menu('MAIN_MENU')

        class ScoreBoard(Button, IF="menu != 'PARTY' and game"):
            STYLE = style(Color.CLICKABLE, Border.BUTTON, **button_style, text="Partie en cours", width=16)

            def command(self):
                self.set_menu('PARTY')

    class Quit(Button):
        STYLE = style(Color.CLICKABLE, Border.BUTTON, **button_style, text="Quitter", font=Font.L)

        def command(self):
            self.quit()
