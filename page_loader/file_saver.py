import os

from page_loader.logger import get_logger

logger = get_logger(__name__)


def save_data_as_file(data, path):
    logger.info("Start downloading resource into %s", path)

    with open(path, 'wb') as file:
        file.write(data)

    logger.info("Resource download completed")
    return


def save_text_as_file(data, path):
    with open(path, 'w') as file:
        file.write(data)


def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info('Directory has been created')
