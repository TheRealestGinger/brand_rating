import csv
from collections import defaultdict

from .config import configure_argument_parser
from .constants import DATA_DIR
from .output import output, file_output


def average_rating(files):
    brand_rating = defaultdict(float)
    brand_count = defaultdict(int)
    result = []
    for filename in files:
        with open(DATA_DIR / filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                brand_rating[row['brand']] += float(row['rating'])
                brand_count[row['brand']] += 1
        file.close()
    for brand in brand_rating:
        result.append(
            (brand, round(brand_rating[brand] / brand_count[brand], 2))
        )
    return sorted(result, key=lambda x: x[1], reverse=True)


MODE_TO_FUNCTION = {
    'average-rating': average_rating,
}


def main():
    args = configure_argument_parser().parse_args()
    result = MODE_TO_FUNCTION[args.mode](args.files)
    output(result)
    file_output(result, args.report)


if __name__ == '__main__':
    main()
