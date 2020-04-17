#!/usr/bin/env python3

# owodecode.py, a part of owoencoder
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
        print("python owodecode.py [-kc] <encoded_file> [ ... ]")
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
        if not fn.lower().endswith(".owo"):
            print("%s: File doesn't end with a .owo extension, " \
                "ignoring" % fn, file=stderr)
            in_fns.remove(fn)
        if exists(fn[:-4]):
            print("%s: Decoding would cause a naming conflict " \
                "with an existing file, ignoring" % fn)
            in_fns.remove(fn)
    out_fns = [fn[:-4] for fn in in_fns]
    for i in range(len(in_fns)):
        decode(in_fns[i], out_fns[i])

def decode(in_fn, out_fn):
    in_fp = open(in_fn, "r")
    if STDOUT_FLAG == False:
        out_fp = open(out_fn, "wb")
    else:
        out_fp = stdout.buffer
    while True:
        # read (almost) 1MB at a time, to the nearest multiple of 24
        in_buffer = in_fp.read(1048560)
        if not in_buffer:
            break
        out_buffer = in_buffer.replace("OwO", "1").replace("UwU", "0")
        try:
            out_fp.write(b''.join(
                [int(out_buffer, 2).to_bytes(len(out_buffer) // 8, "big")]
            ))
        except ValueError:
            print("%s: An error occurred processing this file, potentially " \
                "it is not an encoded file. Aborting." % in_fn)
            exit(1)
    in_fp.close()
    if STDOUT_FLAG == False:
        out_fp.close()
    if KEEP_ORIG == False:
        remove(in_fn)

if __name__ == "__main__":
    main()
