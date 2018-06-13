import pandas as pd

import argparse
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path')
    parser.add_argument('input_files', nargs='+')
    args = parser.parse_args()

    raw_files = [''.join(open(f)) for f in args.input_files]
    raw_soups = [BeautifulSoup(f, 'html.parser') for f in raw_files]
    dataframes = [convert_to_dataframe(soup) for soup in raw_soups]
    df = pd.concat(dataframes)
    df.to_csv(args.output_path, index=None, sep='\t')


def convert_to_dataframe(soup):
    trs = soup.find_all('body')[-1].find_all('tr')
    columns = [t.text for t in trs[0].find_all('td')]
    text_values = [[t.text for t in tr.find_all('td')] for tr in trs[1].find_all('tr')]
    return pd.DataFrame.from_records(text_values, columns=columns)


if __name__ == '__main__':
    main()
