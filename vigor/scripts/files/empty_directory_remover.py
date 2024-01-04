#!/usr/bin/env python3

import os
import shutil

import click

from pathlib import Path


@click.command()
@click.argument("root_dir")
def remove_empty_directories(root_dir: str):
    """
    Finds folders in root_dir that only contain an .nfo file, without a corresponding media file.
    In this case, these folders are "empty", and should be removed.

    Args:
        root_dir (str): Root Directory to scan. Only looks at first level subdirectories.
    """
    to_delete = []

    for path, _, files in os.walk(root_dir):
        if len(files) == 1 and ".nfo" in files[0]:
            to_delete.append((files[0], path))


    for item in to_delete:
        print(f"Deleting file {item[0]} and directory {item[1]}")
        os.remove(os.path.join(item[1], item[0]))
        os.rmdir(item[1])


if __name__ == "__main__":
    remove_empty_directories()
