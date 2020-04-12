import argparse

from ..cache import SimpleCacheManager
from ..exceptions import BruceError, FailedTaskException
from ..parser import parse
from ..toposort import toposort
from .optionnator import EnvBackend, Optionnator, PyProjBackend


def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="*", type=str, default="")

    return parser.parse_args()


def main(configfile: str) -> None:
    args = setup()
    opts = Optionnator(backends=[EnvBackend(), PyProjBackend("pyproject.toml")])
    cache = SimpleCacheManager.get(
        path=opts.get("store", ".bruce/store.json"),
        format=opts.get("store_format", "json"),
    )
    tasks = parse(opts.get("configfile", "Bruce.toml"))

    task_names = [t.key for t in tasks]
    for t in args.tasks:
        if t not in task_names:
            print(f'Could not find task named "{t}".')
            print(f"Available tasks are: {task_names}")
            exit(1)

    for n in toposort(tasks, args.tasks):
        print(f"Executing {n.task.name}:")
        try:
            ran = n.task.run(cache)
        except BruceError as e:
            print(e)
            exit(1)

        if not ran:
            print("Unmodified.")
