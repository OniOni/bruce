import argparse
from parser import parse

from cache import SimpleCacheManager
from toposort import toposort


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
        ran = n.task.run(cache)
        if not ran:
            print("Unmodified.")


if __name__ == "__main__":
    main()
