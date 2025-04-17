#!/usr/bin/python3
"""Markdown to HTML - Task 1: Heading conversion only"""

import sys
import os


def convert_headings(line):
    """Convert heading markdown to HTML"""
    if line.startswith('#'):
        count = 0
        while count < len(line) and line[count] == '#':
            count += 1
        if 1 <= count <= 6 and line[count] == ' ':
            content = line[count:].strip()
            return f"<h{count}>{content}</h{count}>"
    return None


def main():
    """Main entrypoint"""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        exit(1)

    with open(input_file, "r") as md_file, open(output_file, "w") as html_file:
        for line in md_file:
            stripped = line.strip()
            if not stripped:
                continue
            converted = convert_headings(stripped)
            if converted:
                html_file.write(converted + '\n')

    exit(0)


if __name__ == "__main__":
    main()
