#!/usr/bin/env python3
import pathlib

def mk_venv(path: str = ".bruce/venv") -> str:
    import venv  # type: ignore
    if not pathlib.Path(path).exists:
        venv.create(path, with_pip=True)

    return path


def fetch(version: str = "0.0.1") -> str:
    return f".bruce/bruce-{version}-py3-none-any.whl"


def install(wheel: str) -> None:
    import subprocess
    subprocess.run([".bruce/venv/bin/pip", "install", "--no-cache-dir", wheel])


def bootstrap() -> None:
    mk_venv()
    whl_path = fetch()
    install(whl_path)


def run() -> None:
    import sys
    sys.path.insert(0, ".bruce/venv/lib/python3.7/site-packages/")

    from bruce.cli import main
    main()


if __name__ == "__main__":
    bootstrap()
    run()
