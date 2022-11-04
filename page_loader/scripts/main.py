import sys

from page_loader.cli import parse_args
from page_loader.download import download
from page_loader.logger import get_logger


logger = get_logger(__name__)


def main():
    args = parse_args()
    try:
        path = download(args.page_url, args.output)
    except Exception as e:
        logger.info(e)
        logger.error('Page was not downloaded, see log file')
        sys.exit(1)
    else:
        print(f"Page successfully downloaded into {path}")


if __name__ == '__main__':
    main()
