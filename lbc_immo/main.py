import time
from pathlib import Path
import pandas as pd
import logging
from unidecode import unidecode
from itertools import repeat
import json

from lbc_immo.datawork import DataLoader, filter_for_period
from featurewriters import FeatureWriter, ImmoFeatureWriter


log_file = Path('/home/debian/lbc_immo/lbc_immo.log')
data_dir = Path('/home/debian/lbc_immo/data/lobstr_delivery/')
http_server_data_dir = Path('/var/www/lbc-immo/')


logging.basicConfig(
    format='%(asctime)s | %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
        ]
    )


if __name__ == '__main__':
    baseWriter = {
        'Ventes immobilières': ImmoFeatureWriter
    }
    for cat, df in DataLoader(data_dir).data.items():
        for d1, d2 in [(0, 0), (1, 1), (2, 2), (5, 3), (10, 6), (365, 11)]:
            filtered_df = filter_for_period(df, 'last_publication_date', d1, d2)
            Jstr = f'J{d1}' if d1 == d2 else f'J{d1}_J{d2}'
            geojson_fn = http_server_data_dir / f"{unidecode(cat).replace(' ', '_')}_{Jstr}.json"
            logging.info(
                f'Writing {filtered_df.shape[0]} features for {Jstr} ("{cat}" category) to file'
                f'"{cat}" category)')

            features_list = list(map(
                getattr,
                filter(
                    lambda x: hasattr(x, 'feature'),
                    map(
                        baseWriter.get(cat, FeatureWriter),
                        [r for i, r in filtered_df.iterrows()])
                    ),
                repeat('feature')
                ))

            with open(geojson_fn, "w+") as f:
                json.dump(features_list, f, indent=4)
