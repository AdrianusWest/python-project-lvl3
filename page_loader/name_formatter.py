import os
from urllib.parse import urlparse


def get_file_name(url):
    draft_name, ext = process_url(url)
    return format_file_name(draft_name, ext)


def get_directory_name(page_file_name):
    name, _ = os.path.splitext(page_file_name)
    return name + '_files'


def process_url(url):

    if urlparse(url).path:
        name, ext = os.path.splitext(urlparse(url).netloc + urlparse(url).path)
        return name, ext

    else:
        name = urlparse(url).netloc
        ext = None
        return name, ext


def format_file_name(name, ext):
    if not ext:
        ext = '.html'

    for symbol in name:
        if not symbol.isalnum():
            name = name.replace(symbol, '-')

    if name.endswith('-'):
        name = name[:-1]

    return name + ext
