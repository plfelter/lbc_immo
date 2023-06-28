from pathlib import Path
from unidecode import unidecode
from itertools import repeat
import json
import geojson as gj
import logging

from datawork import DataLoader, filter_for_period
from featurewriters import FeatureWriter, ImmoFeatureWriter, ImmoLocFeatureWriter


def process(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    periods = [(0, 0), (1, 1), (2, 2), (5, 3), (10, 6), (365, 11)]

    for cat, df in DataLoader(input_dir).data.items():
        for d1, d2 in periods:

            filtered_df = filter_for_period(df, 'last_publication_date', d1, d2)
            Jstr = f'J{d1}' if d1 == d2 else f'J{d1}_J{d2}'
            geojson_fn = output_dir / f"{unidecode(cat).replace(' ', '_')}_{Jstr}.json"

            features_list = list(map(
                getattr,
                filter(
                    lambda x: hasattr(x, 'feature') and type(x.feature) == gj.Feature,
                    map(
                        select_writer(cat),
                        [r for i, r in filtered_df.iterrows()])
                    ),
                repeat('feature')
                ))

            with open(geojson_fn, "w+") as f:
                json.dump(features_list, f, indent=4)

            logging.info(
                f'Written {filtered_df.shape[0]} features for {Jstr} ("{cat}" category) '
                f'to file {geojson_fn}')


def select_writer(category: str):
    writers = {
        'Ventes immobilières': ImmoFeatureWriter,
        'Locations': ImmoLocFeatureWriter
    }
    return writers.get(category, FeatureWriter)
