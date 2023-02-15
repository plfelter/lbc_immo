from pathlib import Path
import logging
import argparse

from core import process


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

def main():
    args = build_argument_parser().parse_args()

    process(Path(args.input_dir), Path(args.output_dir))


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input-dir",
        type=str,
        help="Directory path of input data files from lobstr.io",
        default=data_dir,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Directory path of output geojson files",
        default=http_server_data_dir,
    )

    return parser


if __name__ == '__main__':
    main()
