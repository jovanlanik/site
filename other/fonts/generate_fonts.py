#!/usr/bin/env python3
# jovus
# Copyright (c) 2024 Jovan Lanik

import pathlib
import argparse
import fontforge

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="generate_fonts",
            description="Automatic FontForge font generator",
            epilog="Report bugs to <jox969@gmail.com>.",
    )
    parser.add_argument('file', nargs="+")
    args = parser.parse_args()

    for file in args.file:
        output = pathlib.Path(file).with_suffix(".otf")

        font = fontforge.open(file)
        font.generate(str(output))
