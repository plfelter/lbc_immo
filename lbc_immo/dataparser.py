from typing import List
from pathlib import Path
import pandas as pd
import logging


class DataParser:
    pass

class DataLoader:
    def __init__(self, data_dir: Path):
        self.df = self._load_data(data_dir.resolve().glob('*.csv'))

    @staticmethod
    def _load_file(csv_file: Path):
        df = pd.DataFrame()
        try:
            # Use python engine to preserve newline characters in text fields
            df = pd.read_csv(csv_file, engine='python').set_index('annonce_id', drop=False)
            logging.info(f'Loaded {csv_file}')
        except Exception:
            logging.warn(f'Could not load file {csv_file}')
        return df

    @staticmethod
    def _load_data(csv_files: List[Path]):
        # TODO: first sort dataframes that have the same column names
        return pd.concat(list(map(self._load_file, csv_files))
