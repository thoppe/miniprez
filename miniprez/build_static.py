import os
from importlib import resources
import logging

logger = logging.getLogger("miniprez")


def include_resource(filename):

    if not os.path.exists(filename):
        logger.warning(f"Copying {filename}")

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
