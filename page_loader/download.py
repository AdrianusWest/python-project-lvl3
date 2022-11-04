import os

from page_loader.file_saver import (create_directory,
                                    save_data_as_file,
                                    save_text_as_file)
from page_loader.html_parser import parse_html_page
from page_loader.loader import load_content, load_text
from page_loader.logger import get_logger
from page_loader.name_formatter import get_directory_name, get_file_name

from progress.bar import ChargingBar


logger = get_logger(__name__)


def download(base_url, output_path):
    if not os.path.exists(output_path):
        logger.error('Output directory %s does not exist!', output_path)
        raise IOError('Output directory does not exist!')
    logger.info('Start page download from %s', base_url)
    page_file_name = get_file_name(base_url)
    page_output_path = os.path.join(output_path, page_file_name)
    file_dir_name = get_directory_name(page_file_name)
    files_dir_path = os.path.join(output_path, file_dir_name)
    page = load_text(base_url)
    resources, html_page = parse_html_page(page, files_dir_path, base_url)

    if resources:
        create_directory(files_dir_path)
        download_resources(resources)

    save_text_as_file(html_page, page_output_path)
    logger.info("Page and resources from %s has been loaded", base_url)
    return page_output_path


def download_resources(resources):
    with ChargingBar('Downloading resources...',
                     max=len(resources)) as progress:
        for resource_url, resource_path in resources:
            progress.next()
            resource = load_content(resource_url)
            save_data_as_file(resource, resource_path)
