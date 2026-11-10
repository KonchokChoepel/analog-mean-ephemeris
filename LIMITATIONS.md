# Limitations (read before citing)

1. **Mean positions, not real positions.** The calendars follow regular-pace cycles. The true planets differ from them by an *orb*, printed on each Master page (for example Mercury–Venus about ±10 days, Moon–Mercury 3.3 days). The calendars are an arithmetic frame, not a prediction of where planets are in the sky.
2. **The epoch is not independently verified.** Orbital elements are Standish (JPL, valid 1800–2050), because the build environment had no access to DE440. The Saturn and Neptune residuals at the epoch imply it could be off by up to about 3 days. Calendars whose cycle starts near the epoch (Moon–Jupiter's Year 1 in particular) could change year label if the epoch moves.
3. **Day-boundary mismatch.** Whole-day year lengths mean about 14.7% of year starts fall in a different calendar day from the true event. This was a design choice, not an oversight.
4. **Moon calendar signs are ordinal.** The Moon's 12 lunations drift against the zodiac by about 11° a year.
5. **Month lengths.** Real-apse months are rounded to whole days; changes are listed in the Month-Length Tables (event counts over 5,000 years: Sun 15, Mercury 35, Venus 4, Mars 144, Jupiter 10, Saturn 21).
6. **Redundancy.** 15 of the 28 pairs have a slow/fast ratio below 0.1, so they add little beyond the slower planet's own calendar. The Moon calendar (12 lunations) and Moon–Sun share one period (354.367 days). The third correction tier is inert in 34 of 36 calendars.
7. **Upkeep.** About 49 cycle rollovers a year across the set.
8. **No claim about astrology.** This repository is the timekeeping instrument only; it makes no empirical claim.
