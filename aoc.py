#!/usr/bin/env python3
"""
A utility module for pulling data from the AdventOfCode site.
"""
import sys
from typing import Optional
from pathlib import Path
from datetime import date
import argparse
import logging

import requests


SESSION_KEY_FILENAME = "session_key.txt"

URL_TMPL = "https://adventofcode.com/{year}/day/{day}{path}"
USER_AGENT = "https://github.com/tomp/AOC-2022 by pollard.tom@gmail.com"

THIS_YEAR = str(date.today().year)
THIS_DAY = str(date.today().day)

BASE_DIR = Path(__file__).parent


logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--year",
        "-y",
        default=THIS_YEAR,
        help="The year of the puzzle",
    )
    parser.add_argument(
        "--day",
        "-d",
        default=THIS_DAY,
        help="The day of the month of the puzzle",
    )
    parser.add_argument(
        "--session-key",
        "-k",
        default=SESSION_KEY_FILENAME,
        help="name of text file containing the session key",
    )


class Client:
    """A Client instance holds state for accessing pages on the adventofcode website.
    It wraps the low-level code for downloading paricular pages from that website,
    on behalf of an authenticated user.
    """

    def __init__(
        self,
        year: Optional[str] = None,
        day: Optional[str] = None,
        session: Optional[str] = None,
    ):
        self.year = year or THIS_YEAR
        self.day = day or THIS_DAY
        self.session_filename = session

        self._headers = {"User-Agent": USER_AGENT}
        self._cookies = {}

        if self.session_filename:
            session_file = str(BASE_DIR / self.session_filename)
            session_key = Path(session_file).read_text().strip()
            self._cookies["session"] = session_key

        self.session = requests.Session()

    def get_page(
        self,
        year: str = "",
        day: str = "",
        path: str = "",
        raw: bool = False
    ):
        if not year:
            year = self.year
        if not day:
            day = self.day
        if path and not path.startswith("/"):
            path = "/" + path
        url = URL_TMPL.format(year=year, day=day, path=path)
        resp = self.session.get(url, headers=self._headers, cookies=self._cookies)
        logger.debug(f"REQ: {resp.request.url}")
        logger.debug(f"OK: {resp.ok}")
        if raw:
            return resp.content.decode()
        return resp.text
