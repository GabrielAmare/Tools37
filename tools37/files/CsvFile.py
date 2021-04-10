from typing import List
from .BaseFile import BaseFile


class CsvFile(BaseFile):
    extension = ".csv"

    @classmethod
    def _save_line(cls, keys: List[str], vals: dict):
        return "\n" + ",".join(str(vals.get(key, '')) for key in keys)

    @classmethod
    def save(cls, fp: str, keys: List[str], data: List[dict]) -> None:
        with cls._open_w(fp) as file:
            file.write(",".join(keys))
            for vals in data:
                file.write(cls._save_line(keys, vals))

    @classmethod
    def _load_line(cls, line: str):
        return tuple(map(str.strip, line.split(",")))

    @classmethod
    def load(cls, fp: str) -> dict:
        with cls._open_r(fp) as file:
            keys = None
            for line in file.readlines():
                if keys is None:
                    keys = cls._load_line(line)
                else:
                    vals = cls._load_line(line)
                    yield dict(zip(keys, vals))
