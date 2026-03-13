#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from typing import Union, TextIO
import os
import fnmatch
import gzip
import bz2

OPEN_IO = Union[gzip.GzipFile, bz2.BZ2File, TextIO]


def files_iter(top: str, pat: str) -> Iterator[str]:
    for path, dir, names in os.walk(top):
        for fn in fnmatch.filter(names, pat):
            yield os.path.join(path, fn)


def open_files_iter(names: Iterator[str]) -> Iterator[OPEN_IO]:
    for fn in names:
        fo: OPEN_IO
        if fn.endswith(".gz"):
            fo = gzip.open(fn, "rb")
        elif fn.endswith(".bz2"):
            fo = bz2.open(fn, "rb")
        else:
            fo = open(fn, "rt")
        yield fo
        fo.close()


def read_lines_iter(open_files: Iterator[OPEN_IO]) -> Iterator[bytes | str]:
    for fo in open_files:
        yield from fo


# def iter_lines(
#     open_files: Iterator[OPEN_IO], line_selector: str
# ) -> Iterator[str]:
#     pass


if __name__ == "__main__":
    # for f in files_iter("www", "*"):
    #     print(f)
    files = files_iter("www", "access-log")
    file_objects = open_files_iter(files)
    lines = read_lines_iter(file_objects)
    for line in lines:
        print(f"{line = }")
