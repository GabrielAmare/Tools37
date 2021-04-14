from typing import List
from .Action import Action


class ActionManager:
    def __init__(self, target):
        self.target: object = target
        self.actions: List[Action] = []
        self.index: int = 0  # points to the position of the next action

    def do(self, *actions: Action):
        assert actions
        self.actions = self.actions[:self.index]

        for action in actions:
            action.do(self.target)
            self.actions.append(action)

        self.index += len(actions)

    def undo(self, n: int = 1):
        # in the end self.index will be equal to self.index - n, we need to make sure self.index >= 0
        # so :
        assert n > 0
        assert self.index >= n
        for i in range(n):
            self.actions[self.index - 1 - i].undo()

        self.index -= n

    def redo(self, n: int = 1):
        # in the end self.index will be equal to self.index + n, we need to make sure self.index <= len(self.actions)
        # so :
        assert n > 0
        assert len(self.actions) - self.index >= n
        for i in range(n):
            self.actions[self.index + i].redo()

        self.index += n
