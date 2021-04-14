from .Action import Action


class Append(Action):
    def __init__(self, item: object):
        super().__init__()
        self.item = item

    def do(self, obj: list) -> None:
        self.obj = obj
        self.obj.append(self.item)

    def undo(self) -> None:
        self.obj.pop(-1)

    def redo(self) -> None:
        self.obj.append(self.item)
