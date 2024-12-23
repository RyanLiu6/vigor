import os
import re

from setuptools import find_packages, setup


def read(filename: str) -> str:
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = str
    with open(filename, encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="vigor",
    version="0.2.2",
    url="https://github.com/RyanLiu6/vigor",
    license="MIT",
    author="Ryan Liu",
    author_email="ryan@ryanliu6.xyz",
    description=(
        "A collection of semi-random functions and scripts that I found useful "
        "for my own usage, packed into a Python library for ease-of-use."
    ),
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
