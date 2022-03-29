#!/usr/bin/env python
import os
import argparse

from typing import List

from hurry.filesize import size


def parse_args():
    parser = argparse.ArgumentParser(description="Directory Explorer")
    parser.add_argument("root_dir", help="Absolute path to root directory to explore.")

    args = parser.parse_args()

    return args


def process_request(root_dir: str) -> None:
    """
    Processes CLI calls.

    Args:
        root_dir (str): Root directory to explore and print information for.
    """
    for item in os.walk(root_dir):
        # each item is 3-tuple of (dirpath, dirnames, filenames)
        current_path = item[0]
        current_directories = item[1]
        current_files = item[2]

        print_directory(current_path, current_files)

        for directory in current_directories:
            process_request(directory)


def print_directory(directory_path: str, directory_files: List[str]) -> None:
    """
    Prints all files and their sizes for a given directory.

    Args:
        directory_path (str): Path to directory.
        directory_files (List[str]): List of files found inside the directory.
    """
    total_size = 0

    print("=====================================")
    print(f"Directory: {directory_path}")

    for file_name in directory_files:
        file_path = os.path.join(directory_path, file_name)
        current_size = os.path.getsize(file_path)
        print(f"File: {file_path} | Size: {size(current_size)}")
        total_size += current_size

    print(f"Total Size: {size(total_size)}")


if __name__ == "__main__":
    args = parse_args()

    process_request(args.root_dir)
