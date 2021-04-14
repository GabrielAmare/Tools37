import os
import time
from tools37 import Console

if __name__ == '__main__':
    """
        Overview example of the functionalities of the Console object
    """
    console = Console()

    for x in console.iter("X", list(range(5))):
        for y in console.iter("Y", list(range(5))):
            console.log(f"({x}, {y})")
    print()
    for x in console.iter("X", list(range(5))):
        console.log(str(x))
        time.sleep(1)
    print()
    console.print("a single line message !")
    print()
    console.print("a multiline\nmessage !")
    print()
    console.error("an error\non multiple\nlines !")
    print()
    console.warn("a warning\non multiple\nlines /!\\")
    print()
    console.sql("CREATE TABLE user;")
    print()
    console.file(os.path.abspath(os.curdir))
    print()
    console.url("https://www.github.com")
    print()
    with console.action("action1"):
        with console.action("action2"):
            console.log("hello !")
    print()
    first_name = console.input("enter you first name :")
    last_name = console.input("enter you last name :")
    console.log(f"your name is {first_name.capitalize()} {last_name.capitalize()} !")
