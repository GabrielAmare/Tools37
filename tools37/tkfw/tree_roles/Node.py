from ..interfaces import Tree


class Node(Tree):
    """Tree which must have a parent and may have childs."""

    def _set_local(self, value):
        raise Exception

    def _get_local(self):
        raise Exception
