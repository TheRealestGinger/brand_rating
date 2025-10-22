import csv

from src.output import output, file_output


def write_sample_rows(path):
    rows = [("A", 5), ("B", 3)]
    with open(path, "w", encoding="utf-8") as f:
        writer = csv.writer(f, dialect="unix")
        writer.writerow(["brand", "rating"])
        writer.writerows(rows)
    return rows


def test_output_prints_table(capsys):
    data = [("A", 5), ("B", 3)]
    output(data)
    captured = capsys.readouterr()
    assert "A" in captured.out
    assert "5" in captured.out
    assert "B" in captured.out
    assert "3" in captured.out


def test_file_output_writes_csv(tmp_path):
    out = tmp_path / "report.csv"
    rows = [("X", 4.5), ("Y", 2.0)]
    file_output(rows, str(out))
    assert out.exists()
    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, dialect="unix")
        contents = list(reader)
    assert contents[0] == ["brand", "rating"]
    assert contents[1] == ["X", "4.5"]
    assert contents[2] == ["Y", "2.0"]
