#!python

import optparse
import lib.mrrlib as mrr
import os

def main():
    parser = optparse.OptionParser(usage="Usage: %prog [options] [path1] ... [pathN]", description="Mirrors the provided paths. If no path is provided, the current working directory is used.")
    parser.add_option("--init", dest="init", help="Sets variables for the provided paths for future mirrors.", action="store_true", default=False)
    parser.add_option("-d", "--dest", dest="destination", help="Sets the mirror destination to the given directory.", action="store")
    parser.add_option("-i", "--ignore", dest="ignore", help="Adds a path to ignore during the mirror.", action="append", default=[])
    parser.add_option("-I", "--unignore", dest="unignore", help="Removes a path from the list ignored during the mirror. Only works with --init", action="append", default=[])
    (options, args) = parser.parse_args()
    do_mirror = True

    mirror_data = mrr.MrrData()
    if options.destination is not None:
        mirror_data.destination = options.destination
    mirror_data.ignore = options.ignore

    if options.init:
        def initialize(path : str):
            current_data = None
            try:
                current_data = mrr.MrrData.of_path(path, reverse_recursion=False)
            except mrr.MrrError as err:
                current_data = mrr.MrrData()
            current_data.destination = mirror_data.destination or current_data.destination
            current_data.ignore = list(set(mirror_data.ignore + current_data.ignore))
            for unignored in options.unignore:
                current_data.ignore.remove(unignored)
            mrr.write_mirror_data(path, current_data)
        if len(args) > 0:
            for path in args:
                abspath = os.path.abspath(path)
                if not os.path.exists(abspath):
                    print("Path does not exist: {}".format(path))
                else:
                    initialize(os.path.abspath(path))
        else:
            initialize(os.getcwd())
        do_mirror = False
    if do_mirror:
        if len(args) > 0:
            for path in args:
                mrr.mirror_path(os.path.abspath(path), override_mirror_data=mirror_data)
        else:
            mrr.mirror_path(os.getcwd(), override_mirror_data=mirror_data)

if __name__ == "__main__":
    main()
