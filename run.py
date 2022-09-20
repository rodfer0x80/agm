#!/usr/bin/python3

import os
import sys

def main():
    if len(sys.argv) != 2:
        return 1
    cdir = "."
    #dirs = __file__.split("/")[1:-1]
    #cdir = ""
    #for d in dirs:
    #    cdir = f"{cdir}/{d}"
    cmd = f"source {cdir}/venv/bin/activate && python {cdir}/{sys.argv[1]}"
    os.system(cmd)
    return 0

if __name__ == '__main__':
    sys.exit(main())
