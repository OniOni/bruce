import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence, Type

from ..cache import Cacheable, FingerprintingStrategy


@dataclass
class BaseWatchable(Cacheable):
    fingerprinting_strategy: Type[FingerprintingStrategy]

    def fingerprint(self) -> str:
        raise NotImplementedError


@dataclass
class File(BaseWatchable):
    path: str

    def fingerprint(self) -> str:
        return self.fingerprinting_strategy.fingerprint(self.path)


@dataclass
class Glob(BaseWatchable):
    glob: str
    exclude: Sequence[str] = field(default_factory=list)

    def fingerprint(self) -> str:
        exclude = re.compile("|".join(self.exclude))

        return self._hash(
            [
                self.fingerprinting_strategy.fingerprint(str(p))
                for p in Path(".").glob(self.glob)
                if not self.exclude or not exclude.match(str(p))
            ]
        )
