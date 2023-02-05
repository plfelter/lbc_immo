import time
from pathlib import Path
import pandas as pd

from featurewriters import FeatureWriter


data_dir = Path('/home/debian/lbc_immo/data/lobstr_delivery/')
http_server_data_dir = Path('/var/www/lbc-immo/')

def load_data(csv_file_list):
    

if __name__ == '__main__':
    load_data(data_dir.glob('*.csv'))

    #while True:
    #    time.sleep(10)
