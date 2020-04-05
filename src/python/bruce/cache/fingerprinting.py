from hashlib import sha1
from os import stat
from typing import Any, List, overload


def hash_(elements: List[str]) -> str:
    m = sha1()
    for el in elements:
        m.update(el.encode())

    return m.hexdigest()


class FingerprintingStrategy:
    @classmethod
    def fingerprint(cls, obj: Any) -> str:
        raise NotImplementedError


class TimestampStrategy(FingerprintingStrategy):
    @classmethod
    def fingerprint(cls, path: str) -> str:
        try:
            stat_info = stat(path)
            return hash_([str(stat_info.st_mtime)])
        except FileNotFoundError:
            return hash_([""])


class ContentStrategy(FingerprintingStrategy):
    @classmethod
    def fingerprint(cls, path: str) -> str:
        with open(path) as f:
            return hash_(f.readlines())
