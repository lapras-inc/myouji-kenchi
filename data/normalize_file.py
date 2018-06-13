import argparse
import unicodedata

parser = argparse.ArgumentParser()
parser.add_argument('infile')
parser.add_argument('outfile')
args = parser.parse_args()

s = ''.join(open(args.infile))
s = unicodedata.normalize('NFKC', s)
open(args.outfile, mode='w').write(s)
