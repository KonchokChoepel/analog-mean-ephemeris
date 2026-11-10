# Analog Mean Ephemeris

A Python project for generating printable, hand-usable calendars of regular-pace planetary cycles.

## What is here

| Path | What it is |
| --- | --- |
| [`src/`](src/) | Python sources that calculate the calendars and generate the PDFs |
| [`docs/`](docs/) | specification and limitations notes |
| [`data/`](data/) | calendar periods and master table |
| [`pdf/`](pdf/) | generated output files |
| [`tests/`](tests/) | project validation tests |

## Quick start

```bash
python3 -m pip install -r requirements.txt
python3 src/build_all.py
```

This rebuilds the PDF set into the `pdf/` directory.

## Repository layout

```text
analog-mean-ephemeris/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── src/
│   ├── build_all.py
│   ├── build_pdf.py
│   ├── run_all.py
│   ├── almanac.py
│   ├── apse.py
│   ├── data.py
│   ├── engine.py
│   ├── eph.py
│   ├── now36.py
│   ├── sep_table.py
│   ├── solar.py
│   └── yearend.py
├── docs/
│   ├── SPECIFICATION.md
│   └── LIMITATIONS.md
├── data/
│   └── calendars.csv
├── pdf/
│   └── generated output files
├── tests/
│   └── test_calendar_repo.py
├── .gitignore
└── legacy root files kept for compatibility during migration
```

## Notes

- The repository is in the middle of a layout cleanup: the organized paths above are available now, while the older root-level files remain for compatibility.
- The build scripts are kept path-friendly so older and newer commands remain usable.
- Generated PDFs are not tracked by default.
