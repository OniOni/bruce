import shlex
import subprocess
from dataclasses import dataclass, field
from functools import reduce
from hashlib import md5
from operator import xor
from typing import List, Optional, cast

from ..cache import BaseCacheManager, Cacheable
from ..exceptions import FailedTaskException
from ..watchable import BaseWatchable


@dataclass
class BaseTask(Cacheable):
    cmd: str
    name: str
    upstream: List["BaseTask"] = field(default_factory=list)
    watch: List[BaseWatchable] = field(default_factory=list)

    def fingerprint(self) -> str:
        els = [el.fingerprint() for el in cast(List[Cacheable], self.watch)]
        els.append(self.cmd)

        return self._hash(els)

    @property
    def key(self) -> str:  # type: ignore
        return self.name

    def exec(self) -> bool:
        raise NotImplementedError

    def run(self, cache: BaseCacheManager) -> bool:
        if cache.changed(self):
            if self.exec():
                cache.cache(self)
            else:
                raise FailedTaskException(f'Task "{self.key}" failed.')

            return True

        return False


class PrintTask(BaseTask):
    def exec(self) -> bool:
        print(f"{self.name}: {self.cmd}")

        return True


class ShellTask(BaseTask):
    def exec(self) -> bool:
        res = subprocess.run(self.cmd, shell=True, stdout=subprocess.PIPE)
        print(res.stdout.decode().strip())

        return res.returncode == 0


class MetaTask(BaseTask):
    def exec(self) -> bool:
        return True
