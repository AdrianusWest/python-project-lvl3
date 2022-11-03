import os
import tempfile

from file_reader import read_file

from page_loader.download import download
from page_loader.name_formatter import get_file_name

import pytest

import requests_mock


FILES_COUNT = 4
SITE_PATH = '/courses'
BASE_URL = 'https://ru.hexlet.io'
PAGE_FILES_DIR = 'ru-hexlet-io-courses_files'


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


def test_download_page_with_res(content, correct_names, image, style, script):

    with requests_mock.Mocker() as mock:
        mock.get(BASE_URL + SITE_PATH, text=content)
        mock.get(BASE_URL + '/assets/professions/nodejs.png', content=image)
        mock.get(BASE_URL + '/assets/application.css', content=style)
        mock.get(BASE_URL + '/packs/js/runtime.js', content=script)

        with tempfile.TemporaryDirectory() as temp:

            correct_html = read_file('tests/fixtures/html_result.html', 'r')
            correct_path = os.path.join(temp, correct_names.get('html'))
            result_path = download(BASE_URL + SITE_PATH, temp)
            assert read_file(result_path, 'r') == correct_html
            assert result_path == correct_path
            image_path = os.path.join(temp, PAGE_FILES_DIR,
                                      correct_names.get('img'))
            image_name = get_file_name(
                BASE_URL + '/assets/professions/nodejs.png')
            assert image_name == correct_names.get('img')
            assert read_file(image_path, 'rb') == image

            css_path = os.path.join(temp, PAGE_FILES_DIR,
                                    correct_names.get('css'))
            css_name = get_file_name(BASE_URL + '/assets/application.css')
            assert read_file(css_path, 'rb') == style
            assert css_name == correct_names.get('css')
            js_path = os.path.join(temp, PAGE_FILES_DIR,
                                   correct_names.get('js'))
            js_name = get_file_name('https://ru.hexlet.io/packs/js/runtime.js')
            assert read_file(js_path, 'rb')
            assert js_name == correct_names.get('js')
            page_name, _ = os.path.splitext(get_file_name(
                BASE_URL + SITE_PATH),
            )
            files_count = len(os.listdir(os.path.join(temp,
                                                      page_name + '_files')))
            assert files_count == FILES_COUNT


def test_download_page_without_res(correct_names, html):
    with requests_mock.Mocker() as mock:
        mock.get(BASE_URL + SITE_PATH, text=html)
        with tempfile.TemporaryDirectory() as temp:
            page_path = download(BASE_URL + SITE_PATH, temp)
            correct_path = os.path.join(temp, correct_names.get('html'))
            assert read_file(page_path, 'r') == html
            assert page_path == correct_path


@pytest.mark.parametrize('url, exception', [
    ('ru.hexlet.io', 'WRONG ADDRESS!'),
    ('sptth://ru.hexlet.io', 'WRONG ADDRESS!'),
    ('https://site.com/404', 'CONNECTION ERROR!'),
])
def test_download_with_errors(url, exception):
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(Exception):
            download(url, temp)


@pytest.mark.parametrize('url, output_path', [
    ('https://ru.hexlet.io', ''),
    ('https://ru.hexlet.io', '$%^@*&////'),
])
def test_storage_errors(url, output_path):
    with pytest.raises(IOError):
        download(url, output_path)
