#!/usr/bin/env python3
import pathlib
import subprocess
from os import environ


def mk_venv(path: str = ".bruce/venv") -> str:
    import venv  # type: ignore

    if not pathlib.Path(path).exists():
        venv.create(path, with_pip=True)

    return path


def fetch(version: str = "0.0.1") -> str:
    path = f".bruce/bruce_bld-{version}-py3-none-any.whl"

    if not pathlib.Path(path).exists():
        subprocess.run(
            [".bruce/venv/bin/pip", "download", f"bruce-bld=={version}", "-d", ".bruce"]
        )
    return path


def install(wheel: str) -> None:
    if not pathlib.Path(".bruce/venv/lib/python3.7/site-packages/bruce").exists():
        subprocess.run([".bruce/venv/bin/pip", "install", "--no-cache-dir", wheel])


def bootstrap() -> None:
    bruce_dir = pathlib.Path(".bruce")

    if not bruce_dir.exists():
        bruce_dir.mkdir()
        bruce_dir.joinpath("store.json").write_text("{}")

    mk_venv()
    whl_path = fetch()
    install(whl_path)


def run() -> None:
    import sys

    path = (
        ".bruce/venv/lib/python3.7/site-packages/"
        if environ.get("DEV", 0) == 0
        else "src/python"
    )

    sys.path.insert(0, path)

    from bruce.cli import main

    main()


if __name__ == "__main__":
    bootstrap()
    run()
