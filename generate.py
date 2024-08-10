#!/usr/bin/env python3
# site
# Copyright (c) 2024 Jovan Lanik

import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

import sitegen

if __name__ == "__main__":
    main_dir = Path.cwd()

    static_dir = main_dir.joinpath("static")
    content_dir = main_dir.joinpath("content")
    template_dir = main_dir.joinpath("template")

    main_out = main_dir.joinpath("deploy")

    # copy static files
    shutil.copytree(static_dir, main_out, dirs_exist_ok=True)

    with open(main_dir.joinpath("site.json"), "r", encoding="utf-8") as file:
        site_vars = json.loads(file.read())

    default_template = site_vars.pop("template")

    env = Environment(loader=FileSystemLoader([content_dir, template_dir]), autoescape=select_autoescape())

    # TODO: top-level pages nav
    pages = content_dir.walk()
    for path, dirs, files in pages:
        for dir in dirs:
            main_out.joinpath(dir).mkdir(exist_ok=True)

        for file in files:
            input = path / file

            if input.suffix == ".md":
                content = sitegen.MarkdownContent(sitegen.PathContentLoader, input)
            elif input.suffix == ".html":
                content = sitegen.HTMLContent(sitegen.PathContentLoader, input)
            elif input.suffix == ".j2" or input.suffix == ".json":
                continue
            else:
                print(f"Unknown file suffix {input.suffix}")
                continue

            output = main_out.joinpath(input.relative_to(content_dir)).with_suffix(".html")
            template = input.with_suffix(".j2")
            vars = input.with_suffix(".json")

            print(f"Generating {output.name}")

            page_vars = {}
            if vars.is_file():
                with open(vars, "r", encoding="utf-8") as file:
                    page_vars = json.loads(file.read())

            if "template" in page_vars:
                template = page_vars.pop("template")
            elif template.is_file():
                template = template.relative_to(content_dir)
            else:
                template = default_template

            all_vars = {}
            all_vars.update(site_vars)
            all_vars.update(page_vars)

            page = sitegen.Page(content=content, template=str(template), env=env, **all_vars)
            with open(output, "w", encoding="utf-8") as file:
                file.write(page.text)
