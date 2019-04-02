import os
from importlib import resources
import logging

logger = logging.getLogger("miniprez")


def include_resource(filename):

    if not os.path.exists(filename):
        logger.info(f"--> {filename}")

        # Create the directory if we need to
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        module_path = ".".join(os.path.split(directory))
        basename = os.path.basename(filename)

        # Read the file into the location
        res = resources.open_binary(module_path, basename)
        with res as FIN, open(filename, "wb") as FOUT:
            FOUT.write(res.read())


def add_script(soup, src, cdn=False, *args, **kwargs):
    """
    Takes a bs4 soup and adds the following script to the end of the body.
    """

    if not cdn:
        include_resource(src)

    tag = soup.new_tag("script", src=src)
    for key, val in kwargs.items():
        tag[key] = val

    soup.body.append(tag)


def add_css(soup, src, cdn=False, *args, **kwargs):
    """
    Takes a bs4 soup and adds the following css to the header
    """

    if not cdn:
        include_resource(src)

    css_args = {"rel": "stylesheet", "type": "text/css", "media": "all"}
    tag = soup.new_tag("link", href=src, **css_args)

    for key, val in kwargs.items():
        tag[key] = val

    soup.head.append(tag)
