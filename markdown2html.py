#!/usr/bin/python3
"""Module to convert Markdown to HTML (task 0)"""

import sys
import os


def print_usage():
    """Print usage message and exit with status 1"""
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)


def print_missing(filename):
    """Print missing file message and exit with status 1"""
    sys.stderr.write(f"Missing {filename}\n")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print_missing(input_file)

    # Read from input file and write the same content to output (base case)
    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    with open(output_file, "w") as f_out:
        f_out.writelines(lines)

    sys.exit(0)

