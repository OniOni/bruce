from dataclasses import dataclass
from typing import Any, Dict, List

from .fingerprinting import hash_
from .store import JsonStore


class Cacheable:
    key: str

    def fingerprint(self) -> str:
        raise NotImplementedError

    def _hash(self, elements: List[str]) -> str:
        return hash_(elements)


@dataclass
class BaseCacheManager:
    def changed(self, obj: Cacheable) -> bool:
        raise NotImplementedError

    def cache(self, obj: Cacheable) -> bool:
        raise NotImplementedError


@dataclass
class SimpleCacheManager(BaseCacheManager):
    store: Dict[str, str]

    @classmethod
    def get(cls, path: str, format: str = "json") -> "SimpleCacheManager":
        if format == "json":
            store = JsonStore(path=path)
            # For some reason, if I don't call reload here,
            # the default __getitem__ method gets called.
            # TODO(mathieu): Figure this out.
            # -- Mathieu
            store.reload()

            return cls(store=store)
        else:
            raise Exception

    def changed(self, obj: Cacheable) -> bool:
        if obj.key in self.store:
            return bool(self.store[obj.key] != obj.fingerprint())

        return True

    def cache(self, obj: Cacheable) -> bool:
        self.store[obj.key] = obj.fingerprint()

        return True
