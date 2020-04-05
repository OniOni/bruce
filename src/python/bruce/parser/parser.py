import configparser
from typing import Any, Dict, List, Type, Union

from ..builder import TYPE, Info, builder, get_info
from ..task import BaseTask


def to_list(s: str) -> List[str]:
    return [k.strip() for k in s.split(",")]


def to_value(s: str, type: TYPE) -> Union[str, List[str]]:
    return s.strip() if type == TYPE.STR else to_list(s)


def parse(filename: str) -> List[BaseTask]:
    cp = configparser.ConfigParser()
    with open(filename) as fp:
        cp.read_file(fp)

    task_info: Dict[str, Info] = {}
    for s in cp.sections():
        type, name = [k.strip() for k in s.split(":")]

        info = get_info(type)

        keys = {k: to_value(v, info.get(k)) for k, v in cp.items(s)}

        task_info[name] = info(name=name, **keys)  # type: ignore

    return builder(task_info)
