from tools37 import CommandManager


class Indenter(CommandManager):
    def __init__(self, base_indent: str = "  "):
        self.level: int = 0
        self.base_indent: str = base_indent

    @bind_to(dict)
    def parse_dict(self, obj: dict) -> str:
        self.level += 1
        text = "{\n" + ",\n".join(f"{self.indent}{repr(key)}: {self(val)}" for key, val in obj.items())
        self.level -= 1
        return text + f"\n{self.indent}}}"

    @bind_to(list)
    def parse_list(self, obj: list) -> str:
        self.level += 1
        text = "[\n" + ",\n".join(f"{self.indent}{self(val)}" for val in obj)
        self.level -= 1
        return text + f"\n{self.indent}]"

    @bind_to(object)
    def parse_default(self, obj: object) -> str:
        return repr(obj)

    @property
    def indent(self):
        return self.level * self.base_indent


if __name__ == '__main__':
    indent = Indenter("\t")

    print(indent({"key1": "val1", "key2": 2, "list": [0, 1, 2, 3, "coucou"]}))
