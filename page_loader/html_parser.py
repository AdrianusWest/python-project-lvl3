from bs4 import BeautifulSoup
import os

from urllib.parse import urljoin, urlparse, urlunparse
from page_loader.name_formatter import get_file_name
from page_loader.logger import get_logger
from progress.bar import ChargingBar


TAGS_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href'
}


logger = get_logger(__name__)


def parse_html_page(page, files_dir_path, base_url):

    parser = BeautifulSoup(page, 'html.parser')
    resources_paths = parser.find_all(list(TAGS_ATTRIBUTES.keys()))
    resources = prepare_resources(resources_paths,
                                  files_dir_path, base_url)
    html_page = parser.prettify()
    return resources, html_page


def prepare_resources(resources_paths, files_dir_path, base_url):
    logger.info('Start preparing resources')
    progress = ChargingBar('Preparing resources...', max=len(resources_paths))
    resources = []
    parsed_base_url = urlparse(base_url)
    domain = urlunparse(
        (parsed_base_url.scheme, parsed_base_url.netloc, '', '', '', '')
    )
    parsed_domain = urlparse(domain)

    for tag in resources_paths:
        progress.next()
        full_resource_url = ''
        attribute = TAGS_ATTRIBUTES.get(tag.name)
        resource_url = tag.get(attribute)
        parsed_resource_url = urlparse(resource_url)

        if not parsed_resource_url.netloc:
            full_resource_url = urljoin(domain, resource_url)

        if parsed_resource_url.netloc == parsed_domain.netloc:
            url_scheme = parsed_resource_url.scheme if parsed_resource_url.scheme else parsed_domain.scheme  # noqa: E501
            full_resource_url = urlunparse(
                (
                    url_scheme,
                    parsed_resource_url.netloc,
                    parsed_resource_url.path,
                    "",
                    parsed_resource_url.query,
                    parsed_resource_url.fragment
                )
            )

        if not full_resource_url:
            continue

        resource_file_name = get_file_name(full_resource_url)
        new_resource_path = os.path.join(
            os.path.basename(files_dir_path),
            resource_file_name
        )
        tag[attribute] = new_resource_path
        resource_file_path = os.path.join(files_dir_path, resource_file_name)
        resources.append((full_resource_url, resource_file_path))
    progress.finish()
    logger.info('Resource preparation completed')

    return resources
