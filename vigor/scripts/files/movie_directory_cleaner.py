#!/usr/bin/env python3

import click

from pathlib import Path


@click.command()
@click.argument("root_dir")
def clean_directory(root_dir: str):
    """
    Finds movies in root_dir that are "loose" ie not in a directory
    of its own, and creates a directory for it.

    Args:
        root_dir (str): Root Directory to scan. Does not scan directories
            inside root_dir.
    """
    root_path = Path(root_dir)
    files = [x for x in root_path.glob("**/*") if x.is_file()]

    for file_path in files:
        if file_path.suffix == ".nfo":
            continue
        else:
            new_folder = Path(root_path / file_path.stem)
            Path.mkdir(new_folder)
            file_path.rename(new_folder / file_path.name)

            info_path = Path(root_path / f"{file_path.stem}.nfo")
            if info_path.is_file:
                info_path.rename(new_folder / info_path.name)


if __name__ == "__main__":
    clean_directory()
