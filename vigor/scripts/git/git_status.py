#!/usr/bin/env python

import os
import argparse

from pathlib import Path
from typing import Optional
from git import Repo, GitCommandError, InvalidGitRepositoryError


def parse_args():
    parser = argparse.ArgumentParser(description="Checks git status for all directories under root_dir")
    parser.add_argument("--root_dir", default=Path.home(),
                        help="Absolute path to root folder for checking.")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
                        help="Quiet mode, only prints out information for repos with changes.")

    args = parser.parse_args()

    return args.root_dir, args.quiet


def process_request(root_dir: str, quiet: bool) -> None:
    """
    Processes CLI calls.

    Args:
        root_dir (str): Root directory to look for Git Repos for.
        quiet (bool): If True, will not print on repos that have no changes.
            Will not affect printing on repos that do have changes.
    """
    processed_repos = set()
    for item in os.walk(root_dir):
        # each item is 3-tuple of (dirpath, dirnames, filenames)
        current_path = item[0]
        git_repo = get_git_repo(current_path)

        if git_repo:
            repo = Repo(current_path)
            branch = repo.active_branch
            repo_path = repo.working_tree_dir
            repo_name = repo_path.split("/")[-1]

            if repo_name in processed_repos:
                continue
            else:
                processed_repos.add(repo_name)

            try:
                upstream_commits = list(repo.iter_commits(f"{branch}@{{u}}..{branch}"))
                unpushed_commits = len(upstream_commits) != 0
            except GitCommandError:
                unpushed_commits = False

            if repo.is_dirty() or repo.untracked_files or unpushed_commits:
                print("=======================================================================================")
                print(f"Code changes in {repo_name} located at {repo_path}")
                print(repo.git.status())
            else:
                if quiet:
                    continue
                else:
                    print("=======================================================================================")
                    print(f"No changes in {repo_name} located at {repo_path}")
            print()


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
