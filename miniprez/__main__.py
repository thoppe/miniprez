#! /usr/bin/env python
"""
Usage:
    miniprez.py INPUT [-o OUTPUT|-t] [--condense] [--nocopy] [--verbose] [--watch=<kn>]
    miniprez.py --version

-h --help     Show this help
-o, --output  FILE specify output file [default: INPUT.html]
-t, --term    Output just the slides to stdout
--watch=<kn>  Continuously rebuild on changes to input every n seconds [default: once]
--condense    Don't pretty-print the output [default: False]
--nocopy      Don't copy the static files: css, js, etc [default: False]
--verbose     Print more text [default: False]
--version     Output the current version number and exit
"""

import os
import time
from docopt import docopt
import miniprez


def main():
    args = docopt(__doc__)
    f_md = args["INPUT"]

    if args["--version"]:
        print(miniprez.__version__)
        exit()

    if not os.path.exists(f_md):
        raise IOError("{} not found".format(f_md))

    if args["OUTPUT"] is None:
        f_base = os.path.basename(f_md)
        args["OUTPUT"] = '.'.join(f_base.split('.')[:-1]) + '.html'

    if args["--watch"] == 'once':
        miniprez.build(args)
        exit()

    while True:
        miniprez.build(args)
        time.sleep(float(args["--watch"]))


if __name__ == "__main__":
    main()
