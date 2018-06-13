# Data Generation Steps

1. Get raw data files

``` shell
mkdir raw
cd raw
bash get_raw_attestation_data.sh
```

2. Normalize

``` shell
mkdir processed
for f in raw/attested_*.html; do python normalize_file.py $f processed/$(basename $f); done
```

3. More processing

``` shell
python produce_attested_list.py processed/attested_myouji.txt processed/attested_*a.html
```

``` shell
python make_table_with_frequency_data.py processed/frequency_count_myouji.tsv processed/attested_*0*.html
```

``` shell
python produce_frequency_list.py processed/myouji_frequency_count.json processed/attested_myouji.txt processed/frequency_count_myouji.tsv
```

4. Make the FST

``` shell
python produce_lexical_data_fst.py processed/myouji_frequency_count.json lexical_data_fst.txt
```
