class Action:
    def __init__(self):
        self.obj = None

    def do(self, obj: object) -> None:
        raise NotImplementedError

    def undo(self) -> None:
        raise NotImplementedError

    def redo(self) -> None:
        raise NotImplementedError
