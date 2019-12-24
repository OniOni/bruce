import configparser
from typing import Any, Dict, List, Union

from ..task import BaseTask, ShellTask
from ..watchable import BaseWatchable, Glob, Timestamp


def parse(filename: str) -> List[BaseTask]:
    cp = configparser.ConfigParser()
    with open(filename) as fp:
        cp.read_file(fp)

    task_info: Dict[str, Any] = {}
    for s in cp.sections():
        type, name = [k.strip() for k in s.split(":")]
        task_info[name] = {
            "type": type,
        }

        upstream_info = cp.get(s, "upstream", fallback=None)
        task_info[name]["upstream"] = (
            [k.strip() for k in upstream_info.split(",")] if upstream_info else []
        )
        cp.remove_option(s, "upstream")

        task_info[name]["keys"] = {k: v for k, v in cp.items(s)}

    done: Dict[str, BaseTask] = {}
    tasks = list(task_info.items())
    while tasks:
        inst: Union[BaseWatchable, BaseTask]
        name, info = tasks.pop(0)
        upstream: List[str] = info["upstream"]
        if not upstream or len(upstream) == len(set(done) & set(upstream)):
            if info["type"] == "file":
                inst = Timestamp(**info["keys"])
            elif info["type"] == "glob":
                inst = Glob(
                    glob=info["keys"]["glob"],
                    exclude=info["keys"]["exclude"].split(",")
                    if "exclude" in info["keys"]
                    else [],
                )
            elif info["type"] == "task":
                watch_info = info["keys"].pop("watch", None)
                watch = [s.strip() for s in watch_info.split(",")] if watch_info else []
                inst = ShellTask(
                    name,
                    upstream=[done[up] for up in upstream],
                    watch=[done[w] for w in watch],  # type: ignore
                    **info["keys"]
                )
            else:
                raise Exception("Unhandled type")

            done[name] = inst  #  type: ignore
        else:
            tasks.append((name, info))

    return [v for v in done.values() if isinstance(v, BaseTask)]
