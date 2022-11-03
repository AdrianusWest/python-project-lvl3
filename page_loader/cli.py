import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Downloads page')
    parser.add_argument('page_url', type=str)
    parser.add_argument(
        "-o", "--output",
        help='Set the path to directory',
        default=os.getcwd(),
    )
    return parser.parse_args()
