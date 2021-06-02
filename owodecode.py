#!/usr/bin/env python3

# owodecode.py, a part of owoencoder
# Made by Glitch, 2020
# https://www.glitchfur.net

from sys import stdout, stderr
from os.path import exists
from os import remove

import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("encoded_file", metavar="<encoded_file>", type=str, nargs="+")
    parser.add_argument('-k', dest="keep_original", action='store_true',
                        help="Keep the input file. Do not delete it after doing encoding or decoding")
    parser.add_argument('-c', dest="to_stdout", action='store_true',
                        help="Encode or decode to stdout instead of a file. This implies -k. This also makes piping output possible")

    args = parser.parse_args()

    to_stdout = args.to_stdout
    keep_original = args.keep_original or to_stdout
    in_fns = args.encoded_file

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
        decode(in_fns[i], out_fns[i], to_stdout, keep_original)

def decode(in_fn, out_fn, to_stdout=False, keep_original=False):
    in_fp = open(in_fn, "r")
    if to_stdout == False:
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
    if to_stdout == False:
        out_fp.close()
    if keep_original == False:
        remove(in_fn)

if __name__ == "__main__":
    main()
