# File to test datawork.py
import sys
from os.path import join, dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

from pathlib import Path
import logging
import numpy as np

from lbc_immo.datawork import DataLoader, filter_for_period


logging.basicConfig(
    format='%(asctime)s | %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG)


def test_dataloader():
    dl = DataLoader(Path.cwd() / 'data' / 'lobstr_delivery')
    print(dl.data)


def test_filter_for_period():
    for cat, df in DataLoader(Path.cwd() / 'data' / 'lobstr_delivery').data.items():
        for d1, d2 in [(0, 0), (2, 1), (5, 3), (10, 6), (365, 11)]:
            print(d1, d2)
            print(filter_for_period(df, 'last_publication_date', d1, d2).shape)


if __name__ == '__main__':
    test_dataloader()
    #test_filter_for_period()
