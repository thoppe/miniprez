"""Miniprez. 
Running with a filename starts a watcher that will build the html whenever
the input changes.

Usage:
  miniprez.py <markdown_file>

Options:
  -h --help     Show this screen.
  -v --version  Show the version.
"""
import asyncio
from docopt import docopt
from _version import __version__
from build_loop import parser_loop


def main():
    args = docopt(__doc__, version=__version__)
    f_markdown = args["<markdown_file>"]
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_loop(f_markdown))
    
if __name__ == "__main__":
    main()
