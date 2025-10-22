import csv
import importlib
import importlib.util
import sys
import types
from types import SimpleNamespace
import pytest

from src.constants import PROJECT_ROOT


def load_main_module():
    src_dir = PROJECT_ROOT / 'src'
    file_path = src_dir / 'main.py'
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    pkg_name = "src"
    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [str(src_dir)]
        sys.modules[pkg_name] = pkg

    module_name = "src.main"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(
        module_name,
        str(file_path),
        submodule_search_locations=[str(src_dir)]
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["brand", "rating"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def test_average_rating_single_file(tmp_path):
    mod = load_main_module()
    f = tmp_path / "a.csv"
    write_csv(
        f,
        [
            {"brand": "A", "rating": "4"},
            {"brand": "B", "rating": "3"},
            {"brand": "A", "rating": "5"}
        ]
    )
    result = mod.average_rating([str(f)])
    assert result == [("A", 4.5), ("B", 3.0)]


def test_average_rating_multiple_files(tmp_path):
    mod = load_main_module()
    f1 = tmp_path / "f1.csv"
    f2 = tmp_path / "f2.csv"
    write_csv(
        f1,
        [{"brand": "A", "rating": "4"}, {"brand": "B", "rating": "2"}]
    )
    write_csv(
        f2,
        [{"brand": "A", "rating": "5"}, {"brand": "C", "rating": "3"}]
    )
    result = mod.average_rating([str(f1), str(f2)])
    assert result == [("A", 4.5), ("C", 3.0), ("B", 2.0)]


def test_average_rating_rounding(tmp_path):
    mod = load_main_module()
    f = tmp_path / "round.csv"
    write_csv(
        f,
        [{"brand": "X", "rating": "4"}, {"brand": "X", "rating": "4.3333"}]
    )
    result = mod.average_rating([str(f)])
    assert result == [("X", 4.17)]


def test_average_rating_invalid_rating_raises(tmp_path):
    mod = load_main_module()
    f = tmp_path / "bad.csv"
    write_csv(f, [{"brand": "A", "rating": "abc"}])
    with pytest.raises(ValueError):
        mod.average_rating([str(f)])


def test_main_calls_output_and_file_output(monkeypatch, tmp_path):
    mod = load_main_module()
    f = tmp_path / "data.csv"
    write_csv(
        f,
        [{"brand": "A", "rating": "5"},
         {"brand": "B", "rating": "3"}]
    )

    args = SimpleNamespace(
        mode="average-rating",
        files=[str(f)],
        report="report.csv"
    )

    class DummyParser:
        def parse_args(self_inner):
            return args

    out_calls = []
    file_calls = []

    monkeypatch.setattr(
        mod,
        "configure_argument_parser",
        lambda: DummyParser()
    )
    monkeypatch.setattr(mod, "output", lambda res: out_calls.append(res))
    monkeypatch.setattr(
        mod,
        "file_output",
        lambda res, report: file_calls.append((res, report))
    )

    mod.main()

    assert len(out_calls) == 1
    assert len(file_calls) == 1
    expected = [("A", 5.0), ("B", 3.0)]
    assert out_calls[0] == expected
    assert file_calls[0][1] == "report.csv"


def test_main_invalid_mode_raises(monkeypatch, tmp_path):
    mod = load_main_module()
    f = tmp_path / "d.csv"
    write_csv(f, [{"brand": "A", "rating": "1"}])
    args = SimpleNamespace(mode="unknown-mode", files=[str(f)], report="r.csv")

    class DummyParser:
        def parse_args(self_inner):
            return args

    monkeypatch.setattr(
        mod,
        "configure_argument_parser",
        lambda: DummyParser()
    )

    with pytest.raises(KeyError):
        mod.main()
