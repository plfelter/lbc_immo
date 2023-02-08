# File to test datawork.py
import sys
from os.path import join, dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

from pathlib import Path

from lbc_immo.datawork import DataLoader, filter_for_period


def test_dataloader():
    print(DataLoader(Path.cwd() / 'data' / 'lobstr_delivery').data)


def test_datawork():
    for cat, df in DataLoader(Path.cwd() / 'data' / 'lobstr_delivery').data.items():
        DataParser(df)

def test_filter_for_period():
    for cat, df in DataLoader(Path.cwd() / 'data' / 'lobstr_delivery').data.items():
        for d1, d2 in [(0, 0), (2, 1), (5, 3), (10, 6), (365, 11)]:
            print(d1, d2)
            print(filter_for_period(df, 'last_publication_date', d1, d2).shape)


if __name__ == '__main__':
    #test_dataloader()
    #test_datawork()
    test_filter_for_period()
