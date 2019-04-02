"""Miniprez. 

    Running with watch starts will rebuild build the html 
    whenever the input changes.

Usage:
  miniprez.py <markdown_file>
  miniprez.py watch <markdown_file>

Options:
  -h --help     Show this screen.
  -v --version  Show the version.
"""
from _version import __version__
import asyncio
from docopt import docopt
from continuous_integration import parser_loop, build_html
import sys
import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger("miniprez")
fmt = "%(asctime)s %(levelname)s %(message)s"
coloredlogs.install(level="DEBUG", logger=logger, fmt=fmt)


def main():
    args = docopt(__doc__, version=__version__)
    f_markdown = args["<markdown_file>"]

    if args["watch"]:
        sleep_time = 0.5
        logger.debug(f"Rebuilding on changes every {sleep_time:0.2f} seconds")
        loop = asyncio.get_event_loop()
        function = parser_loop(f_markdown)
        loop.run_until_complete(function)
    else:
        build_html(f_markdown)


if __name__ == "__main__":
    main()
