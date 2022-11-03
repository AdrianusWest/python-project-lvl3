from file_reader import read_file

import pytest


@pytest.fixture()
def content():
    return read_file('tests/fixtures/file1.html', 'r')


@pytest.fixture()
def image():
    return read_file('tests/fixtures/nodejs.png', 'rb')


@pytest.fixture()
def style():
    return read_file('tests/fixtures/style.css', 'rb')


@pytest.fixture()
def script():
    return read_file('tests/fixtures/script.js', 'rb')


@pytest.fixture()
def html():
    return read_file('tests/fixtures/page_without_res.html', 'r')


@pytest.fixture()
def correct_names():
    return {
        'html': 'ru-hexlet-io-courses.html',
        'img': 'ru-hexlet-io-assets-professions-nodejs.png',
        'css': 'ru-hexlet-io-assets-application.css',
        'js': 'ru-hexlet-io-packs-js-runtime.js',
    }
