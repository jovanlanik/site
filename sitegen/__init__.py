# sitegen
# Copyright (c) 2024 Jovan Lanik

import markdown
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def PathContentLoader(path, encoding="utf-8", **kwargs):
    with open(path, "r", encoding=encoding, **kwargs) as file:
        return FileContentLoader(file)


def FileContentLoader(file):
    return file.read()


def ContentLoader(text):
    return text


class Content:
    pass


class HTMLContent(Content):
    def __init__(self, loader=ContentLoader, *args, **kwargs):
        self.text = loader(*args, **kwargs)
        self.html = self.text


class MarkdownContent(Content):
    def __init__(self, loader=ContentLoader, *args, **kwargs):
        self.text = loader(*args, **kwargs)
        self.html = markdown.markdown(self.text)


class Page:
    def __init__(self, content, template, env=None, **kwargs):
        opt = {
                'loader': FileSystemLoader(searchpath=Path.cwd()),
                'autoescape': select_autoescape()
        }

        if env is None:
            self.env = Environment(**opt)
        else:
            self.env = env.overlay()

        self.template = self.env.get_template(template)
        self.text = self.template.render(content=content.html, **kwargs)
