#!/usr/bin/env python

import argparse
import os
from os import PathLike
from pathlib import Path
from typing import Optional, Tuple, Union

from git import InvalidGitRepositoryError, Repo


def parse_args() -> Tuple[str, bool]:
    parser = argparse.ArgumentParser(
        description="Checks git status for all directories under root_dir"
    )
    parser.add_argument(
        "--root_dir",
        default=Path.home(),
        help="Absolute path to root folder for checking.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Quiet mode, only prints out information for repos with changes.",
    )

    args = parser.parse_args()

    return args.root_dir, args.quiet


def get_repo_name(repo_path: Union[str, PathLike[str]]) -> str:
    """
    Get repository name from path.

    Args:
        repo_path: Path to repository

    Returns:
        str: Repository name
    """
    path_str = str(repo_path)  # Convert PathLike to str
    return path_str.split(os.sep)[-1]


def process_request(root_dir: Union[str, PathLike[str]], quiet: bool = False) -> None:
    """
    Process git status for all directories under root_dir.

    Args:
        root_dir: Root directory to check
        quiet: If True, only print repos with changes
    """
    if not os.path.exists(root_dir):
        raise ValueError(f"Directory {root_dir} does not exist!")

    for item in os.scandir(root_dir):
        if not item.is_dir():
            continue

        try:
            repo = Repo(item.path)
            if not repo.bare:
                repo_name = get_repo_name(item.path)
                branch = repo.active_branch
                repo_path = repo.working_tree_dir

                if (
                    repo.is_dirty()
                    or repo.untracked_files
                    or len(list(repo.iter_commits(f"{branch}@{{u}}..{branch}"))) != 0
                ):
                    print(
                        "======================================================================================="
                    )
                    print(f"Code changes in {repo_name} located at {repo_path}")
                    print(repo.git.status())
                else:
                    if quiet:
                        continue
                    else:
                        print(
                            "======================================================================================="
                        )
                        print(f"No changes in {repo_name} located at {repo_path}")
                print()
        except InvalidGitRepositoryError:
            continue


def get_git_repo(path: str) -> Optional[Repo]:
    """
    Returns a git.Repo object if path refers to a Git Repo, else,
    return None.

    Args:
        path (str): Absolute path of the folder.

    Returns:
        Optional[git.Repo]: The git.Repo object referring to parameter
            path, or None.
    """
    try:
        repo = Repo(path)
        return repo
    except InvalidGitRepositoryError:
        return None


if __name__ == "__main__":
    args = parse_args()

    process_request(*args)
