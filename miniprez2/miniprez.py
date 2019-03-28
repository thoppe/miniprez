"""Miniprez

Usage:
  miniprez.py <markdown_file>

Options:
  -h --help     Show this screen.
"""

import asyncio
import os
from docopt import docopt

async def file_watcher(target_file, sleep_time=0.5):
    '''
    Watchs a file. If modified return the time since last modification.
    '''
    
    latest_modification_time = os.path.getmtime(target_file)
    
    while True:
        current_time = os.path.getmtime(target_file)
        if current_time > latest_modification_time:
            delta = current_time - latest_modification_time
            latest_modification_time = current_time
            yield delta

        await asyncio.sleep(sleep_time)
        
async def main():
    async for changes in file_watcher(f_markdown):
        print(changes)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='UNVERSIONED')
    f_markdown = arguments["<markdown_file>"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
