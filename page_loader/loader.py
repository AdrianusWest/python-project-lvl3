import requests
from page_loader.logger import get_logger

logger = get_logger(__name__)


def load_content(url):
    response = load(url)
    return response.content


def load_text(url):
    response = load(url)
    return response.text


def load(url):
    try:
        logger.info('Trying to connect')
        response = requests.get(url)
        response.raise_for_status()
        logger.info('Successful connection')

    except (requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema) as e:
        logger.error('Wrong address! Check URL-address')
        raise Exception('Wrong address!') from e

    except requests.exceptions.HTTPError as e:
        logger.error('Connection error! Check URL-address')
        raise Exception('Connection error!') from e

    except requests.exceptions.ConnectionError as e:
        logger.error('Connection error! Check URL-address')
        raise Exception('Connection error!') from e

    else:
        return response
