"""Reprint the 36 A3 calendar sheets (fronts and backs) with a new two-year Date Finder window.

    python3 reprint_calendars.py 2028 11 Calendars_Nov2028.pdf

The Lifetime Tables already run to 2125; only the Date Finder window moves.
"""
import sys, datetime as dt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
import engine2 as E, a3_sheets as SH
Y,Mo,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
SH.DF_FIRST=(Y,Mo); SH.PRINT_DATE=dt.date.today()
c=canvas.Canvas(out,pagesize=landscape(A3)); c.setTitle(f'The 36 Calendar Analog Ephemeris · calendars, Date Finders from {SH.MON[Mo-1]} {Y}'); c.setAuthor('Aidan John Walsh')
for s in E.all_sheets():
    SH.front(c,s); c.showPage(); SH.back(c,s); c.showPage()
c.save(); print('written',out)
