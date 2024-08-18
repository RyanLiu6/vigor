#!/usr/bin/env python3

import os

import click

from PIL import Image


@click.command()
@click.argument("image_dir")
@click.option("--dry-run", is_flag=True, default=False, help="Dry Run")
def image_to_pdf(image_dir: str, dry_run: bool):
    """
    Gathers all images in `image_dir`, sorted by name, then merges them into
    a singular PDF, output to `image_dir` as well.
    """
    # Step 1: Gather all images inside given directory
    files = os.listdir(image_dir)

    # .endswith((...)) comes from PIL (Pillow) itself - only checks for extensions
    # and not if the image is valid / corrupt / unreadable
    images = sorted([item for item in files if item.lower().endswith((".png", ".jpg", ".jpeg"))])
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
