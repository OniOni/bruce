from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Mapping, Optional, Sequence, Type, Union, cast

from ..cache import ContentStrategy, FingerprintingStrategy, TimestampStrategy
from ..task import BaseTask, MetaTask, ShellTask
from ..watchable import BaseWatchable, File, Glob


class TYPE(Enum):
    LIST = auto()
    STR = auto()


def _to_type(typing_info: Any) -> TYPE:
    return TYPE.LIST if "Sequence" in str(typing_info) else TYPE.STR


DEFAULT_FINGERPRINTINGSTRATEGY = "timestamp"


@dataclass
class Info:
    name: str

    @classmethod
    def get(cls, k: str) -> TYPE:
        if k not in cls.__annotations__:
            raise Exception

        return _to_type(cls.__annotations__[k])

    @property
    def type(self) -> str:
        return self.__class__.__name__.lower()[:-4]


@dataclass
class TaskInfo(Info):
    cmd: str = field(default="")
    upstream: Sequence[str] = field(default_factory=list)
    watch: Sequence[str] = field(default_factory=list)


@dataclass
class GroupInfo(Info):
    upstream: Sequence[str] = field(default_factory=list)
    watch: Sequence[str] = field(default_factory=list)


@dataclass
class GlobInfo(Info):
    glob: str
    exclude: Sequence[str]
    fingerprintingstrategy: str = DEFAULT_FINGERPRINTINGSTRATEGY


@dataclass
class FileInfo(Info):
    path: str
    fingerprintingstrategy: str = DEFAULT_FINGERPRINTINGSTRATEGY


_INFO = {k.__name__.lower()[:-4]: k for k in [TaskInfo, GroupInfo, GlobInfo, FileInfo]}


def get_info(type: str) -> Type[Info]:
    return _INFO[type]


def strategy_builder(strategy_name: str) -> Optional[Type[FingerprintingStrategy]]:
    if strategy_name == "content":
        return ContentStrategy
    elif strategy_name == "timestamp":
        return TimestampStrategy
    else:
        return None


def builder(task_info: Dict[str, Info]) -> List[BaseTask]:
    done: Dict[str, BaseTask] = {}
    tasks = list(task_info.items())
    while tasks:
        inst: Union[BaseWatchable, BaseTask]
        name, info = tasks.pop(0)
        upstream: List[str] = getattr(info, "upstream", [])
        fingerprinting_strategy = strategy_builder(
            getattr(info, "fingerprintingstrategy", DEFAULT_FINGERPRINTINGSTRATEGY)
        )

        if not fingerprinting_strategy:
            raise Exception(
                f"No such fingerprinting strategy {getattr(info, 'fingerprintingstrategy', None)}"
            )

        if not upstream or len(upstream) == len(set(done) & set(upstream)):
            if isinstance(info, FileInfo):
                inst = File(
                    path=info.path, fingerprinting_strategy=fingerprinting_strategy
                )
            elif isinstance(info, GlobInfo):
                inst = Glob(
                    glob=info.glob,
                    fingerprinting_strategy=fingerprinting_strategy,
                    exclude=info.exclude,
                )
            elif isinstance(info, TaskInfo):
                watch = [done[s] for s in info.watch]
                upstream_ = [done[up] for up in upstream]
                inst = ShellTask(
                    name=name,
                    cmd=info.cmd,
                    upstream=upstream_,
                    watch=watch,  # type: ignore
                )
            elif isinstance(info, GroupInfo):
                watch = [done[s] for s in info.watch]
                upstream_ = [done[up] for up in upstream]
                inst = MetaTask(
                    name=name, cmd="", upstream=upstream_, watch=watch,  # type: ignore
                )
            else:
                raise Exception(f"Unhandled type: {info.type}")

            done[name] = inst  #  type: ignore
        else:
            tasks.append((name, info))

    return [v for v in done.values() if isinstance(v, BaseTask)]
