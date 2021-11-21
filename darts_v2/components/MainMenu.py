from tools37.tkfw import *
from ..constants import *


def play_button(name: str, label: str):
    disabled = name not in AVAILABLE_GAMES

    class Play(Button, Fill):
        PADDING = 10
        STYLE = style(Color.CLICKABLE, Border.BUTTON, **button_style, text=label, font=Font.XL)

        if disabled:
            STYLE['cursor'] = 'X_cursor'
            STYLE['state'] = 'disabled'
            STYLE['font'] = (*STYLE['font'], 'bold')
            STYLE['background'] = 'gray'

        def command(self):
            self.play(name)

    return Play


class MainMenu(LargeColumn, IF="menu == 'MAIN_MENU'"):
    """Menu principal affiché lorsque aucune partie n'est commencée."""
    STYLE = style(Color.DARK, Border.NULL, Padding.NULL)

    class Section1(Row):
        class Classic(LabelFrame, Horizontal, Fill):
            STYLE = style(Color.DARK, Border.BOX, Padding.M, text="Classique", font=Font.XL)

            Play301 = play_button(name='301', label='301')
            Play501 = play_button(name='501', label='501')
            Play801 = play_button(name='801', label='801')

    class Section2(Row):
        class Classic(LabelFrame, Horizontal, Fill):
            STYLE = style(Color.DARK, Border.BOX, Padding.M, text="Autres", font=Font.L)

            PlayCricket = play_button(name='cricket', label='Cricket'),
            PlayRTC = play_button(name='rtc', label='Around the clock'),
            PlayTraining = play_button(name='training', label='Training'),
