# About

This library identifies (kenchi) romanized Japanese family names (myouji),
largely in order to split romanized Japanese names into given name and family name.

## Usage

``` python-console
>>> import myouji_kenchi
>>> myouji_kenchi.order_names(['Yamada', 'Satoshi'])
['Satoshi', 'Yamada']
>>> myouji_kenchi.get_score_as_myouji('Yamada')
201046.0
>>> myouji_kenchi.get_score_as_myouji('Satoshi')
329.0
>>> transliterator = myouji_kenchi.MyoujiBackTransliteration()
>>> transliterator.back_transliterate('Yamada')
[('ヤマダ', 201046.0)]
```

## Background

The Japanese ordering of a name is `family name` `given name`, 
whereas the Western ordering is `given name` `family name`.
When a name is written in Japanese script 
one can assume it follows that convention.
However,
when a Japanese name is written in Latin characters
it might be in either order,
depending on the context and the author.
While sometimes a person's name can be treated as atomic,
it is often desirable to know which name is which.

One major complication is the variety of romanization schemes in active use.
Most libraries for back transliterating from Latin characters to Japanese script
presuppose that the romanization scheme for the original transliteration is known.
Often in the sort of situation 
where you do not know the order of a Japanese name
the romanization scheme will also be unknown.
This library targets Kunrei-shiki, Nihon-shiki, and (Modified) Hepburn,
with allowance for the common deviations of 
omitting macrons and apostrophes.

# Installation/Dependencies

1. Install [OpenFst](http://www.openfst.org/).

    It is necessary that 
    the version of OpenFst and the version of the OpenFst Python binding match.
    Note that OpenFst must be compiled with the `--enable-far` option
    in order to support that binding package.  

    ``` shell
    wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.6.tar.gz
    tar xf openfst-1.6.6.tar.gz
    cd openfst-1.6.6
    ./configure --enable-far
    make
    sudo make install 
    ```
  
2. Pip install myouji-kenchi

    ``` shell
    pip install myouji-kenchi
    ```
    
Compiling OpenFst on OS X can be troublesome. 
Making sure you have the latest version of your compiler and 
prefixing `pip install` and/or `make` 
with `CFLAGS="-std=c++11 -stdlib=libc++"` can be helpful.

For Python dependencies see `setup.py` and `requirements_dev.txt`.

# License

MIT License (see LICENSE file)
