import argparse

from ..cache import SimpleCacheManager
from ..exceptions import BruceError, FailedTaskException
from ..parser import parse
from ..toposort import toposort


def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="*", type=str, default="default")

    return parser.parse_args()


def main() -> None:
    args = setup()
    cache = SimpleCacheManager(path=".bruce/store.json")
    tasks = parse("Bruce.ini")

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


if __name__ == "__main__":
    main()
