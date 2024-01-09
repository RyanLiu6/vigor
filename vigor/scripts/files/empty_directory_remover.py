#!/usr/bin/env python3

import os
import shutil

import click


to_delete = []

@click.command()
@click.argument("root_dir")
@click.option("--dry-run", is_flag=True, default=False, help="Dry Run")
@click.option("-r", "--recursive", is_flag=True, default=False, help="Should recursively check sub-directories")
def remove_empty_directories(root_dir: str, dry_run: bool, recursive: bool):
    """
    Finds folders in root_dir that only contain an .nfo file, without a corresponding media file.
    In this case, these folders are "empty", and should be removed.

    Args:
        root_dir (str): Root Directory to scan. Only looks at first level subdirectories.
    """
    inner_function(root_dir=root_dir, recursive=recursive)

    for item in to_delete:
        file_path = os.path.join(item[1], item[0])
        print(f"Deleting file {file_path} and directory {item[1]}")
        if not dry_run:
            os.remove(file_path)
            os.rmdir(item[1])


def inner_function(root_dir: str, recursive: bool):
    for path, subdir, files in os.walk(root_dir):
        if len(files) == 1 and ".nfo" in files[0]:
            to_delete.append((files[0], path))

        if recursive:
            for sub in subdir:
                inner_function(root_dir=sub, recursive=recursive)


if __name__ == "__main__":
    remove_empty_directories()
