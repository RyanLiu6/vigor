#!/usr/bin/env python3

import os
import click


NFO = "nfo"
MP4 = "mp4"

@click.command()
@click.argument("folder_path")
@click.option("--force/--no-force", help="Force generate NFO files", default=False)
def generate_nfo_file(folder_path: str, force: bool):
    """
    Generates NFO file for movies.

    This assumes that:
    1. All movies files exist under a common theme, in this case, their main poster actor.
    2. All main poster actor folders exist under a central folder, whose absolute path is given to the script at runtime.

    Args:
        folder_path (str): Root directory to explore and create NFO files for.
    """
    _generate_helper(folder_path=folder_path, force=force)


def _generate_helper(folder_path: str, force: bool):
    for item in os.walk(folder_path):
        # each item is 3-tuple of (dirpath, dirnames, filenames)
        current_path = item[0]
        current_directories = item[1]
        current_files = item[2]

        processed_files = {}
        for file_name in current_files:
            if file_name.endswith(NFO):
                processed_files[file_name.replace(NFO, MP4)] = file_name

        for file_name in current_files:
            if force:
                if file_name.endswith(MP4):
                    _create_nfo_file(file_name=file_name, directory=current_path)
            else:
                if file_name.endswith(MP4) and file_name not in processed_files:
                    _create_nfo_file(file_name=file_name, directory=current_path)

        for directory in current_directories:
            _generate_helper(folder_path=directory)


def _create_nfo_file(file_name: str, directory: str):
    with open("nfo_movie_template") as template:
        template_variables = dict(
            title=file_name,
            actor_name=os.path.basename(directory)
        )

        template = template.read().format(**template_variables)

    with open(os.path.join(directory, file_name.replace(MP4, NFO)), "w+") as f:
        f.write(template)


if __name__ == "__main__":
    generate_nfo_file()
