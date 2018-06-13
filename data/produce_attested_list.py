import argparse
import regex
import jaconv

from bs4 import BeautifulSoup
from itertools import chain


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path')
    parser.add_argument('input_files', nargs='+')
    args = parser.parse_args()

    raw_files = [''.join(open(f)) for f in args.input_files]
    raw_soup = [BeautifulSoup(f, 'html.parser') for f in raw_files]
    names = [td.text
             for td in
             chain.from_iterable(soup.body.find_all('td') for soup in raw_soup)
             if regex.match('\p{Hiragana}+$', td.text)]
    names = sorted(set(jaconv.hira2kata(n) for n in names))

    with open(args.output_path, mode='w') as output_file:
        output_file.write('\n'.join(names))


if __name__ == '__main__':
    main()
