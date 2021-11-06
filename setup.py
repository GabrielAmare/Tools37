from install37 import setup
from tools37.__meta__ import __version__

if __name__ == "__main__":
    setup(
        name="tools37",
        version=__version__,
        author="Gabriel Amare",
        author_email="gabriel.amare.dev@gmail.com",
        description="various tools & utilitaries for python 3.7",
        url="https://github.com/GabrielAmare/Tools37",
        packages=[
            "tools37",
            "tools37.actions",
            "tools37.algebra",
            "tools37.console",
            "tools37.events",
            "tools37.files",
            "tools37.geom",
            "tools37.graphic",
            "tools37.physics",
            "tools37.text",
        ],
        classifiers=[],
        python_requires=">=3.7"
    )
