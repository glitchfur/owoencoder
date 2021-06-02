#!/usr/bin/env python3

# owoencode.py, a part of owoencoder
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
                        help="Keep the input file. Do not delete it after doing encoding")
    parser.add_argument('-c', dest="to_stdout", action='store_true',
                        help="Encode to stdout instead of a file. This implies -k. This also makes piping output possible")

    args = parser.parse_args()

    to_stdout = args.to_stdout
    keep_original = args.keep_original or to_stdout
    in_fns = args.encoded_file

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
        encode(in_fns[i], out_fns[i], to_stdout, keep_original)

def encode(in_fn, out_fn, to_stdout=False, keep_original=False):
    in_fp = open(in_fn, "rb")
    if to_stdout == False:
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
    if to_stdout == False:
        out_fp.close()
    if keep_original == False:
        remove(in_fn)

if __name__ == "__main__":
    main()
