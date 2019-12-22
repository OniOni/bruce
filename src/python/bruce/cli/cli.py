import argparse

from ..cache import SimpleCacheManager
from ..parser import parse
from ..task import FailedTaskException
from ..toposort import toposort


def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="*", type=str, default="default")

    return parser.parse_args()


def main() -> None:
    args = setup()
    cache = SimpleCacheManager(path=".bruce/store.json")
    tasks = parse("Bruce.ini")

    for n in toposort(tasks, args.tasks):
        print(f"Executing {n.task.name}:")
        try:
            ran = n.task.run(cache)
        except FailedTaskException as e:
            print(e)
            exit(1)

        if not ran:
            print("Unmodified.")


if __name__ == "__main__":
    main()
