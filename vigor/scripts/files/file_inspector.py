#!/usr/bin/env python3

import re
import click
import filedate

from pathlib import Path
from datetime import datetime

from dateutil.parser import parse

def check_date(input_text):
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE)
    return pattern.search(input_text)


@click.command()
@click.argument("root_dir")
@click.option("--rename/--no-rename", default=False,
    help="If set, renames to the format of IMG_0001.*")
@click.option("--date/--no-date", default=False,
    help="If set, changes created date of file to a datetime found \
        in the name of the file")
def inspect_files(root_dir: str, date: bool, rename: bool):
    """
    Some of my files are timestamped, but that metadata was not preserved in certain cases.

    This script parses a file name, and if parseable, sets that file's creation date to the one
    described by the file name.

    Args:
        root_dir (str): Root Directory to scan.
    """
    root_path = Path(root_dir)
    files = [x for x in root_path.glob("**/*") if x.is_file()]
    files.sort()

    count = 0
    for file_path in files:
        file_name = file_path.name
        regex_result = check_date(file_name)
        if regex_result:
            if date:
                file_date = filedate.File(file_path)
                date = datetime.strptime(regex_result.group(), '%Y-%m-%d')
                file_date.set(created=date.strftime("%m/%d/%Y, %H:%M:%S"))

            if rename:
                count += 1
                new_path = Path(file_path.parent / f"IMG_{str(count).zfill(4)}{file_path.suffix}")
                file_path.rename(new_path)


if __name__ == "__main__":
    inspect_files()
