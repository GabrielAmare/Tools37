from .Action import Action


class SetItem(Action):
    def __init__(self, key: str, val: object):
        super().__init__()
        self.key = key
        self.had = None
        self.old = None
        self.val = val

    def do(self, obj: dict) -> None:
        self.obj = obj
        self.had = self.key in self.obj
        self.old = self.obj[self.key] if self.had else None
        self.obj[self.key] = self.val

    def undo(self) -> None:
        if self.had:
            self.obj[self.key] = self.old
        else:
            del self.obj[self.key]

    def redo(self) -> None:
        self.obj[self.key] = self.val
