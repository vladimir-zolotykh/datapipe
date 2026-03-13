#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, IO

import os
import fnmatch


def files_iter(top: str, pat: str) -> Iterator[str]:
    for path, dir, names in os.walk(top):
        for fn in fnmatch.filter(names, pat):
            yield os.path.join(path, fn)


# def iter_open(filenames: Iterator[str]) -> Iterator[IO[str | bytes]]:
#     yield f


# def iter_chain():
#     for it in input_iters:
#         yield from it


# def iter_lines(
#     open_files: Iterator[IO[str | bytes]], line_selector: str
# ) -> Iterator[str]:
#     pass


if __name__ == "__main__":
    for f in files_iter("www", "*"):
        print(f)
