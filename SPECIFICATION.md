# Specification

The rules every sheet is built from. `src/engine2.py` implements them; `calendars.csv` lists the result for all 36 sheets.

## Frame, clock, epoch

- Tropical zodiac throughout. Periods are mean tropical periods (Meeus / Simon et al. mean elements, of date). True positions, where needed, come from the Swiss Ephemeris (Moshier).
- Single planets are counted heliocentrically (the barycentric hypothesis). Retrogrades and stations do not appear in a mean cycle; they live inside the orb.
- A day begins at 18:00 by your own clock, everywhere, and takes the date of the day it ends in. Every printed time is symbolic. Hours are numbered 1–24 from 18:00.
- Epoch: the heliocentric Saturn–Neptune conjunction of 8 Dec 2025. Folvasin Year 0 is the March equinox of 4888 BCE; the Solar year that began at the March equinox of 2025 is 6912.

## The 36 sheets

Order: Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn, then the Nodes (1–8); then the 28 pairs in the same order, the faster body first (9–36). Codes: A Saturn, B Jupiter, C Mars, D Sun, E Venus, F Mercury, G Moon, H Nodes; a single body doubles its letter (GG … HH).

## Year markers

- A single body’s year begins as it enters the sign of its exaltation (true, heliocentric for the planets; the true March equinox for the Sun; the mean Nodes entering Gemini, backwards).
- The Moon’s year is twelve lunations from the New Moon with the Sun in Taurus.
- A pair’s year begins at its last mean conjunction in the sign of its **mutual exaltation**, the midpoint of the two exaltations taken along the shorter arc.
- The Moon’s pairs count twelve conjunctions as one year; Mercury–Sun counts three cycles (36 houses).
- Moon–Mercury and Moon–Venus are counted as seen from Earth, where both planets keep close to the Sun: twelve lunations, beginning with the month in which the Moon meets the planet in the mutual-exaltation sign.
- Year 1 of every sheet is the last such event before the epoch.

## Whole days and the rotating new year

1. Period ÷ day (or ÷ lunation on a slow sheet) = short year (whole units) + leftover hours.
2. The leftover hours set the **factor**, a whole-number factor of 24 (Hour-Step Table: 0–1 → 1, 2 → 2, 3 → 3, 4 → 4, 5–6 → 6, 7–9 → 8, 10–13 → 12, 14–16 → 16 (factor 8), 17–18 → 18 (6), 19–20 → 20 (4), 21 → 21 (3), 22 → 22 (2), 23 → 23 (1); under ½ h: step 0, factor 1; 23½ h or more: step 24, factor 24).
3. Each year starts *step* hours later than the last. If the start hour passes 24, take away 24: the year just ended is long (the intercalary day, the split last box).
4. Up to three correction tiers: every N own years, add or take away the factor. The N are chosen to keep the printed year start nearest the mean cycle over 40 000 own years, each tier at least four times the interval of the one before.

## Months

- Single planets: the twelve 30° signs from the exaltation sign, each sized by the time the body takes to cross it (Kepler, elements at the epoch), rounded cumulatively to the short year.
- The Moon, the Nodes and every pair: equal months, each boundary placed at the whole day nearest the mean cycle (the year starting, on average, half-way through box 1). Lunar months alternate 30, 29, …
- The Nodes’ months run backwards (Gemini, Taurus, Aries …) and their days count down.
- Pair months are houses of the slower body that the faster one transits (counted forward from the visible planet in a Node pair), each marked with a sign counted from the mutual-exaltation sign in house 1: a fixed label, not the sign where the pair stands, which moves on with every conjunction.
- The heavy box in month 1 is the whole day in which the body reaches its exaltation degree (a pair: the midpoint), on average.

## The sky as seen from Earth

The sheets count mean cycles; five rules turn them into the visible sky.

- **Sun:** the Sun sheet’s month is the Sun’s sign; the day, less one, is about its degree.
- **Moon:** on Moon–Sun the 1st is the New Moon and the Full Moon falls near the 15th; the Moon stands about 12° east of the Sun per day since the 1st.
- **Planets:** each Sun–planet sheet (Mercury, Venus, Mars, Jupiter, Saturn) prints, bottom left of every box, the planet’s mean distance from the Sun as seen from Earth, from circular mean orbits: g = atan2(a sin θ, a cos θ + 1), θ the mean separation planet − Sun, a the mean orbital radius in AU. E = east (evening sky), W = west (morning sky), 180 = opposition; under about 12° the planet is lost in the Sun’s glare. The planet in the sky = the Sun’s degree ± g. Two planets meet in the sky when their figures read the same on the same side.
- **The Moon’s meetings:** each Moon–planet sheet has the meeting on the 1st (for Mercury and Venus, whose months are lunations, the 1st is the New Moon; for Mars, Jupiter and Saturn, the mean meeting). The ☽ figure, bottom right of the same Sun–planet box, moves it by whole days: g ÷ (Moon − Sun motion) for Mercury and Venus, (g − θ) ÷ (Moon − planet motion) for the outer planets. Saturn’s figure is always 0 and is not printed.
- **Eclipses:** on Sun–Nodes the ◐ boxes are the days when the mean Sun stands within 18° of either Node: every eclipse falls in one.

Checked against the real sky for 2026–2035, read straight off the printed sheets: the Moon’s meetings fell within a day of the printed day for Venus every month, Saturn 98 in 100, Mercury 97, Jupiter 96, Mars 95, never more than two days out; all 45 eclipses fell in ◐ boxes.

## Slow sheets

Cycles over 1000 days (Jupiter, Saturn, the Nodes, Jupiter–Saturn, Jupiter–Nodes, Saturn–Nodes) count one box per lunation. A box begins on the 1st of a month of the Moon sheet; the Moon sheet’s ledger is run back and forward for this. One slow-sheet hour is a 24th of a lunation.

## Orb and wobble

- Orb: the largest distance, in days, between the real event and the sheet’s day, from the equations of centre of the bodies involved (for Moon–Mercury and Moon–Venus, from the planet’s greatest distance from the Sun).
- Wobble: the largest distance, in hours, between the printed year start and the exact mean cycle.

## Journal

Event first: write what happened before looking at the sheets; then fill in each body’s month and day. Planetary hours are fixed, hour 13 (06:00) belonging to the day’s ruler.
