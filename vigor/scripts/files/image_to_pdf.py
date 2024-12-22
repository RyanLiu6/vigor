#!/usr/bin/env python3

import os
import re
from typing import List, Union

import click
from PIL import Image


def natural_sort_key(s: str) -> List[Union[int, str]]:
    """
    Return a key for natural sorting that handles numbers within text.
    For example: ['asdf_1.jpg', 'asdf_2.jpg', 'asdf_10.jpg'] will sort correctly.

    This splits on number sequences and converts them to integers while keeping
    the surrounding text intact for comparison.
    """

    def try_int(text: str) -> Union[int, str]:
        try:
            return int(text)
        except ValueError:
            return text.lower()

    # Split on sequences of digits while keeping the digits
    # This will turn "asdf_123.jpg" into ["asdf_", "123", ".jpg"]
    return [try_int(c) for c in re.split(r"(\d+)", s)]


@click.command()
@click.argument("image_dir")
@click.option("--dry-run", is_flag=True, default=False, help="Dry Run")
def image_to_pdf(image_dir: str, dry_run: bool) -> None:
    """
    Gathers all images in `image_dir`, sorted by name, then merges them into
    a singular PDF, output to `image_dir` as well.
    """
    # Step 1: Gather all images inside given directory
    files = os.listdir(image_dir)

    # Use natural sorting instead of regular sorting
    images = sorted(
        [item for item in files if item.lower().endswith((".png", ".jpg", ".jpeg"))],
        key=natural_sort_key,
    )
    image_full_paths = [os.path.join(image_dir, image) for image in images]

    print(f"Images to be merged are: {images}")

    if dry_run or not images:
        return

    # Finally merge and convert to PDF
    data = [Image.open(path).convert("RGB") for path in image_full_paths]
    output_path = os.path.join(image_dir, "output.pdf")

    # Weird PIL way of saving to PDF ...
    data[0].save(output_path, "PDF", save_all=True, append_images=data[1:])

    print(f"Merged PDF saved at: {output_path}")


if __name__ == "__main__":
    image_to_pdf()
