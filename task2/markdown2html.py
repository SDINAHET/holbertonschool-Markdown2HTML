#!/usr/bin/python3
"""
Markdown to HTML - Tasks 1 & 2: Headings and unordered lists
"""

import sys
import os


def convert_headings(line):
    """Convert heading markdown to HTML"""
    if line.startswith('#'):
        count = 0
        while count < len(line) and line[count] == '#':
            count += 1
        if 1 <= count <= 6 and len(line) > count and line[count] == ' ':
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
        in_ul = False

        for line in md_file:
            stripped = line.strip()

            if not stripped:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                continue

            heading = convert_headings(stripped)
            if heading:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                html_file.write(heading + '\n')
            elif stripped.startswith("- "):
                if not in_ul:
                    html_file.write("<ul>\n")
                    in_ul = True
                html_file.write(f"<li>{stripped[2:].strip()}</li>\n")
            else:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                # Future support for paragraphs or other types
                pass

        if in_ul:
            html_file.write("</ul>\n")

    exit(0)


if __name__ == "__main__":
    main()
