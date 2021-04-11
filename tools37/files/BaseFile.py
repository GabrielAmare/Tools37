import os


class BaseFile:
    extension: str = ""

    @classmethod
    def _parse_fp(cls, fp: str) -> str:
        if fp.endswith(cls.extension):
            return fp
        else:
            return fp + cls.extension

    @classmethod
    def _open_w(cls, fp: str):
        try:
            return open(cls._parse_fp(fp), mode="w", encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(os.path.abspath(e.filename))

    @classmethod
    def _open_r(cls, fp: str):
        try:
            return open(cls._parse_fp(fp), mode="r", encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(os.path.abspath(e.filename))
