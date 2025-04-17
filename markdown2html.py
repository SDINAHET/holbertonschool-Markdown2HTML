#!/usr/bin/python3
"""
Script markdown2html - Converts a Markdown file to an HTML file.
Tâche 0 : Vérification des arguments et de l'existence du fichier Markdown.
"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Pour l’instant, le script ne fait rien d’autre.
    sys.exit(0)

