from dataclasses import dataclass
from functools import reduce
from operator import xor
from os import stat
from pathlib import Path
from typing import List

from ..cache import Cacheable


class BaseWatchable(Cacheable):
    def fingerprint(self) -> str:
        raise NotImplementedError


@dataclass
class File(BaseWatchable):
    path: str


class Timestamp(File):
    def fingerprint(self) -> str:
        try:
            stat_info = stat(self.path)
            return self._hash([str(stat_info.st_mtime)])
        except FileNotFoundError:
            return self._hash([""])


@dataclass
class Glob(BaseWatchable):
    glob: str

    def fingerprint(self) -> str:
        return self._hash(
            [Timestamp(str(p)).fingerprint() for p in Path(".").glob(self.glob)]
        )
