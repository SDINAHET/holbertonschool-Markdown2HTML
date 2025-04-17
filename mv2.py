#!/usr/bin/python3
"""
markdown2html module
"""
import sys
import os
import hashlib


def convert_md_to_html(input_file, output_file):
    """Convert markdown from input_file to HTML in output_file"""
    try:
        with open(input_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    result = []
    in_ul = False
    in_ol = False
    in_paragraph = False

    for line in lines:
        line = line.rstrip()

        # Skip blank lines
        if not line:
            if in_paragraph:
                result.append("</p>")
                in_paragraph = False
            if in_ul:
                result.append("</ul>")
                in_ul = False
            if in_ol:
                result.append("</ol>")
                in_ol = False
            continue

        # Headings
        if line.startswith('#'):
            count = 0
            while count < len(line) and line[count] == '#':
                count += 1
            if 1 <= count <= 6:
                result.append(f"<h{count}>{line[count:].strip()}</h{count}>")
            continue

        # Unordered list
        if line.startswith("- "):
            if not in_ul:
                result.append("<ul>")
                in_ul = True
            result.append(f"<li>{line[2:].strip()}</li>")
            continue

        # Ordered list
        if line.startswith("* "):
            if not in_ol:
                result.append("<ol>")
                in_ol = True
            result.append(f"<li>{line[2:].strip()}</li>")
            continue

        # Paragraphs
        if not in_paragraph:
            result.append("<p>")
            in_paragraph = True
        else:
            result.append("<br/>")

        # Formatting: bold and emphasis
        text = line
        text = text.replace("**", "<b>", 1).replace("**", "</b>", 1)
        text = text.replace("__", "<em>", 1).replace("__", "</em>", 1)

        # [[MD5]] and ((remove c))
        while '[[' in text and ']]' in text:
            start = text.index('[[')
            end = text.index(']]') + 2
            word = text[start+2:end-2]
            hashed = hashlib.md5(word.encode()).hexdigest()
            text = text[:start] + hashed + text[end:]

        while '((' in text and '))' in text:
            start = text.index('((')
            end = text.index('))') + 2
            word = text[start+2:end-2]
            cleaned = word.replace('c', '').replace('C', '')
            text = text[:start] + cleaned + text[end:]

        result.append(text)

    if in_paragraph:
        result.append("</p>")
    if in_ul:
        result.append("</ul>")
    if in_ol:
        result.append("</ol>")

    with open(output_file, "w") as f:
        f.write('\n'.join(result))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    convert_md_to_html(sys.argv[1], sys.argv[2])
