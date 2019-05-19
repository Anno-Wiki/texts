"""This file is going to be concerned with quickly processing certain textual
idiosyncracies into a format acceptable to the icc processor/pre-processor.

Hell, this could probably replace preprocessor.py for most things except
annotations.
A list of things this file needs to perform:

1. Convert '--' to '—' automatically.
2. Convert n number of spaces into m number of hashes (#) for the indentation
   processor.
3. Surround lines preceded by n number of spaces with brackets for the purpose
   of stage directions.
4. I might eventually convert `'` to `‘` and `’`. This is still done with my
   preprocessor right now (as is the em dash) but it seems so fragile I might
   find it preferential to do it here.

"""
import sys
import io
import argparse
import re

# Constants for re.sub
EMDASH = (re.compile('--'), '—')


def loop(FIN, FOUT, patterns):
    """The main loop of the program."""
    for line in FIN:
        for pattern in patterns:
            line = re.sub(*pattern, line)
        FOUT.write(line)


def get_hash_patterns(hashes):
    hashes = [hash.split('=') for hash in hashes]
    hashes = sorted(hashes, key=lambda hash: hash[0], reverse=True)
    _hashes = []
    for h in hashes:
        pattern = re.compile(r'^ {' + str(h[0]) + r'}(?! )')
        replace = '#' * int(h[1])
        _hashes.append((pattern, replace))
    return _hashes


def main(FIN, FOUT, args):
    patterns = [EMDASH]
    if args.hash:
        patterns.extend(get_hash_patterns(args.hash.split(',')))
    if args.bracket:
        pattern = re.compile('^ {' + args.bracket + '}(?! )([^[]*)\n')
        replace = r'[\1]\n'
        patterns.append((pattern, replace))
    print(patterns)
    loop(FIN, FOUT, patterns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("A handful of tools to format a text for "
                                     "the ICC")
    parser.add_argument('-i', '--input', action='store', type=str,
                        help="The input file. Defaults to stdin.")
    parser.add_argument('-o', '--output', action='store', type=str,
                        help="The output file. Defaults to stdout.")
    parser.add_argument('--hash', action='store', type=str,
                        help="A comma-separated list of n number of spaces to "
                        "convert to m number of hashes, e.g. '3=2,5=4'")
    parser.add_argument('-b', '--bracket', action='store', type=str,
                        help="The number of spaces to match at the beginning "
                        "of a line to surround it with brackets for a stage "
                        "direction.")

    args = parser.parse_args()

    FIN = io.open(args.input, 'r', encoding='utf-8-sig') if args.input\
        else open(args.input, 'rt', encoding='utf-8-sig')
    FOUT = sys.stdout if not args.output else open(args.output, 'wt')

    main(FIN, FOUT, args)
