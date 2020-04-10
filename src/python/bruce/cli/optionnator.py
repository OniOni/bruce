import os
from typing import Dict, List, Optional

try:
    import toml
except Exception:
    toml = None  # type: ignore


class OptionBackend:
    def get(self, key: str) -> Optional[str]:
        raise NotImplemented


class EnvBackend(OptionBackend):
    def get(self, key: str) -> Optional[str]:
        return os.environ.get(f"BRC_{key.upper()}", None)


class PyProjBackend(OptionBackend):
    def __init__(self, filename: str) -> None:
        self._store: Dict[str, str] = {} if not toml else toml.load(filename)["tool"][
            "bruce"
        ]

    def get(self, key: str) -> Optional[str]:
        return self._store.get(key, None)


class Optionnator:
    def __init__(self, backends: List[OptionBackend]) -> None:
        self._backends = backends

    def get(self, k: str, default: str) -> str:
        for b in self._backends:
            val = b.get(k)
            if val:
                return val

        return default
