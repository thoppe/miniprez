"""Miniprez. 
Running with a filename starts a watcher that will build the html whenever
the input changes.

Usage:
  miniprez.py <markdown_file>

Options:
  -h --help     Show this screen.
"""

import asyncio
import os 
from docopt import docopt
from parser import  miniprez_markdown, build_body

import logging
logger = logging.getLogger('miniprez')

async def file_watcher(target_file, sleep_time=0.5):
    '''
    Watchs a file. If modified, yield the filename. 
    Yield the filename once to start.
    '''
    
    # Yield the file first
    yield target_file, 0

    latest_modification_time = os.path.getmtime(target_file)
    
    while True:
        current_time = os.path.getmtime(target_file)
        if current_time > latest_modification_time:
            delta = current_time - latest_modification_time
            latest_modification_time = current_time
            yield target_file, delta

        await asyncio.sleep(sleep_time)

        
async def parser_loop():
    '''
    Main event loop. If the target file is modified, start a rebuild.
    '''

    async for f_target, dt in file_watcher(f_markdown):

        # If dt is not None, this isn't the first build
        if dt:
            logger.warning(f"{f_target} modified, building")

        # Regardless, start the build
        build_html(f_target)


def build_html(f_target):
    f_html_output = f_target.replace('.md', '.html')
    logger.warning(f"Building {f_target} to {f_html_output}")
    
    with open(f_target) as FIN:
        markdown = FIN.read()
        
    html = miniprez_markdown(markdown)
    soup = build_body(html)

    with open(f_html_output, 'w') as FOUT:
        FOUT.write(soup.prettify())


            
if __name__ == "__main__":
    arguments = docopt(__doc__, version='UNVERSIONED')
    f_markdown = arguments["<markdown_file>"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_loop())
