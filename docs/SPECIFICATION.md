# Specification

The rules the 36 calendars follow. Everything is whole days; the aim is a set of printed pages that can be used by hand.

## Frame
- **Epoch:** the heliocentric Saturn–Neptune conjunction, 8 Dec 2025 (about 16:30 UTC). It is the shared reference for every calendar.
- **Year numbering (Folvasin Year):** the epoch falls in Year 6912. Year 0 is attached, symbolically, to the March equinox of 4888 BCE; Year 1 is 4887 BCE.
- **Only the Solar calendar fixes the year.** Every other calendar's start date is also given as a Solar date. Only the Solar page needs reprinting each year; the others are reusable.
- **Day:** begins at 18:00 UTC and carries the Gregorian date of the day it ends in. Hour 0 is 18:00 UTC.
- **Slow calendars:** where the cycle is 1,000 days or more, one box is 30 real days.

## The 36 calendars
Planet key: A Saturn, B Jupiter, C Mars, D Sun, E Venus, F Mercury, G Moon, H Lunar Nodes.

- **8 own-cycle calendars:** Sun, Moon (12 lunations), Mercury, Venus, Mars, Jupiter, Saturn, Nodes. Cycles are mean (regular-pace) heliocentric.
- **28 pair calendars:** one for each pair of the eight bodies. The cycle is the mean conjunction period of the two.

See `data/calendars.csv` for periods, year lengths and start dates.

## Years and corrections
- A year has `d` days (short) or `d+1` days (long). The last box of month 12 is split: the short-year day number top-left, the long-year number bottom-right. The calendar has exactly `d` numbered days in a short year.
- The leftover hours of the true period are handled by a lookup table (hour → factor), and by up to three tiers of correction years (every N1, N2, N3 years). Tier intervals are chosen by search across the full cycle design.

## Months
- **Single-planet calendars (Sun, Mercury, Venus, Mars, Jupiter, Saturn):** 12 arcs of 30° true longitude from the start (Sun: 0° Aries; others: the planet's exaltation), computed from real orbital elements and rounded to whole days.
- **Moon (12 lunations):** from the New Moon in Taurus.
- **Pair calendars:** twelve equal months. Each month is one house (30°) of the slower planet. **Exception:** the Moon's seven pairs, whose year is twelve conjunctions; each month is one conjunction cycle.

## Weekdays
Only the Solar page carries weekdays, written annually in blank header boxes.

## Hand use
Cross off one box per day on every page. Year-End Cards say whether each cycle ends on the short or long day.
