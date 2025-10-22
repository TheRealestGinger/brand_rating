import argparse


def configure_argument_parser():
    parser = argparse.ArgumentParser(
        description='Анализ рейтинга брендов'
    )
    parser.add_argument(
        '--mode',
        default='average-rating'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        help='Загрзука файла(-ов)'
    )
    parser.add_argument(
        '--report',
        help='Режим работы (название итогового файла)'
    )
    return parser
