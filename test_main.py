import pytest
from main import calc_avg_rating, make_report, read_files


# ВЫЧСЛЕНИЯ


def test_calc_avg_rating_valid_data():
    products = [
        {"brand": "apple", "rating": "4.9"},
        {"brand": "apple", "rating": "4.2"},
        {"brand": "samsung", "rating": "4.8"}
    ]
    result = calc_avg_rating(products)
    assert result["apple"] == pytest.approx(4.55)
    assert result["samsung"] == pytest.approx(4.8)


def test_calc_avg_rating_empty_list():
    result = calc_avg_rating([])
    assert result == {}


def test_calc_avg_rating_invalid_rating():
    products = [
        {"brand": "sony", "rating": "5"},
        {"brand": "sony", "rating": "abc"},
        {"brand": "lg", "rating": None},
        {"brand": "", "rating": "3.5"},
    ]
    result = calc_avg_rating(products)
    print(result)
    assert "sony" in result
    assert "lg" not in result
    assert isinstance(result["sony"], float)


def test_calc_avg_rating_missing_keys():
    products = [{"wrong_key": "apple", "rating": "5"}]
    result = calc_avg_rating(products)
    assert result == {}


# ЧТЕНИЕ ФАЙЛОВ


def test_read_files_valid_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("brand,rating\napple,5.0\nsamsung,4.9\n", encoding="utf-8")
    rows = list(read_files([str(csv_file)]))
    assert len(rows) == 2
    assert rows[0]["brand"] == "apple"


def test_read_files_nonexistent_file(capsys):
    file_name = "no_such_file.csv"
    rows = list(read_files([file_name]))
    out = capsys.readouterr()
    assert f"Файла {file_name} не существует!" in out.err
    assert rows == []


def test_read_files_wrong_extension(capsys, tmp_path):
    file_name = "file.txt"
    txt_file = tmp_path / file_name
    txt_file.write_text("brand,rating\napple,5\n", encoding="utf-8")
    rows = list(read_files([str(txt_file)]))
    err = capsys.readouterr().err
    assert "Не все файлы имеют расширение CSV!" in err
    assert rows == []


# СОЗДАНИЕ ОТЧЕТА


def test_make_report_creates_file(tmp_path):
    rows = [("apple", 4.55), ("samsung", 4.8)]
    out_file = tmp_path / "report.csv"
    make_report(str(out_file), rows)
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "apple" in content
    assert "samsung" in content


def test_make_report_invalid_directory(tmp_path):
    bad_dir = tmp_path / "no_such" / "no_path"
    file_path = bad_dir / "report.csv"
    rows = [("apple", 4.5)]
    make_report(str(file_path), rows)
    assert file_path.exists()