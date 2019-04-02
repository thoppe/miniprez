import asyncio
import os
from parser import miniprez_markdown, build_body

import logging

logger = logging.getLogger("miniprez")


async def file_watcher(target_file, sleep_time=0.5):
    """
    Watchs a file. If modified, yield the filename. 
    Yield the filename once to start.
    """

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


async def parser_loop(f_markdown, sleep_time=0.5):
    """
    Main event loop. If the target file is modified, or new start a build.
    """
    async for f_target, dt in file_watcher(f_markdown, sleep_time):
        build_html(f_target)


def build_html(f_target):
    """
    Build the html from the markdown.
    """

    f_html_output = f_target.replace(".md", ".html")
    logger.info(f"Building {f_target} to {f_html_output}")

    with open(f_target) as FIN:
        markdown = FIN.read()

    html = miniprez_markdown(markdown)
    soup = build_body(html)

    with open(f_html_output, "w") as FOUT:
        FOUT.write(soup.prettify())
