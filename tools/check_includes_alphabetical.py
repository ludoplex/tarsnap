#!/usr/bin/env python3
""" Checks that #include blocks match the Tarsnap STYLE. """

import sys
import re

import style_utils


def get_included_filename(line):
    """ Extracts blah.h from '#include <blah.h>' or '#include "blah.h"'.

        Args:
            line (string): a line of a .h or .c file."""
    if line.startswith("#include"):
        if included := re.findall('"[^"]*"', line):
            return included[0][1:-1]
        if included := re.findall('<[^>]*>', line):
            return included[0][1:-1]
    return None


def is_block_correct_order(values_orig):
    """ Checks that the list is in (mostly) alphabetical order.

        *Additional note*: in the Tarsnap STYLE for #include blocks, the
        string "sys/types.h" should come first.

        Args:
            values (list): a list of strings."""
    values = list(values_orig)
    # sys/types.h should always be first; we achieve this by removing
    # if it is first in the list
    if values[0] == "sys/types.h":
        values = values[1:]
    return values == sorted(values)


def handle_file(filename):
    """ Parses a .h or .c file and checks that the #include blocks are
        alphabetical.

        Args:
            filename (string): the .h or .c filename to examine."""
    include_block = []
    with open(filename, encoding="utf-8") as filep:
        for i, line in enumerate(filep):
            if included_filename := get_included_filename(line):
                include_block.append(included_filename)
            elif len(include_block) > 0:
                if not is_block_correct_order(include_block):
                    print("Non-alphabetical include block")
                    print("\t%s" % filename)
                    print("\tstarts line %i" % i)
                    print("\t%s" % include_block)
                include_block = []


def main(filenames):
    """ Checks files for #include blocks matching the Tarsnap STYLE.

        Args:
            filenames (list): the filenames (as strings) to check."""
    for filename in filenames:
        # don't apply to libarchive right now
        if style_utils.is_libarchive(filename):
            continue
        handle_file(filename)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Manual usage: specify the filename")
        print("Automatic usage:")
        print("    find . -name \"*.h\" | "
              "xargs tools/check_includes_alphabetical.py")
        print("    find . -name \"*.c\" | "
              "xargs tools/check_includes_alphabetical.py")
        exit(1)
    main(sys.argv[1:])
