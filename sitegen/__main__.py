# sitegen
# Copyright (c) 2024 Jovan Lanik

# Example cmdline interface to sitegen

import sitegen
import argparse
import json
import pathlib

parser = argparse.ArgumentParser(
        prog="sitegen",
        description="Static site generator",
        epilog="Report bugs to <jox969@gmail.com>.",
)
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-t", "--template", required=True)
parser.add_argument("-j", "--json", required=True)
args = parser.parse_args()

with open(args.json, "r", encoding="utf-8") as file:
    vars = json.loads(file.read())

if pathlib.Path(args.input).suffix == ".md":
    type = sitegen.ContentType.Markdown
else:
    type = sitegen.ContentType.HTML

input = sitegen.PathLoader(args.input)
content = sitegen.Content(input, type)
page = sitegen.Page(content, args.template, **vars)
with open(args.output, "w", encoding="utf-8") as output:
    output.write(page.output)
