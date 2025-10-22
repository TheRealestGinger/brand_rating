import csv

from tabulate import tabulate

from .constants import RESULT_DIR


def output(result):
    print(tabulate(
        result,
        headers=['brand', 'rating'],
        tablefmt='pipe',
        showindex=range(1, len(result) + 1)
    ))


def file_output(result, report):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULT_DIR / report, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerow(['brand', 'rating'])
        writer.writerows(result)
