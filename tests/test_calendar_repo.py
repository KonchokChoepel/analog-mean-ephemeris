import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_calendar_csv_has_36_entries():
    with (ROOT / 'data' / 'calendars.csv').open(newline='') as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 36
    assert len({row['code'] for row in rows}) == 36
    assert rows[0]['code'] == 'DD'


def test_citation_and_license_are_clean():
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    citation_text = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    assert 'YOUR NAME' not in license_text
    assert 'YOUR-USER' not in citation_text


def test_gitignore_exists():
    assert (ROOT / '.gitignore').exists()
