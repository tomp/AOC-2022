#!/usr/bin/env python3
"""
A utility module for pulling data from the AdventOfCode site.
"""
import sys
from pathlib import Path
import argparse
import logging

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

import aoc


FMT_HTML = "html"
FMT_TEXT = "text"
FMT_MD = "md"
OUTPUT_FORMATS = (FMT_HTML, FMT_TEXT, FMT_MD)

SUFFIX_FORMAT = {
    ".html": FMT_HTML,
    ".md": FMT_MD,
    ".txt": FMT_TEXT,
}


logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class UsageError(Exception):
    """A UsageError is raised when there's an issue parsing the command-line options."""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Write the day's problem description to a text file."
    )
    parser.add_argument(
        "--outfile",
        help="The file to which to write the output.",
    )
    parser.add_argument(
        "--format",
        help="The output file format (html, md, or text)",
    )
    parser.add_argument(
        "--input",
        action="store_true",
        help="Download the day's input file",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Produce debug output",
    )
    aoc.add_arguments(parser)

    opt = parser.parse_args()

    if opt.input and opt.format:
        logger.warning("--format is ignored when writing input data")
        opt.format = FMT_MD

    if opt.outfile:
        if opt.format:
            logger.warning("--format is ignored when an output file is specified")
        suffix = Path(opt.outfile).suffix.lower()
        opt.format = SUFFIX_FORMAT[suffix]

    if not opt.format:
        opt.format = FMT_MD
    if opt.format not in OUTPUT_FORMATS:
        raise UsageError(f"Unrecognized format '{opt.format}'")

    return opt


def main() -> int:
    opt = parse_args()
    if opt.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("[debug mode]")

    aoc_client = aoc.Client(year=opt.year, day=opt.day, session=opt.session_key)

    if opt.input:
        input_text = aoc_client.get_page(year=opt.year, day=opt.day, path="input", raw=True)
        if opt.outfile:
            with Path(opt.outfile).open("w") as fp:
                fp.write(input_text)
                logger.info(f"Wrote {opt.outfile}")
        else:
            print(input_text)
        return 0

    page_html = aoc_client.get_page(year=opt.year, day=opt.day)

    if opt.format == FMT_HTML:
        output_text = page_html
    elif opt.format in (FMT_TEXT, FMT_MD):
        soup = BeautifulSoup(page_html, "html.parser")
        output_text = markdownify(str(soup.body.main))

    if opt.outfile:
        with Path(opt.outfile).open("w") as fp:
            fp.write(output_text)
            logger.info(f"Wrote {opt.outfile}")
            return 0

    print(output_text)
    return 0


if __name__ == "__main__":
    main()
