# sitegen
# Copyright (c) 2024 Jovan Lanik

import markdown
import pathlib
import jinja2
from enum import Enum
from bs4 import BeautifulSoup


def FileLoader(file):
    return file.read()


def PathLoader(path, encoding="utf-8", **kwargs):
    with open(path, "r", encoding=encoding, **kwargs) as file:
        return FileLoader(file)


class ContentType(Enum):
    HTML = 0
    Markdown = 1


class Content:
    def process(self, input):
        return input

    def format(self, input):
        soup = BeautifulSoup(input, 'html.parser')
        return soup.prettify(formatter="html5")

    def __init__(self, input, type=ContentType.HTML):
        self.input = input
        if type == ContentType.Markdown:
            self.original_html = markdown.markdown(self.input)
            self.processed_html = self.original_html
        else:
            self.original_html = self.input
            self.processed_html = self.process(self.original_html)
        self.formatted_html = self.format(self.processed_html)
        self.output = self.formatted_html


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
        self.output = self.template.render(content=content.output, **kwargs)
