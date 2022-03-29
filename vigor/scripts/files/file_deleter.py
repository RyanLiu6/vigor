#!/usr/bin/env python
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="File deleter")
    parser.add_argument("input_file", help="A text file containing information to process.")
    parser.add_argument("root_dir", help="Absolute path to root directory for deletion.")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="If set, does not actually delete files and only prints out information \
                             about files that would be deleted.")

    args = parser.parse_args()

    return args.input_file, args.root_dir, args.dry_run


def process_request(input_file: str, root_dir: str, dry_run: bool) -> None:
    """
    Processes CLI calls.

    Args:
        input_file (str): Text file containing filenames to delete.
        root_dir (str): Root directory to explore and delete files for.
        dry_run (bool): If True, will not remove any files.
    """
    to_delete = set()
    with open(input_file, "r", encoding="utf-8") as read_file:
        for line in read_file:
            to_delete.add(line.strip())

    print(f"Files to delete are: {to_delete}")

    for item in os.walk(root_dir):
        # each item is 3-tuple of (dirpath, dirnames, filenames)
        current_path = item[0]
        current_files = set(item[2])

        matching = to_delete & current_files

        if matching:
            print(f"Found files: {matching} in folder {current_path}")

            if not dry_run:
                for item in matching:
                    os.remove(os.path.join(current_path, item))

                print(f"Removed files: {matching} from folder {current_path}")


if __name__ == "__main__":
    args = parse_args()

    process_request(*args)
