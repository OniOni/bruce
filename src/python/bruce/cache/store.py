import json
import pathlib
from typing import Dict, Iterator


class JsonStore(Dict[str, str]):
    def __init__(self, path: str) -> None:
        self.path = pathlib.Path(path)

        if not self.path.exists():
            self.path.write_text("{}")

    def reload(self) -> None:
        with self.path.open() as fd:
            doc = json.load(fd)

        self.clear()
        for k, v in doc.items():
            super().__setitem__(k, v)

    def flush(self) -> None:
        with self.path.open(mode="w") as fd:
            json.dump({k: v for k, v in super().items()}, fd)

    def __getitem__(self, k: str) -> str:
        self.reload()
        return super().__getitem__(k)

    def __setitem__(self, k: str, v: str) -> None:
        super().__setitem__(k, v)
        self.flush()

    def __delitem__(self, k: str) -> None:
        super().__delitem__(k)
        self.flush()

    def __iter__(self) -> Iterator[str]:
        self.reload()
        return super().__iter__()

    def __len__(self) -> int:
        self.reload()
        return super().__len__()
