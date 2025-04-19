#!/usr/bin/python3
"""
Markdown to HTML - Full converter
"""

import sys
import os
import re
import hashlib


def convert_inline(text):
    """Apply inline Markdown transformations"""
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Emphasis
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    # MD5
    text = re.sub(r'\[\[(.*?)\]\]',
                  lambda m: hashlib.md5(m.group(1).encode()).hexdigest(),
                  text)
    # Remove c/C
    text = re.sub(r'\(\((.*?)\)\)',
                  lambda m: re.sub(r'[cC]', '', m.group(1)),
                  text)
    return text


def write_paragraph(buffer, output):
    """Flush paragraph buffer"""
    if buffer:
        output.write("<p>\n")
        output.write("<br/>\n".join(buffer) + "\n")
        output.write("</p>\n")


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    with open(input_file, 'r') as md, open(output_file, 'w') as html:
        ul_open = False
        ol_open = False
        p_buffer = []

        def close_lists():
            nonlocal ul_open, ol_open
            if ul_open:
                html.write("</ul>\n")
                ul_open = False
            if ol_open:
                html.write("</ol>\n")
                ol_open = False

        for line in md:
            stripped = line.strip()

            if not stripped:
                write_paragraph(p_buffer, html)
                p_buffer = []
                close_lists()
                continue

            # Headings
            heading_match = re.match(r'^(#{1,6}) (.+)', stripped)
            if heading_match:
                write_paragraph(p_buffer, html)
                p_buffer = []
                close_lists()
                level = len(heading_match.group(1))
                content = convert_inline(heading_match.group(2).strip())
                html.write(f"<h{level}>{content}</h{level}>\n")
                continue

            # Unordered list
            if stripped.startswith("- "):
                write_paragraph(p_buffer, html)
                p_buffer = []
                if ol_open:
                    html.write("</ol>\n")
                    ol_open = False
                if not ul_open:
                    html.write("<ul>\n")
                    ul_open = True
                html.write(f"<li>{convert_inline(stripped[2:].strip())}</li>\n")
                continue

            # Ordered list
            if stripped.startswith("* "):
                write_paragraph(p_buffer, html)
                p_buffer = []
                if ul_open:
                    html.write("</ul>\n")
                    ul_open = False
                if not ol_open:
                    html.write("<ol>\n")
                    ol_open = True
                html.write(f"<li>{convert_inline(stripped[2:].strip())}</li>\n")
                continue

            # Paragraph content
            close_lists()
            p_buffer.append(convert_inline(stripped))

        # Final flush
        write_paragraph(p_buffer, html)
        close_lists()

    sys.exit(0)


if __name__ == "__main__":
    main()
