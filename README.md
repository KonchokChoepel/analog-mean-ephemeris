# Analog Mean Ephemeris

**36 printable calendars of regular-pace planetary cycles, in whole numbers, for use by hand.**

An analog ephemeris: eight own-cycle calendars (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Lunar Nodes) and 28 pair calendars (every pair of the eight). You cross off one box a day on each page; every conjunction cycle and every year comes round on the printed page, with no software. Even a child can use it.

> It is a timekeeping instrument. It follows *mean* (regular-pace) cycles, not the planets' true positions; the gap (the "orb") is printed on every page. See [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

## What's here

| Path | What it is |
|---|---|
| [`pdf/36_Calendars_Hand_Pack.pdf`](pdf/36_Calendars_Hand_Pack.pdf) | The 36 Master calendars: how-to, 100-year grids, correction rules |
| [`pdf/almanacs/`](pdf/almanacs/) | Seven "cult almanac" packs: Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn and Nodes. Each holds a planet's calendar plus its pairs with the slower planets, with Month-Length Tables |
| [`pdf/Year_End_Cards.pdf`](pdf/Year_End_Cards.pdf) | One card per calendar: the next ten cycles, short or long, with last-day dates |
| [`pdf/Separation_Table.pdf`](pdf/Separation_Table.pdf) | Degrees-to-days table for the 28 pairs, in whole numbers |
| [`data/calendars.csv`](data/calendars.csv) | Periods, year lengths, start dates, worst-case error and orb for all 36 |
| [`docs/SPECIFICATION.md`](docs/SPECIFICATION.md) | The rules |
| [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) | What it does not do, and what is unverified |
| [`src/`](src/) | Python that generates every PDF |

## The idea in brief

- **One epoch:** the Saturn–Neptune conjunction of 8 Dec 2025, in Folvasin Year 6912 (Year 0 is symbolically the March equinox of 4888 BCE).
- **Whole days:** a day begins at 18:00 UTC and carries the Gregorian date of the day it ends in. Each cycle is a short year (`d` days) or a long year (`d+1`), and the last box of month 12 is split to show both.
- **Corrections you can look up:** a small hour-factor table plus up to three tiers of correction years keep every calendar within a day of its true mean cycle (mean worst case 8.8 hours).
- **Months from real orbits:** single-planet months are 12 arcs of 30° true longitude, rounded to whole days; a Month-Length Table lists the rare changes over about 5,000 years. Pair months are houses of the slower planet.
- **Only one page is reprinted each year:** the Solar page, which fixes the year. The rest are reusable.

Full rules: [docs/SPECIFICATION.md](docs/SPECIFICATION.md).

## Rebuild the PDFs

```bash
pip install -r requirements.txt
python3 src/build_all.py                      # writes ./output/
python3 src/build_all.py 2027-01-01T18:00:00  # Year-End Cards counted from another UTC moment
```

Takes about 20 seconds. Needs DejaVu fonts (set `DEJAVU_DIR` if they are not in `/usr/share/fonts/truetype/dejavu/`). The orbital elements are Standish (1800–2050) and sit in `src/eph.py`.

## Status

The calendar arithmetic is complete and reproducible. **The epoch has not been checked against a modern ephemeris such as JPL DE440**, and may be off by up to about 3 days; see the limitations. Independent checking is welcome.

## Licence

Code: MIT. PDFs, data and text: CC BY 4.0. See [LICENSE](LICENSE). Replace `YOUR NAME` in `LICENSE` and `CITATION.cff`, and `YOUR-USER` in `CITATION.cff`, before publishing.
