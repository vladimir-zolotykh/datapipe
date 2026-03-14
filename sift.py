#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from typing import Union, TextIO
import os
import fnmatch
import gzip
import bz2
import re

# OPEN_IO = Union[gzip.GzipFile, bz2.BZ2File, TextIO]
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


if __name__ == "__main__":
    files = files_iter("www", "access-log")
    file_objects = open_files_iter(files)
    lines = read_lines_iter(file_objects)
    res = match_lines_iter(lines, ".*ply.*")
    for line in res:
        print(f"{line = }")
