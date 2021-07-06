from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from tools37.files import CsvFile


class Entry:
    KEYS = ['at', 'code', 'content']

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(at=datetime.fromisoformat(data['at']), code=data['code'], content=data['content'])

    def to_dict(self) -> Dict[str, str]:
        return dict(at=self.at.isoformat(), code=self.code, content=self.content)

    @classmethod
    def new(cls, code: str, content: str) -> Entry:
        return cls(at=datetime.now(), code=code, content=content)

    def __init__(self, at: datetime, code: str, content: str):
        self.at: datetime = at
        self.code: str = code
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}({self.at!r}, {self.code!r}, {self.content!r})"


class Log:
    @classmethod
    def load(cls, fp: str, auto_save: bool = False) -> Log:
        """Load a .csv as log content"""
        if CsvFile.exists(fp):
            data = CsvFile.load(fp)
        else:
            if auto_save:
                CsvFile.save(fp=fp, keys=Entry.KEYS, data=[])
            data = []

        return cls(data=list(map(Entry.from_dict, data)), fp=fp, auto_save=auto_save)

    def save(self, fp: str = '') -> None:
        """Save the log content to a .csv file"""
        fp = fp or self.fp
        assert fp
        CsvFile.save(fp=fp, keys=Entry.KEYS, data=list(map(Entry.to_dict, self.data)))
        self.fp = fp

    def __init__(self, data: List[Entry] = None, fp: str = '', auto_save: bool = False):
        self.data: List[Entry] = data or []
        self.fp: str = fp
        self.auto_save: bool = auto_save

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def new(self, code: str, content: str) -> Entry:
        entry = Entry.new(code=code, content=content)
        self.data.append(entry)
        if self.auto_save and self.fp:
            CsvFile.add(fp=self.fp, keys=Entry.KEYS, data=entry.to_dict())
        return entry

    def findall(self, min_at: datetime = None, max_at: datetime = None, code: str = None):
        def criteria(entry):
            if min_at and entry.at < min_at:
                return False

            if max_at and entry.at > max_at:
                return False

            if code and entry.code != code:
                return False

            return True

        return filter(criteria, self)


def main():
    from random import randint

    log = Log.load('test_log', True)

    session_start = log.new('session', 'calculating some divisions')

    for _ in range(randint(100, 200)):
        x = randint(-10, 10)
        y = randint(-10, 10)

        try:
            r = x / y
            log.new('success', f"{x!r} / {y!r} = {r!r}")
        except Exception as error:
            log.new('error', f"{x!r} / {y!r} -> {error}")

    print()
    print('all log sessions')
    for entry in log.findall(code='session'):
        print(entry)

    session_successes = list(log.findall(code='success', min_at=session_start.at))
    session_errors = list(log.findall(code='error', min_at=session_start.at))
    n_successes = len(session_successes)
    n_errors = len(session_errors)
    n_attempts = n_errors + n_successes

    print()
    print('current session errors')
    for entry in session_errors:
        print(entry)

    print()
    print('current session infos')
    print(f'number of attempts = {n_attempts}')
    print(f'number of errors = {n_errors}')
    print(f'number of successes = {n_successes}')
    print(f'error percent = {int((100 * n_successes) / n_attempts)}%')


if __name__ == '__main__':
    main()
