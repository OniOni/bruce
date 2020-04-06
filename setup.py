#!/usr/bin/env python

from setuptools import find_packages, setup  # type: ignore

setup(
    name="bruce-bld",
    version="0.0.8",
    description="Small Command Executor",
    author="Mathieu Sabourin",
    author_email="mathieu.c.sabourin@gmail.com",
    packages=find_packages("src/python"),
    package_dir={"": "src/python"},
    extras_require={
        'toml': [
            'toml'
        ]
    }
)
