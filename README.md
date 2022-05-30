# Market Comparator
Version 1.0

# WITHOUT virtual env

# After install python in the system:
cd [project_home]
pip install -r requirements.txt

# WITH virtual env

## Create virtual env:
cd [project_home]
pipenv --python 3.8.12

## Delete virtual env (use only for fresh env. installation)
pipenv --rm

## Enter virtual env:
pipenv shell

## Install dependencies:
pipenv install

## Generate requirements.txt from pipfile
pipenv lock -r > requirements.txt

## Datafeeds - Pandas Datareader
https://pandas-datareader.readthedocs.io/en/latest/readers/index.html

# Markets:
## Yahoo
https://finance.yahoo.com/quote/SHY?p=SHY&.tsrc=fin-srch

# RUN
## Using debugger from VSCode
## From command line
python src/main.py -s1 SPY -s2 TLT -f 2018-01-01 -t 2020-12-31
