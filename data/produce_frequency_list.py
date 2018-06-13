import pandas as pd

import argparse
import regex
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path')
    parser.add_argument('attested_names_path')
    parser.add_argument('frequency_count_path')
    args = parser.parse_args()

    attested_names = list(l.strip() for l in open(args.attested_names_path))
    top_ten_thousand = pd.read_csv(args.frequency_count_path, sep='\t')

    furigana_columns = [c for c in top_ten_thousand.columns if 'フリガナ' in c]

    frequency_scores = {}
    for rank, group in top_ten_thousand.groupby('新順位'):
        readings = group[furigana_columns].values
        readings = readings[~pd.isnull(readings)]
        readings = set(regex.sub(r'[★☆]', '', r) for r in readings)
        readings = set(r for r in readings if regex.match(r'\p{Katakana}+$', r))
        frequency = int(group['世帯数'].iloc[0])
        for r in readings:
            frequency_scores[r] = frequency_scores.get(r, 0) + frequency

    for name in attested_names:
        frequency_scores[name] = frequency_scores.get(name, 1)

    json.dump(frequency_scores, open(args.output_path, mode='w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
