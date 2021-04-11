import os
from tools37 import MultiLang

SPLIT_CATEGORIES: bool = False

if __name__ == '__main__':
    if not os.path.exists("langs"):
        ml = MultiLang.from_data({
            "fr": {
                "GLOBAL": {
                    "TITLE": "titre",
                    "CONTENT": "contenu",
                    "RELOAD": "chargement du français"
                },
                "COLORS": {
                    "BLUE": "bleu",
                    "RED": "rouge",
                    "GREEN": "vert"
                }
            },
            "en": {
                "GLOBAL": {
                    "TITLE": "title",
                    "CONTENT": "content",
                    "RELOAD": "loading english"
                },
                "COLORS": {
                    "BLUE": "blue",
                    "RED": "red",
                    "GREEN": "green"
                }
            }
        })
        if SPLIT_CATEGORIES:
            ml.save_langs("global", category="GLOBAL")
            ml.save_langs("colors", category="COLORS")
        else:
            ml.save_langs("langs")
    else:
        ml = MultiLang()
        if SPLIT_CATEGORIES:
            ml.load_langs("global", category="GLOBAL")
            ml.load_langs("colors", category="COLORS")
        else:
            ml.load_langs("langs")

    ml.subscribe(lambda: print(ml["GLOBAL.RELOAD"]))

    ml.lang = "en"
    ml.lang = "fr"
    ml.lang = "sp"
    ml.lang = "gl"
