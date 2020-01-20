import json
from dataclasses import dataclass
from typing import Any, List

from .fingerprinting import hash_


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
    path: str

    def changed(self, obj: Cacheable) -> bool:
        with open(self.path) as doc:
            store = json.load(doc)

        if obj.key in store:
            return bool(store[obj.key] != obj.fingerprint())

        return True

    def cache(self, obj: Cacheable) -> bool:
        with open(self.path) as doc:
            store = json.load(doc)

        store[obj.key] = obj.fingerprint()

        with open(self.path, mode="w") as doc:
            json.dump(store, doc)

        return True
