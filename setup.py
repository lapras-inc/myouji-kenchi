from setuptools import find_packages
from setuptools import setup


long_description = open('README.md').read()


setup(name='myouji_kenchi',
      version='1.0.0',
      author='Derick Anderson',
      author_email='anderson.derick.w@gmail.com',
      description='Determine if romanized Japanese names are family names',
      url='https://github.com/scouty-inc/myouji-kenchi',
      long_description=long_description,
      long_description_content_type='text/markdown',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      package_data={'myouji_kenchi': ['data/lexical_data_fst.txt']},
      include_package_data=True,
      install_requires=[
          'numpy',
          'openfst>=1.6.6<1.6.7',
          'regex',
      ],
      classifiers=(
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Natural Language :: Japanese',
          'Topic :: Text Processing :: Linguistic'
      ))
