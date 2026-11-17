"""Bind the built parts into the distributed sets.

  python3 assemble.py a4 OUT GUIDE CALENDARS [ESSAY]
      The A4 home set: the calibration guide, the 36 calendars, the essay if given.
      A guide of three pages (the Empirical Edition) keeps its third page, the sealed key,
      for last, padded so that it always prints on a sheet of its own.

  python3 assemble.py a3 OUT PACK ESSAY
      Adds the essay to an A3 pack as its closing sheet, scaled to A3, with a blank back.
"""
import sys
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A3, A4


def blank(w, size):
    w.add_blank_page(width=size[0], height=size[1])


def a4(out, guide, cals, essay=None):
    w = PdfWriter(); g = PdfReader(guide).pages
    key = g[2] if len(g) == 3 else None
    for p in g[:2]: w.add_page(p)
    for p in PdfReader(cals).pages: w.add_page(p)
    if essay:
        for p in PdfReader(essay).pages: w.add_page(p)
    if key is not None:
        if len(w.pages) % 2: blank(w, A4)          # the key starts a fresh sheet
        w.add_page(key); blank(w, A4)              # and nothing prints behind it
    meta(w, guide); w.write(out)


def a3(out, pack, essay):
    w = PdfWriter(clone_from=pack)
    if len(w.pages) % 2: blank(w, A3)
    e = PdfReader(essay).pages[0]
    k = A3[0] / float(e.mediabox.width)
    page = w.add_blank_page(width=A3[0], height=A3[1])
    page.merge_transformed_page(e, Transformation().scale(k, k))
    blank(w, A3)
    w.write(out)


def meta(w, src):
    m = PdfReader(src).metadata or {}
    t = (m.get('/Title') or '').replace('Calibrating the 36 calendars', 'The 36 Calendar Analog Ephemeris · A4 black and white') \
                               .replace('Calibrating the 36 cycles', 'The 36 Calendar Analog Ephemeris · A4 black and white')
    w.add_metadata({'/Title': t, '/Author': 'Aidan John Walsh'})


if __name__ == '__main__':
    mode, *a = sys.argv[1:]
    {'a4': a4, 'a3': a3}[mode](*a)
