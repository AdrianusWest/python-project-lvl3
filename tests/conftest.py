import os

from file_reader import read_file

import pytest


@pytest.fixture()
def content(request):
    filename, = request.param
    return read_file(os.path.join(os.path.dirname(__file__),
                                  'fixtures', filename), 'r')


@pytest.fixture()
def image():
    return read_file(os.path.join(os.path.dirname(__file__),
                                  'fixtures', 'nodejs.png'), 'rb')


@pytest.fixture()
def style():
    return read_file(os.path.join(os.path.dirname(__file__),
                                  'fixtures', 'style.css'), 'rb')


@pytest.fixture()
def script():
    return read_file(os.path.join(os.path.dirname(__file__),
                                  'fixtures', 'script.js'), 'rb')


@pytest.fixture()
def html():
    return read_file(os.path.join(os.path.dirname(__file__),
                                  'fixtures', 'page_without_res.html'), 'r')


@pytest.fixture()
def correct_names():
    return {
        'html': 'ru-hexlet-io-courses.html',
        'img': 'ru-hexlet-io-assets-professions-nodejs.png',
        'css': 'ru-hexlet-io-assets-application.css',
        'js': 'ru-hexlet-io-packs-js-runtime.js',
    }
