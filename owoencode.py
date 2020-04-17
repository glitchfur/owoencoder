#!/usr/bin/env python3

# owoencode.py, a part of owoencoder
# Made by Glitch, 2020
# https://www.glitchfur.net

from sys import argv, stdout, stderr
from os.path import exists, split
from os import remove

KEEP_ORIG = False
STDOUT_FLAG = False

def main():
    if len(argv) < 2:
        print("The syntax for running this script is as follows:")
        print("python owoencode.py [-kc] <original_file> [ ... ]")
        exit(0)
    in_fns = argv[1:]
    # There is probably a better way to handle parameters. But considering
    # there are only two, I'm not too worried about it right now.
    for param in in_fns:
        if param.startswith("-"):
            global KEEP_ORIG
            global STDOUT_FLAG
            if "k" in param:
                KEEP_ORIG = True
            if "c" in param:
                STDOUT_FLAG = True
                KEEP_ORIG = True # Output going to stdout, keep original file
            in_fns.remove(param)
    for fn in in_fns:
        if not exists(fn):
            print("%s: No such file or directory" % fn, file=stderr)
            exit(1)
        if exists("%s.owo" % fn):
            print("%s: Encoding would cause a naming conflict " \
                "with an existing file, ignoring" % fn)
            in_fns.remove(fn)
    out_fns = ["%s.owo" % fn for fn in in_fns]
    for i in range(len(in_fns)):
        encode(in_fns[i], out_fns[i])

def encode(in_fn, out_fn):
    in_fp = open(in_fn, "rb")
    if STDOUT_FLAG == False:
        out_fp = open(out_fn, "w")
    else:
        out_fp = stdout
    while True:
        in_buffer = in_fp.read(1048576) # read 1MB at a time
        if not in_buffer:
            break
        out_buffer = ''.join([bin(byte)[2:].zfill(8) for byte in in_buffer])
        out_fp.write(out_buffer.replace("1", "OwO").replace("0", "UwU"))
    in_fp.close()
    if STDOUT_FLAG == False:
        out_fp.close()
    if KEEP_ORIG == False:
        remove(in_fn)

if __name__ == "__main__":
    main()
