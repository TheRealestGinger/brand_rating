import argparse

from src.config import configure_argument_parser


def test_configure_argument_parser_defaults():
    parser = configure_argument_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    ns = parser.parse_args([])
    assert ns.mode == "average-rating"
    assert getattr(ns, "files", None) is None
    assert getattr(ns, "report", None) is None


def test_configure_argument_parser_with_args():
    parser = configure_argument_parser()
    ns = parser.parse_args(
        [
            "--mode",
            "average-rating",
            "--files",
            "a.csv",
            "b.csv",
            "--report",
            "out.csv"
        ]
    )
    assert ns.mode == "average-rating"
    assert ns.files == ["a.csv", "b.csv"]
    assert ns.report == "out.csv"
