#!/usr/bin/env python3
import pathlib
import subprocess
import sys
from os import environ

DEFAULT_VERSION = "0.0.8"
DEFAULT_LOCATION = ".bruce"
DEFAULT_CONFIG_FILE = "Bruce.toml"
PYTHON_VERSION = f"python{sys.version_info.major}.{sys.version_info.minor}"


def mk_store(path: str) -> None:
    bruce_dir = pathlib.Path(path)

    if not bruce_dir.exists():
        bruce_dir.mkdir()
        bruce_dir.joinpath("store.json").write_text("{}")


def mk_venv(path: str) -> str:
    import venv  # type: ignore

    venv_path = f"{path}/venv"
    if not pathlib.Path(venv_path).exists():
        venv.create(venv_path, with_pip=True)

    return venv_path


def fetch(version: str, location: str) -> str:
    path = f"{location}/bruce_bld-{version}-py3-none-any.whl"

    if not pathlib.Path(path).exists():
        subprocess.run(
            [
                f"{location}/venv/bin/pip",
                "download",
                f"bruce-bld[toml]=={version}",
                "--isolated",
                "-d",
                ".bruce",
            ]
        )
    return path


def install(wheel: str, location: str) -> None:
    if not pathlib.Path(
        f"{location}/venv/lib/{PYTHON_VERSION}/site-packages/bruce"
    ).exists():
        subprocess.run(
            [
                f"{location}/venv/bin/pip",
                "install",
                "--no-cache-dir",
                "--isolate",
                "--no-index",
                "--find-links=.bruce",
                "bruce-bld[toml]",
            ]
        )


def bootstrap() -> None:
    location = environ.get("BRC_DIR", DEFAULT_LOCATION)
    version = environ.get("BRC_VER", DEFAULT_VERSION)

    mk_store(location)
    mk_venv(location)
    whl_path = fetch(version, location)
    install(whl_path, location)


def run() -> None:
    import sys

    path = (
        f".bruce/venv/lib/{PYTHON_VERSION}/site-packages/"
        if environ.get("BRC_DEV", 0) == 0
        else "src/python"
    )

    sys.path.insert(0, f".bruce/venv/lib/{PYTHON_VERSION}/site-packages/")
    sys.path.insert(0, path)

    from bruce.cli import main

    main(DEFAULT_CONFIG_FILE)


if __name__ == "__main__":
    bootstrap()
    run()
