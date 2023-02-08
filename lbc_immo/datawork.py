from typing import List
from pathlib import Path
import pandas as pd
import numpy as np
import logging
from functools import reduce, cache
from datetime import datetime, timedelta


logging.basicConfig(
    format='%(asctime)s | %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG)


def filter_for_period(df: pd.DataFrame, date_field: str, d1: int, d2: int):
    dt_d1 = (datetime.now() - timedelta(days = d1)).date()
    dt_d2 = (datetime.now() - timedelta(days = d2)).date()
    dates = df.loc[:, date_field].dt.date
    m = (dates >= dt_d1) & (dates <= dt_d2)
    return df.loc[m, :]


class DataLoader:
    def __init__(self, data_dir: Path):
        logging.info(f'Running on directory {data_dir.resolve()}')
        self.data = self._load_data(list(data_dir.resolve().glob('*.csv')))
        for k, df in self.data.items():
            logging.info(f'Found {df.shape[0]} entries for category {k}.')
        self.alldata = pd.concat(self.data.values(), ignore_index=True)

    @staticmethod
    def _load_file(csv_file: Path):
        try:
            # Use python engine to preserve newline characters in text fields
            df = pd.read_csv(csv_file, engine='python')
            assert np.all(df.category_name == df.category_name.iloc[0])
            logging.info(f'Loaded {csv_file}')
        except IndexError:
            logging.error(f'Dropping file {csv_file} because it seems empty.')
            return csv_file, '', pd.DataFrame()
        except AssertionError:
            logging.error(f'Dropping file {csv_file} because category_name changes across the file.')
            return csv_file, '', pd.DataFrame()
        except Exception as e:
            logging.error(f'Could not load file {csv_file} with following exception:\n\t{e}')
            return csv_file, '', pd.DataFrame()

        return csv_file, df.category_name.iloc[0], df

    @staticmethod
    def preprocess_df(df: pd.DataFrame):

        # Change date string to pd.datetime
        for cname in df.columns:
            if 'date' in str(cname).lower() or str(cname).lower() == 'collected_at':
                df.loc[:, cname] = pd.to_datetime(df.loc[:, cname], errors='coerce')

        # Keep most recent publicated version and set annonce_id as index
        return pd.merge(
            left=df,
            right=df.groupby(['annonce_id']).last_publication_date.max().reset_index(),
            on=['annonce_id', 'last_publication_date'],
            how='inner'
        ).drop_duplicates(['annonce_id', 'last_publication_date'])


    def _load_data(self, csv_files: List[Path]):
        logging.info(f'Found {len(csv_files)} files')
        categories = dict()
        for csv_file, category, df in map(self._load_file, csv_files):
            if df.empty: continue
            if category not in categories:
                categories[category] = list()
            categories[category].append(df)

        # We assume that concatenating dataframes from the same category will not create Nan because
        # they should have the same fields (depends on Lobstr scrapping service implementation)
        return {
            cat: self.preprocess_df(pd.concat(dfs, ignore_index=True))
            for cat, dfs in categories.items()
            }
