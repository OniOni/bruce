from typing import Dict, List

import toml

from ..builder import builder, get_info
from ..task import BaseTask


def parse(filename: str) -> List[BaseTask]:
    doc = toml.load(filename)

    task_info = {}
    for type_, inst in doc.items():
        for name, info in inst.items():
            task_info[name] = get_info(type_)(name=name, **info)  # type: ignore

    return builder(task_info)
