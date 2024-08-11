# sitegen
# Copyright (c) 2024 Jovan Lanik

import markdown
import pathlib
import jinja2


def PathContentLoader(path, encoding="utf-8", **kwargs):
    with open(path, "r", encoding=encoding, **kwargs) as file:
        return FileContentLoader(file)


def FileContentLoader(file):
    return file.read()


def ContentLoader(text):
    return text


class HTMLContent:
    def __init__(self, loader=ContentLoader, *args, **kwargs):
        self.text = loader(*args, **kwargs)
        self.html = self.text


class MarkdownContent:
    def __init__(self, loader=ContentLoader, *args, **kwargs):
        self.text = loader(*args, **kwargs)
        self.html = markdown.markdown(self.text)


class Page:
    def __init__(self, content, template, env=None, **kwargs):
        if env is None:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(searchpath=pathlib.Path.cwd()),
                autoescape=jinja2.select_autoescape(),
            )
        else:
            self.env = env.overlay()

        self.template = self.env.get_template(template)
        self.text = self.template.render(content=content.html, **kwargs)
