#!/usr/bin/env python3
# site
# Copyright (c) 2024 Jovan Lanik

import json
import shutil
import pathlib
import jinja2
import argparse

import sitegen


def generate(args):
    main_dir = pathlib.Path.cwd()

    static_dir = main_dir.joinpath("static")
    content_dir = main_dir.joinpath("content")
    template_dir = main_dir.joinpath("template")

    main_out = main_dir.joinpath("deploy")


    # copy static files
    shutil.copytree(static_dir, main_out, dirs_exist_ok=True)

    default_template = arg_vars.pop("template")

    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([content_dir, template_dir]),
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
    )

    nav = []
    pages = []
    paths = {}
    dir = content_dir.walk()
    for path, dirs, files in dir:
        for dir in dirs:
            main_out.joinpath(path.relative_to(content_dir) / dir).mkdir(exist_ok=True)

        for file in files:
            input = path / file

            if input.suffix == ".md":
                type = sitegen.ContentType.Markdown
            elif input.suffix == ".html":
                type = sitegen.ContentType.HTML
            elif input.suffix == ".j2" or input.suffix == ".json":
                continue
            else:
                print(f"Unknown file suffix {input.suffix}")
                continue

            content = sitegen.Content(sitegen.PathLoader(input), type)

            output = main_out.joinpath(input.relative_to(content_dir)).with_suffix(".html")
            template = input.with_suffix(".j2")
            vars = input.with_suffix(".json")

            page_vars = {}
            if vars.is_file():
                with open(vars, "r", encoding="utf-8") as file:
                    page_vars = json.loads(file.read())

            if "template" in page_vars:
                template = page_vars.pop("template")
            elif template.is_file():
                template = str(template.relative_to(content_dir))
            else:
                template = default_template

            all_vars = {"hide": False, "priority": 0}
            all_vars.update(arg_vars)
            all_vars.update(page_vars)

            top = False
            parent = input.parent
            if input.stem == "index" and parent != content_dir:
                index = parent.relative_to(content_dir)
                paths[index] = {
                    "href": f"/{index}",
                    "title": all_vars["title"],
                }
                if parent.parent != content_dir:
                    print(f"Found index: {index}")
                else:
                    top = True
                    print(f"Found top-level index: {index}")
                    if all_vars["hide"] is False:
                        nav.append({
                            "href": f"/{index}",
                            "title": all_vars["title"],
                            "priority": all_vars["priority"]
                        })
            else:
                if parent != content_dir:
                    print(f"Found page: {input.name}")
                else:
                    top = True
                    print(f"Found top-level page: {input.name}")
                    if all_vars["hide"] is False:
                        top = input.relative_to(content_dir)
                        nav.append({
                            "href": f"/{top}",
                            "title": all_vars["title"],
                            "priority": all_vars["priority"]
                        })

            page = {}
            page["input"] = input
            page["content"] = content
            page["output"] = output
            page["template"] = template
            page["vars"] = all_vars
            page["top"] = top

            pages.append(page)

    for page in pages:
        page["vars"]["nav"] = nav
        page["vars"]["path"] = []
        if page["top"] is False:
            parents = list(page["input"].relative_to(content_dir).parents)
            parents.reverse()
            parents.pop(0)
            if page["input"].stem == "index":
                parents.pop(-1)
            for parent in parents:
                page["vars"]["path"].append(paths[parent])

        out_name = page["output"].name
        in_name = page["input"].name
        print(f"Generating {out_name} from {in_name}")

        genpage = sitegen.Page(content=page["content"], template=page["template"], env=env, **page["vars"])
        with open(page["output"], "w", encoding="utf-8") as file:
            file.write(genpage.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="generate_site",
            description="Static site generator",
            epilog="Report bugs to <jox969@gmail.com>.",
    )
    parser.add_argument("-j", "--json", default="site.json", required=False)
    parser.add_argument("-J", "--extra-json", required=False)
    args = parser.parse_args()

    arg_vars = {}
    with open(args.json, "r", encoding="utf-8") as file:
        arg_vars.update(json.loads(file.read()))
    if args.extra_json:
        arg_vars.update(json.loads(args.extra_json))

    generate(arg_vars)
