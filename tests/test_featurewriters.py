# File to test featurewriters.py
import sys
from os.path import join, dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

import pandas as pd
from pathlib import Path
import json
from pprint import pprint

from lbc_immo.featurewriters import FeatureWriter, ImmoFeatureWriter


def test_feature_generation():
	csv_p = Path.cwd() / 'data' / '662839.csv'
	df = pd.read_csv(csv_p)
	features_list = [ImmoFeatureWriter(e).feature for i, e in df.iterrows()]
	print(json.dumps(features_list, indent=4))
	with open("testfeatures.json", "w+") as f:
		json.dump(features_list, f, indent=4)


if __name__ == '__main__':
	test_feature_generation()