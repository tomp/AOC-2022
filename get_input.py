#!/usr/bin/env python3
"""
Download some day's input from the AOC site.
This requires a session key for a particular user's account.
"""
from pathlib import Path
import argparse

import requests

SESSION_KEY = "session_key.txt"
SITE = "https://adventofcode.com/2022"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "day",
        type=int,
        help="Day number (eg '3')"
    )
    parser.add_argument(
        "--session-key",
        default=SESSION_KEY,
        help="name of text file containing the session key",
    )
    opt = parser.parse_args()
    return opt


def main():
    opt = parse_args()
    url = f"{SITE}/day/{opt.day}/input"
    # print(f"URL: {url}")

    session_key = Path(opt.session_key).read_text().strip()

    s = requests.Session()

    resp = s.get(url, cookies={"session": session_key})
    # print(f"OK: {resp.ok}")

    print(resp.content.decode())


if __name__ == "__main__":
    main()
