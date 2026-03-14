#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

# $ python sift.py --file-pat=*108* --line-pat=1730 64
# 81.48.212.152 - - [25/Feb/2008:09:46:03 -0600] "GET /ply/PLYTalk.pdf HTTP/1.1" 206 173064
# 81.48.212.152 - - [25/Feb/2008:09:46:03 -0600] "GET /ply/PLYTalk.pdf HTTP/1.1" 206 173064

from typing import Iterator
from typing import TextIO
import os
import fnmatch
import gzip
import bz2
import re
import argparse
import argcomplete

OPEN_IO = TextIO


def files_iter(top: str, pat: str) -> Iterator[str]:
    for path, dir, names in os.walk(top):
        for fn in fnmatch.filter(names, pat):
            yield os.path.join(path, fn)


def open_files_iter(names: Iterator[str]) -> Iterator[OPEN_IO]:
    for fn in names:
        fo: OPEN_IO
        if fn.endswith(".gz"):
            fo = gzip.open(fn, "rt")
        elif fn.endswith(".bz2"):
            fo = bz2.open(fn, "rt")
        else:
            fo = open(fn, "rt")
        yield fo
        fo.close()


def read_lines_iter(open_files: Iterator[OPEN_IO]) -> Iterator[str]:
    for fo in open_files:
        yield from fo


def match_lines_iter(lines: Iterator[str], pat: str) -> Iterator[str]:
    for line in lines:
        if re.search(pat, line):
            yield line


def bytes_count_iter(lines: Iterator[str]) -> Iterator[float]:
    for line in lines:
        yield float(line.rsplit(None, 1)[1])


FILE_PAT = "*108*"
LINE_PAT = "173064"

parser = argparse.ArgumentParser(
    description="Parse FILE_PAT, LINE_PAT",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--file-pat",
    required=False,
    default=FILE_PAT,
    help="Select files that has ARG in names",
)
parser.add_argument(
    "--line-pat",
    required=False,
    default=LINE_PAT,
    help="Select lines that has ARG",
)

if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    files = files_iter("www", args.file_pat)
    file_objects = open_files_iter(files)
    lines = read_lines_iter(file_objects)
    res = match_lines_iter(lines, args.line_pat)
    count = bytes_count_iter(res)
    print(sum(count))
    # for line in res:
    #     print(line, end="")
