from tools37.tkfw import *
from .AppHeader import AppHeader
from .MainMenu import MainMenu
from ..constants import *


class App(Tk, Vertical):
    STYLE = style(Color.DARK, Border.NULL, Padding.NULL)
    DATA = {
        'menu': 'MAIN_MENU',
        'game': '',
        'party_status': 'BEFORE',
        'party': None,
        'existing_players': [
            {'name': 'Julien', 'exists': True},
            {'name': 'Jean-Pierre', 'exists': True},
            {'name': 'Jean-Gab', 'exists': True}
        ]
    }

    def set_menu(self, value: str):
        self.data['menu'] = value

    def set_game(self, name: str):
        assert name in AVAILABLE_GAMES
        self.data['game'] = name

        if name in ['301', '501', '801']:
            self.data['party_status'] = 'BEFORE'
            self.data['party'] = {
                'init_score': int(name),
                'players': [],
                'scores': []
            }
        else:
            raise NotImplementedError

    def play(self, name: str):
        self.set_game(name)
        self.set_menu('PARTY')

    AppHeader = AppHeader

    class AppBody(LargeRow):
        MainMenu = MainMenu
