#!/usr/bin/python3
"""
Markdown to HTML - Tasks 1 to 5: Headings, lists, paragraphs, bold, emphasis
"""

import sys
import os
import re


def convert_headings(line):
    """Convert heading markdown to HTML"""
    if line.startswith('#'):
        count = 0
        while count < len(line) and line[count] == '#':
            count += 1
        if 1 <= count <= 6 and len(line) > count and line[count] == ' ':
            content = line[count:].strip()
            return f"<h{count}>{apply_inline_formatting(content)}</h{count}>"
    return None


def apply_inline_formatting(text):
    """
    Replaces Markdown-style inline formatting with corresponding HTML:
    **bold** -> <b>bold</b>
    __italic__ -> <em>italic</em>
    """
    # Bold first to avoid conflict with __
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


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
        in_ol = False
        paragraph_buffer = []

        def flush_paragraph():
            """Flush the paragraph buffer if not empty"""
            nonlocal paragraph_buffer
            if paragraph_buffer:
                html_file.write("<p>\n")
                html_file.write("<br/>\n".join(paragraph_buffer) + "\n")
                html_file.write("</p>\n")
                paragraph_buffer = []

        for line in md_file:
            stripped = line.strip()

            # New block (empty line)
            if not stripped:
                flush_paragraph()
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                continue

            heading = convert_headings(stripped)
            if heading:
                flush_paragraph()
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                html_file.write(heading + '\n')
            elif stripped.startswith("- "):
                flush_paragraph()
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                if not in_ul:
                    html_file.write("<ul>\n")
                    in_ul = True
                content = apply_inline_formatting(stripped[2:].strip())
                html_file.write(f"<li>{content}</li>\n")
            elif stripped.startswith("* "):
                flush_paragraph()
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if not in_ol:
                    html_file.write("<ol>\n")
                    in_ol = True
                content = apply_inline_formatting(stripped[2:].strip())
                html_file.write(f"<li>{content}</li>\n")
            else:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                paragraph_buffer.append(apply_inline_formatting(stripped))

        flush_paragraph()
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")

    exit(0)


if __name__ == "__main__":
    main()
