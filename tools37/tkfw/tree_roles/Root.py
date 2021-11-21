from ..interfaces import Tree


class Root(Tree):
    """Tree which have no parent."""

    def _set_local(self, value):
        raise Exception

    def _get_local(self):
        raise Exception
