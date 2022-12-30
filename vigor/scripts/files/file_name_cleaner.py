#!/usr/bin/env python3

import click

from pathlib import Path


@click.command()
@click.argument("root_dir")
@click.argument("to_replace")
@click.option("-mw", "magic_word", default="")
def clean_file_names(root_dir: str, to_replace: str, magic_word: str):
    """
    Replaces any instances of "to_replace" with "magic_word".

    Args:
        root_dir (str): Root Directory to scan.
        to_replace (str): The word to replace.
        magic_word (str): The word that replaces to_replace.
    """
    root_path = Path(root_dir)
    files = [x for x in root_path.glob("**/*") if x.is_file()]

    for file_path in files:
        file_name = file_path.name
        if to_replace in file_name:
            new_path = Path(file_path.parent / file_name.replace(to_replace, magic_word))
            file_path.rename(new_path)


if __name__ == "__main__":
    clean_file_names()
