import os
import shutil
import filecmp

from os.path import realpath, join, dirname, basename

__location__ = realpath(join(os.getcwd(), dirname(__file__)))

static_path = join(dirname(__location__), "miniprez", "static")
dest_path = os.getcwd()


def build_environment(**args):

    verbose = args["--verbose"]
    has_touched = False

    for root, dirs, files in os.walk(static_path):

        # Create any missing directories
        rel_dir = root.split('miniprez/')[-1]

        if not os.path.exists(rel_dir):
            if verbose:
                print("Creating directory {}".format(rel_dir))
            os.makedirs(rel_dir)
            has_touched = True

        for f in files:
            f_src = join(root, f)
            f_dest = os.path.join(rel_dir, basename(f_src))

            if not os.path.exists(f_dest) or not filecmp.cmp(f_src, f_dest):
                shutil.copyfile(f_src, f_dest)
                if verbose:
                    print("Refreshing file {}".format(f_dest))
                has_touched = True

    return has_touched
