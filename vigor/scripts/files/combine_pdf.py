#!/usr/bin/env python3

import os
import click

from pypdf import PdfWriter


@click.command()
@click.argument("pdf_dir")
@click.option("--dry-run", is_flag=True, default=False, help="Dry Run")
def combine_pdf(pdf_dir: str, dry_run: bool):
    """
    Gathers all pdfs in `pdf_dir`, sorted by name, then merges them into
    a singular PDF, output to `pdf_dir` as well.
    """
    # Step 1: Gather all pdfs inside given directory
    files = os.listdir(pdf_dir)
    pdfs = sorted([item for item in files if item.lower().endswith(".pdf")])

    print(f"PDFs to be merged are: {pdfs}")

    if dry_run or not pdfs:
        return

    # Finally merge
    output_path = os.path.join(pdf_dir, "combined.pdf")
    merger = PdfWriter()
    for pdf in pdfs:
        merger.append(os.path.join(pdf_dir, pdf))

    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved at: {output_path}")


if __name__ == "__main__":
    combine_pdf()
