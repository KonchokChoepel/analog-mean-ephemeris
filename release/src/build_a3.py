"""The A3 pack, built entirely from engine2: 112 pages."""
import sys, datetime as dt, math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import engine2 as E, ledger as Lg
from a3_draw import *
import a3_sheets as SH
import build_journal as J
W,H=A3; M=34
S=E.all_sheets(); BY={s['code']:s for s in S}
def no(c): return BY[c]['no']
def nm(c): s=BY[c]; return f"{s['glyphs']} {s['title']}"
GOLDC=colors.Color(*GOLD); SECTC=colors.Color(*SECT); BANDC=colors.Color(*BAND)
K=1.0
def set_scale(k):
    global K,P,PS,H2
    K=k
    P=ParagraphStyle('p',fontName='DejaVuSans',fontSize=9.6*k,leading=12.8*k,spaceAfter=5*k)
    PS=ParagraphStyle('ps',parent=P,fontSize=8.6*k,leading=11.2*k,spaceAfter=3*k)
    H2=ParagraphStyle('h2',fontName='DejaVuSans-Bold',fontSize=10.5*k,leading=13*k,spaceBefore=7*k,spaceAfter=2.5*k,textColor=GOLDC)
set_scale(1.0)
import io
def fitted(c,fn,lo=0.9,hi=1.9,*args):
    """largest type scale at which fn draws without overflow"""
    from reportlab.pdfgen import canvas as _cv
    best=lo; a,b=lo,hi
    for _ in range(14):
        m=(a+b)/2; set_scale(m)
        try:
            sc=_cv.Canvas(io.BytesIO(),pagesize=c._pagesize); fn(sc,*args); ok=True
        except AssertionError: ok=False
        if ok: best=m; a=m
        else: b=m
    set_scale(best); fn(c,*args); set_scale(1.0)
TC=ParagraphStyle('tc',fontName='DejaVuSans',fontSize=8,leading=9.6)
TH=ParagraphStyle('th',fontName='DejaVuSans-Bold',fontSize=8,leading=9.6)
def tbl(rows,widths,head=True,size=8,zebra=True):
    size=size*K
    st=ParagraphStyle('t',fontName='DejaVuSans',fontSize=size,leading=size*1.2); sh=ParagraphStyle('th',parent=st,fontName='DejaVuSans-Bold')
    data=[[Paragraph(str(x),sh if (head and i==0) else st) for x in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths)
    sty=[('TOPPADDING',(0,0),(-1,-1),1.2),('BOTTOMPADDING',(0,0),(-1,-1),1.2),('LEFTPADDING',(0,0),(-1,-1),2.5),('RIGHTPADDING',(0,0),(-1,-1),2.5),('VALIGN',(0,0),(-1,-1),'TOP')]
    if head: sty+=[('BACKGROUND',(0,0),(-1,0),SECTC),('LINEBELOW',(0,0),(-1,0),0.6,GOLDC)]
    if zebra: sty+=[('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BANDC])]
    t.setStyle(TableStyle(sty)); return t
def flow(c,story,x,y,w,h):
    f=Frame(x,y,w,h,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0)
    rest=f.addFromList(story,c); assert not story,'frame overflow'
def two_cols(c,left,right,ytop,ybot):
    gw=(W-2*M-28)/2; story=left+right
    f1=Frame(M,ybot,gw,ytop-ybot,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    f2=Frame(M+gw+28,ybot,gw,ytop-ybot,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    f1.addFromList(story,c); f2.addFromList(story,c); assert not story,'overflow'
def foot(c,size=6):
    c.setFont('DejaVuSans',size); c.drawString(M,M,LIC)
def title_band(c,t,sub):
    fill(c,GOLD); c.rect(M,H-M-58,W-2*M,58,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',24); c.drawString(M+14,H-M-30,t); c.setFont('DejaVuSans',11); c.drawString(M+14,H-M-50,sub); fill(c,(0,0,0))

# ------------------------------------------------------------------ page 1: cover
def cover(c):
    fill(c,GOLD); c.rect(M,H-M-96,W-2*M,96,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',30); c.drawString(M+16,H-M-40,'THE 36 CALENDAR ANALOG EPHEMERIS')
    c.setFont('DejaVuSans-Bold',16); c.drawString(M+16,H-M-62,'A3 PACK')
    c.setFont('DejaVuSans',11); c.drawString(M+16,H-M-82,'Thirty-six calendars of the mean cycles, in whole days. Look up the date, cross off the box.'); fill(c,(0,0,0))
    y=H-M-114
    y-=para(c,'<b>What this is.</b> Each calendar counts the cycle of one planet, or of one pair of planets, in whole days, so you can see where every cycle stands on any day. '
           'Cross off a box a day, and look up the Journal Key to see what each body governs. Everything you need is printed: there is nothing to calculate.',M,y,W-2*M,size=10.5*K)+16*K
    steps=[('SET YOUR DAY, ONCE','A day begins at 18:00 by your own clock, wherever you are, and takes the date of the day it ends in. Every printed time is counted the same way everywhere: '
            'from then on, cross off a box each time your clock passes 18:00. Hours are numbered 1 to 24 from 18:00.'),
           ('LOOK UP TODAY','Turn to a calendar’s back. In its Date Finder, find today’s date: the cell says month · day. Nothing to add, subtract or count. '
            'When the Date Finder runs out, the Lifetime Table below it carries on for a hundred years.'),
           ('CROSS OFF THE BOX','On the front of the sheet, cross off that month and day. Next day, the next box. The six slow sheets move one box at each New Moon: '
            f'on the 1st of every month of the Moon sheet ({no("GG")}). Lost your place? Look today up again.')]
    for i,(t,b) in enumerate(steps):
        from reportlab.platypus import Paragraph as _P
        bh=_P(b,ParagraphStyle('x',fontName='DejaVuSans',fontSize=9.6*K,leading=12.5*K)).wrap(W-2*M-72*K,500)[1]+30*K
        fill(c,BAND); c.rect(M,y-bh,W-2*M,bh,stroke=0,fill=1); fill(c,GOLD); c.setFont('DejaVuSans-Bold',30*K); c.drawString(M+12,y-bh/2-10*K,str(i+1))
        c.setFont('DejaVuSans-Bold',11.5*K); c.drawString(M+60*K,y-17*K,t); fill(c,(0,0,0)); para(c,b,M+60*K,y-23*K,W-2*M-72*K,size=9.6*K,leading=12.5*K); y-=bh+9*K
    y-=6*K; c.setFont('DejaVuSans-Bold',13*K); c.drawString(M,y-12*K,'The sheets'); y-=20*K
    half=18; cw=(W-2*M)/2; c.setFont('DejaVuSans',9*K)
    for i,s in enumerate(S):
        x=M+(i//half)*cw; yy=y-(i%half)*13.2*K
        c.drawString(x,yy-10,f"{s['no']}"); c.drawString(x+20*K,yy-10,s['code']); c.drawString(x+46*K,yy-10,f"{s['glyphs']} {s['title'].upper()}")
        c.drawRightString(x+cw-20,yy-10,f"sheet {s['no']+3}")
    y-=half*13.2*K+14*K
    txt=[ '<b>To print.</b> Print the whole file double-sided, flipping on the LONG edge, so each back sits upright behind its front. Sheets 1–3 and 40–50 are A3 portrait; the 36 calendars (sheets 4–39) '
          'and the Journal (sheets 51–57) are A3 landscape. The Journal sheets have blank backs, so print as many copies of each weekday as you need. Sheet 1 is this page and the Journal Key; '
          'sheet 2 is the method and the tables, which replace a manual; sheet 3 is a practice ledger and the history of the method.',
          f'<b>Start with three sheets for a month:</b> No. {no("DD")} (Sun), No. {no("GG")} (Moon) and No. {no("GD")} (Moon–Sun). The Sun fixes the year, and the Moon fixes the month and carries the six slow sheets. '
          'Then add the sheets of one Almanac, the body you most want to watch, and grow from there. <b>Journal first, sheets second:</b> write the day’s events before you look at the sheets, then fill in each body’s month and day.',
          '<b>How long it lasts.</b> The Date Finders cover Nov 2026 for two years. The Lifetime Tables carry every year start (every box start, on the six slow sheets) for a hundred years, '
          'to 2125, so no sheet needs replacing in a lifetime. When a Date Finder runs out, a new one can be printed from the project repository.',
          '<b>Also in the pack.</b> Sheets 40–50: the Separation Table, then the seven Almanacs, which are A4 pages, two to an A3 sheet, double-sided. Sheets 51–57: the Journal, '
          'one A3 landscape sheet per weekday (two A4 pages, one day), with blank backs; print as many of each as you need.',
          '<b>Copyright and licence.</b> © 2026 Aidan John Walsh. Licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0). You may use, copy, print, '
          'sell and modify this work, commercially too, provided that you credit Aidan John Walsh and the Analog Mean Ephemeris, say what you changed, and release your changes, and anything built '
          'on this work, under the same licence. No part of it, original or added, may be made or held proprietary. Licence text: creativecommons.org/licenses/by-sa/4.0. The code that builds the '
          'pack is under the GNU General Public Licence v3.0. Source: github.com/KonchokChoepel/analog-mean-ephemeris.']
    for t in txt: y-=para(c,t,M,y,W-2*M,size=9.4*K)+8*K
    assert y>=M+18
    foot(c)

# ------------------------------------------------------------------ page 2: Journal Key
KEYROWS=[('G',)+J.KEY['G'],('F',)+J.KEY['F'],('E',)+J.KEY['E'],('D',)+J.KEY['D'],('C',)+J.KEY['C'],('B',)+J.KEY['B'],('A',)+J.KEY['A'],
         ('H','(none of its own: it acts through the planet it meets)','(the Head increases a thing, the Tail diminishes it)','eclipses, sudden gains and losses, arrivals and departures')]
def journal_key(c):
    title_band(c,'JOURNAL KEY · and the words used','Traditional significations, in modern terms. Tally events under them, day by day and year by year.')
    st=ParagraphStyle('k',fontName='DejaVuSans',fontSize=10.5*K,leading=13.5*K)
    rows=[[Paragraph('<b>Body</b>',st),Paragraph('<b>Trades</b>',st),Paragraph('<b>Goods</b>',st),Paragraph('<b>Matters</b>',st)]]
    for b,t,g,m in KEYROWS:
        rows.append([Paragraph(f'<font size="{20*K:.1f}">{E.GLYPH[b]}</font><br/>{E.NAMES[b]}',st),Paragraph(t,st),Paragraph(g,st),Paragraph(m,st)])
    t=Table(rows,colWidths=[90,(W-2*M-90)/3]*1+[(W-2*M-90)/3]*2)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SECTC),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BANDC]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('TOPPADDING',(0,0),(-1,-1),7*K),('BOTTOMPADDING',(0,0),(-1,-1),7*K),('LINEBELOW',(0,0),(-1,0),0.8,GOLDC)]))
    words=('<b>Box:</b> one day on a calendar (one New Moon on a slow sheet). <b>Own year:</b> one turn of a sheet’s cycle. <b>Month</b> (or <b>house</b> on a pair sheet): one of the twelve parts '
           'of an own year (36 houses on Mercury–Sun). <b>Start:</b> the day an own year begins; box 1 again. <b>Ledger:</b> the list of year-start hours, one per year, that decides which years are long. '
           '<b>Step:</b> the hours each new year moves on. <b>Factor:</b> the whole-number factor of 24 that every step and correction on a sheet is built on. <b>Ingress:</b> a body entering a sign. '
           '<b>Conjunction:</b> two bodies at the same longitude. <b>Mean:</b> regular pace, as if the orbit were a circle; <b>true:</b> where the body really is. <b>Orb:</b> how far the real sky can stand from the sheet. '
           '<b>Ephemeris:</b> a table of where the planets are. <b>Folvasin year:</b> the year count of the Solar sheet.')
    story=[t,Spacer(1,14*K),
           Paragraph('Pair calendars read from both bodies: a Mercury–Jupiter calendar speaks of contracts and courts, writing and law, short trips and long ones.',P),
           Paragraph('The Nodes carry no trade of their own. They mark where a body meets the eclipse path, so read them as turning points for whatever the other body governs.',P),
           Paragraph('<b>How to use it.</b> Write the date and what happened <b>first</b>, before you look at the sheets; then add each body’s month and day. Recording the event before its sky keeps the journal honest: '
                     'you notice what happened, not what you expected. At the turn of a month or a year, count the entries under each body and compare.',P),
           Spacer(1,10*K),Paragraph('WORDS USED IN THIS PACK',H2),Paragraph(words,P)]
    flow(c,story,M,M+20,W-2*M,H-2*M-88); foot(c)

# ------------------------------------------------------------------ pages 3-4: the method and the tables
LUTROW=list(range(24))
def step_for(h):
    L=E.LUT[h]; return L if L>0 else 24+L
def method1(c):
    title_band(c,'HOW THE CALENDARS ARE MADE · 1 · the method','From the raw cycle on each sheet to its year, its months and its corrections. Every sheet can be rebuilt with a pencil.')
    gd=BY['GD']; d=gd['des']; sec=round(gd['period']*86400); dd,hh,mm,ss=SH.hms(gd['period']); left=float(d['hrs'])
    L=Lg.Ledger(gd); rows=[['Year','Start hr','+ step','+ corr.','Total','Length']]; H_=gd['start']['hour']
    for y in range(1,11):
        corr=sum(cc for N,cc in d['tiers'] if y%N==0); tot=H_+d['s']+corr; lng=tot>24
        rows.append([str(y),f'{H_:02d}',f"+{d['s']}",(f'{corr:+d}' if corr else '–'),str(tot),f"{d['d']+lng} {'L' if lng else 'S'}"])
        H_=tot-24 if lng else tot
    hs=[[str(h) for h in range(12)],[str(step_for(h)) for h in range(12)],[str(h) for h in range(12,24)],[str(step_for(h)) for h in range(12,24)]]
    ht=Table(hs,colWidths=[(W-2*M-24)/2/12]*12)
    ht.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SECTC),('BACKGROUND',(0,2),(-1,2),SECTC),('FONTNAME',(0,0),(-1,-1),'DejaVuSans'),('FONTSIZE',(0,0),(-1,-1),8.5*K),
                            ('FONTNAME',(0,1),(-1,1),'DejaVuSans-Bold'),('FONTNAME',(0,3),(-1,3),'DejaVuSans-Bold'),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
    t1=d['tiers']
    left_story=[
     Paragraph('1 · WHAT A SHEET COUNTS',H2),
     Paragraph('Each of the 36 sheets counts the whole days of one mean cycle: the cycle of a single body (8 sheets) or the conjunction cycle of a pair (28 sheets). One turn of that cycle is the sheet’s '
               'own year; a box is one day. Only the Solar sheet’s own year is the calendar year. The mean cycle runs at regular pace, as though every orbit were a circle: retrogrades and stations '
               'do not appear, and live inside the orb. On the six slow sheets a box is one New Moon instead of one day.',P),
     Paragraph('2 · ONE FRAME, ONE CLOCK, ONE EPOCH',H2),
     Paragraph('<b>Frame.</b> Every period is tropical, measured from the equinox, so every ingress and conjunction sits in the tropical zodiac. <b>Clock.</b> A day begins at 18:00 by your own clock, '
               'wherever you are, and takes the date of the day it ends in; hours are numbered 1 to 24 from 18:00. Every printed time is symbolic and the same everywhere. <b>Epoch.</b> All sheets share one '
               'epoch: the Saturn–Neptune conjunction of 8 Dec 2025 (Folvasin Year 6912). Year 1 of each sheet begins at the last event before the epoch: a planet entering the sign of its exaltation '
               '(true, heliocentric); the Sun at the March equinox; the New Moon with the Sun in Taurus (the Moon’s own sheet); the Nodes entering Gemini; a pair at its mean conjunction in the sign of its '
               '<b>mutual exaltation</b>, the midpoint of the two exaltations: that sign is the year marker of every pair, as Taurus is the Moon’s and Cancer is Mercury–Sun’s.',P),
     Paragraph('3 · THE RAW DATA ON EVERY SHEET',H2),
     Paragraph('The period in seconds is the one number a sheet is built from. For a single body it is the mean tropical period. For a pair it is the time between conjunctions: 1 ÷ (1/Pa − 1/Pb), '
               'with the Nodes’ backward motion counted as negative. The Moon’s pairs count twelve conjunctions as one year; Mercury–Sun counts three. Moon–Mercury and Moon–Venus are counted as seen from Earth, '
               'where Mercury and Venus keep close to the Sun: their year is twelve lunations. Everything else on the sheet follows from this '
               'number and the Hour-Step Table.',P),
     Paragraph(f'4 · SECONDS TO WHOLE DAYS (Moon–Sun, No. {gd["no"]})',H2),
     Paragraph(f'{num(sec)} s ÷ 86 400 = {gd["period"]:.6f} days = {dd} d {hh} h {mm} min {ss} s. The whole days are the short year: {d["d"]}. The leftover, {gd["period"]-d["d"]:.6f} d = {left:.4f} h, '
               f'is {int(left)} whole hours. Look {int(left)} up in the Hour-Step Table: the factor is {d["factor"]} and the step is {d["s"]}. Each year begins {d["s"]} hours later than the one before. '
               f'When the start hour passes 24, take away 24: the year just ended gains a day and is the long year, {d["d"]+1}.',P),
     Paragraph('<b>Hour-Step Table</b> · shaded rows: whole leftover hours · beneath: the step (leftover under ½ h: no step, factor 1; 23½ h or more: 24). Every step is a factor of 24, or 24 less a factor.',PS),
     ht,
     Paragraph(f'5 · THE YEAR LEDGER (Moon–Sun, years 1–10)',H2),
     Paragraph('Start with Year 1’s start hour, printed in the Raw Cycle box on the back of the sheet. Add the step; add any correction (section 6). If the total is more than 24, the year is long, '
               'and you take away 24 for the next start.',P),
     tbl(rows,[x*min(K,1.45) for x in [50,50,50,50,50,60]]),
     Paragraph('These ten rows are the beginning of the same ledger that the Lifetime Table is cut from: continue it for as long as you like.',PS)]
    right_story=[
     Paragraph('6 · CORRECTION TIERS',H2),
     Paragraph(f'A whole-hour step cannot hold a cycle exactly: a small drift is left over each year. A tier removes it: every N years, the new-year hour moves forward or back by the sheet’s own factor, '
               f'always the same amount on that sheet, so its corrections stay uniform over decades, centuries and millennia. Tier 1 comes round most often and removes the largest drift; tier 2 '
               f'removes what tier 1 leaves; tier 3 what is left of that. The values of N keep the printed year start nearest the true cycle over 40 000 years. Moon–Sun, for instance: '
               + ', '.join(f'every {SH.ordn(N)} year {cc:+d} h'.replace('-','−') for N,cc in t1)+'. Years that carry a correction are marked ▲. '
               f'Venus–Jupiter (No. {no("EB")}) leaves 23.8 h a year, so its factor is 24: every year is long, except every {SH.ordn(BY["EB"]["des"]["tiers"][0][0])} year, when the tier takes the day back. '
               f'Saturn–Nodes (No. {no("AH")}) leaves almost nothing, so it has no step and corrects by +1 h.',P),
     Paragraph('7 · WOBBLE AND ORB',H2),
     Paragraph('Two figures are printed on every sheet. The <b>wobble</b> is the arithmetic: how far, in hours, the printed year start floats from the exact cycle because only whole days are counted. '
               'It stays within a day, never builds up, and returns to centre. The <b>orb</b> is the sky: how far, in days, the real body can stand from its regular-pace position, because orbits are '
               'not circles. They add: in the worst case a real event falls from the printed day by the orb plus the wobble, and usually by far less.',P),
     Paragraph('8 · MONTHS',H2),
     Paragraph('Pair sheets have twelve equal months: the short year divided by twelve, with the extra days spread evenly. On the Moon’s pairs each month is one conjunction, so the pair meets on the 1st of '
               'every month. On every other pair each month is a house, 30° of separation: the faster body in the nth house of the slower, counted forward from the visible planet when the Nodes are one of '
               'the pair. The small sign beside each house is counted from the mutual exaltation (the midpoint of the two exaltations) in house 1: a fixed label, not the sign where the pair stands, since each conjunction falls further round the zodiac than the last. Mercury–Sun runs 36 houses, three '
               'cycles, with one intercalary day after the 36th. Single-body sheets use the body’s real apsides: the year begins at the ingress into the sign of its exaltation, and the twelve months are the '
               'twelve 30° arcs of true longitude that follow, each sized by the time the body takes to cross it, rounded so that the twelve add to the short year exactly. The Nodes’ months run backwards '
               'and their days count down. The heavy box in month 1 is the whole day in which the body reaches its exaltation degree, on average.',P),
     Paragraph('8½ · THE SKY AS SEEN FROM EARTH',H2),
     Paragraph('The sheets count mean cycles; five rules turn them into the sky you see, with no instrument and no arithmetic beyond adding.',P),
     Paragraph(f'<b>The Sun.</b> On the Sun sheet (No. {no("DD")}) the month is the Sun’s sign and the day, less one, is about its degree. '
               f'<b>The Moon.</b> On Moon–Sun (No. {no("GD")}) the 1st is the New Moon and the Full Moon falls near the 15th; the Moon stands about 12° east of the Sun for every day since the 1st. '
               f'<b>The planets.</b> Each Sun–planet sheet (Nos. {no("FD")}, {no("ED")}, {no("DC")}, {no("DB")}, {no("DA")}) prints, bottom left of every box, the planet’s distance from the Sun as seen from Earth: '
               'E, east, in the evening sky; W, west, in the morning sky; 180, opposition, with the planet retrograde around it; under about 12, lost in the Sun’s glare. The planet in the sky = the Sun’s degree ± that figure; two planets meet in the sky '
               'when their figures read the same on the same side. This is the old second inequality, the planet carried round on its circle with the Sun. '
               '<b>The Moon’s meetings.</b> Each Moon–planet sheet has the meeting on the 1st; the ☽ figure on the Sun–planet sheet moves it by whole days; it is printed on the first day of each month and wherever it changes, and holds until the next (Saturn needs none). '
               f'<b>Eclipses.</b> On Sun–Nodes (No. {no("DH")}) the ◐ boxes are the eclipse seasons: a New Moon in one brings an eclipse of the Sun, a Full Moon an eclipse of the Moon.',P),
     Paragraph('Checked against the real sky for 2026–2035, read straight off the printed sheets: the Moon’s meetings fell within a day of the printed day for Venus in every month, for Saturn in 98 months in 100, '
               'Mercury 97, Jupiter 96 and Mars 95, never more than two days out; and all 45 eclipses fell in ◐ boxes.',P),
     Paragraph('9 · THE SLOW SHEETS',H2),
     Paragraph('Six sheets (Jupiter, Saturn, the Nodes, Jupiter–Saturn, Jupiter–Nodes, Saturn–Nodes) have cycles of thousands of days. On them one box is one New Moon: you cross off a box on the 1st of '
               f'every month of the Moon sheet (No. {no("GG")}). The whole method is unchanged; only the unit differs. Short years are counted in New Moons, one hour is a 24th of a lunation (about 29½ hours), '
               'and a correction falls due only when a full lunation of drift has built up.',P),
     Paragraph('10 · REBUILDING OR CHECKING A SHEET',H2),
     Paragraph('1. Take the period in seconds (the Raw Cycle box) and divide by 86 400 (or by the lunation, 2 551 443 s, on a slow sheet): the short year and the leftover hours. '
               '2. Look up the leftover hours in the Hour-Step Table: the step. 3. Take Year 1’s start hour from the Raw Cycle box and build the ledger: add the step, wrap at 24. '
               '4. Apply the tiers on the years they name (▲). 5. Compare with the Lifetime Table: the year starts must agree to the digit. 6. Compare the sky: on the day the sheet calls day 1 of month 1, '
               'the event (ingress or conjunction) happens within the orb.',P),
     Paragraph('11 · THE FOUR CHECKS',H2),
     Paragraph(f'<b>The Moon on the first.</b> On No. {no("GD")} (Moon–Sun), day 1 of every month is the New Moon; the Full Moon falls near the 15th. The orb is one day. '
               f'<b>The Sun on the sign.</b> On No. {no("DD")}, day 1 is the March equinox, the Sun at 0° Aries; each day is about a degree: look the Sun’s degree up in any ephemeris. '
               '<b>The sum.</b> A sheet’s months add to its short year. <b>Count the days.</b> Day 1 of month 1 is an event you can look up (an ingress, a conjunction, the New Moon). Count the days '
               '(or New Moons) since the last one: that is today’s box, and it must match the Date Finder.',P)]
    two_cols(c,left_story,right_story,H-M-74,M+16); foot(c)

def method2(c):
    title_band(c,'HOW THE CALENDARS ARE MADE · 2 · the tables','How every table on every sheet was prepared in advance, so that you never have to work anything out.')
    ff=BY['FF']; L=Lg.Ledger(ff); ex=dt.date(2031,5,22); dn=ex.timetuple().tm_yday
    st=[(d.timetuple().tm_yday,hr) for d,hr,y in L.year_starts_in(2031)]; jan=L.locate(dt.date(2031,1,1))[1]
    a=[q for q,_ in st if q<=dn][-1]; box=dn-a+1; assert box==L.locate(ex)[1]
    sun=Lg.sun_ledger(); s2=sun.start_date(2)
    left=[
     Paragraph('1 · THE DATE FINDER',H2),
     Paragraph('<b>What it is.</b> Every real date of two years, each solved in advance to its box on that sheet: month · day. It is the calendar run forward one day at a time and written down.',P),
     Paragraph('<b>How it was made.</b> For each date: count the days since Year 1 began; run the ledger to find the own year; take the date’s place inside that year; find its month from the month '
               'lengths; write month · day. On the slow sheets the count is in New Moons: the months of the Moon sheet, run back and forward from its own Year 1. Every entry was then checked against a second, independent count.',P),
     Paragraph('<b>Reading it.</b> Gold cells are the first day of a month, red the first day of an own year, and the bands alternate with each own year so you can see where a year turns. A grey cell '
               'is a date that does not exist. An intercalary day shows as month 12, day N, marked +.',P),
     Paragraph('<b>The window.</b> Two years, from the month of printing. Beyond it, the Lifetime Table takes over.',P),
     Paragraph('2 · THE LIFETIME TABLE',H2),
     Paragraph('<b>What it is.</b> One row for each real year, for a hundred years from printing. It outlives the Date Finder, so the sheet stays in use for a lifetime. Jan 1 is the box (the small number '
               'on the front) in which that year opens. After it come the year starts of that real year, each as a day of the year and an hour (1–24, from 18:00). On the six slow sheets the entries are '
               'instead every box start (each New Moon), and a ★ marks a new year. A row marked L is a leap year.',P),
     Paragraph('<b>How it was made.</b> The ledger was run forward for the whole century and every date turned into its box number. The table lists only the points where that number changes: on the '
               'ordinary sheets where it restarts at 1 (a new year), on the slow sheets where it steps up by one.',P),
     Paragraph(f'<b>Worked example (Mercury, No. {ff["no"]}, 22 May 2031).</b> The 2031 row reads: 1 Jan = {jan}; year starts (day · hour) '
               + ', '.join(f'{q}·{h:02d}' for q,h in st)+f'. Day of the year: days before May (120) + 22 = {dn}. The last start not later than day {dn} is {a}. Box = {dn} − {a} + 1 = {box}. Find box {box} on the front.',P),
     Paragraph('3 · MONTH STARTS',H2),
     Paragraph('The real date on which each month begins, for the year in progress and the next, with the days in each month and the Folvasin year. These are the dates for the “starts” blanks on the '
               'front. On the Moon’s pairs a month’s start is a conjunction, so these dates are the conjunction dates; on the slow sheets they are New Moons.',P),
     Paragraph(f'4 · THE SOLAR SHEET (No. {no("DD")})',H2),
     Paragraph(f'Only the Solar sheet fixes the year, and it is the one sheet owed a reprint each year: write the Solar year (6913 from {s2.day} March {s2.year}) and the seven weekday names once. '
               'Weekdays appear on this sheet alone; every other sheet counts days only.',P),
     Paragraph('5 · HOW EACH SHEET’S START WAS FOUND',H2),
     Paragraph('True positions come from the Swiss Ephemeris (Moshier’s analytical theory), mean positions from Meeus’s mean elements (Simon et al.), all tropical, of date. For each sheet, the last moment '
               'before the epoch at which its event occurred was found by bisection: the true Sun at 0°, the March equinox; a planet’s true heliocentric longitude entering the sign of its exaltation; the '
               'mean New Moon with the mean Sun in Taurus; the mean Nodes entering Gemini; a pair at mean conjunction; Mercury–Sun at the mean conjunction with the Sun in Cancer. That moment is Year 1’s '
               'start; on the slow sheets, the New Moon box in which it falls. From there each sheet runs at mean pace, so a real event falls within the orb of the printed day.',P)]
    right=[
     Paragraph('6 · THE FOLVASIN YEAR',H2),
     Paragraph(f'Folvasin years follow the Solar year. The Solar year that began at the March equinox of 2025 (20 March) is 6912, and one is added at each following equinox: 6913 began on {s2.day} March {s2.year}. '
               'Year 0 is the March equinox of 4888 BCE. On the Month Starts table, the Folvasin year is the Solar year in which that own year begins.',P),
     Paragraph('7 · THE HOUR',H2),
     Paragraph('Hours count from the start of the 18:00 day: hour 1 is 18:00 to 19:00 on the evening before the date, hour 7 begins at midnight, hour 13 at 06:00 on the date itself, and hour 21 at 14:00. '
               'A year that starts in hour 21 begins at 14:00 on the date printed. On the slow sheets one hour is one twenty-fourth of a New Moon box, about 29½ real hours.',P),
     Paragraph('8 · THE FRONT',H2),
     Paragraph('The twelve months stand in a grid of four rows and three columns, in order from month 1 at top left. Month 1 has a red title; its shaded box is the day the body reaches its exaltation, '
               'on average (on a pair sheet, the midpoint of the two exaltations). A single-body sheet names its months by sign from its exaltation sign, so each column holds one quality. On a pair sheet '
               'the months are houses, with the angular houses (1, 4, 7, 10) in the first column and each house’s zodiac sign beside it.',P),
     Paragraph('9 · THE BACK AT A GLANCE',H2),
     Paragraph('Date Finder (top): today → month · day. Month Starts, Raw Cycle, Whole Days and Tiers (middle). Lifetime Table (below): every year start, or box start, for a hundred years, with the way to '
               'read it. Sky check (foot): how to confirm the sheet against the sky.',P),
     Paragraph('10 · KEEPING THE PACK TRUE',H2),
     Paragraph('<b>Day by day.</b> Cross off a box when your clock passes 18:00 (on the slow sheets, at each New Moon). Lost days? Look today up in the Date Finder, or in the Lifetime Table once the Date Finder '
               'has run out, and cross off through to it. <b>Year’s end.</b> The last box is split: the top-left number ends a short year, the bottom-right a long one. <b>Each cycle.</b> Rub out and begin '
               'again: the sheet is a template, made for light pencil and an eraser. <b>Next window.</b> The Date Finders run to the date on the back; the Lifetime Tables do not need renewing.',P),
     Paragraph('11 · WHAT TO TRUST',H2),
     Paragraph('If two printed figures ever differ, rebuild the year from the ledger (page 3, section 10): it settles the matter. The Date Finder, the Lifetime Table and the Month Starts are all cut from the '
               'same ledger, and every entry was checked against an independent count.',P),
     Paragraph('12 · CALIBRATING ONCE',H2),
     Paragraph(f'You do this once. Find today’s box in the Date Finder. From then on, cross off a box each time your own clock passes 18:00: the count is the same for everyone. Check it against the sky '
               f'with the Moon on the first (No. {no("GD")}) and the Sun on the sign (No. {no("DD")}), and you are calibrated. The A4 home set counts from the same ledger: its calibration guide prints every sheet’s year in progress, and uses an ephemeris only to check.',P),
     Paragraph('13 · SEE ALSO',H2),
     Paragraph('Journal Key (page 2): what each body governs. Sheet 3: a practice ledger to build a year by hand, and the history this method comes from. After the calendars come the Separation Table '
               'and the seven Almanacs (A4 pages, two to a sheet), then the seven Journal sheets, one for each weekday, two A4 pages each, each with a blank back.',P)]
    two_cols(c,left,right,H-M-74,M+16); foot(c)


# ------------------------------------------------------------------ sheet 3: practice ledger and history
def practice(c):
    title_band(c,'PRACTICE LEDGER · build a year by hand','Pick any sheet, copy its numbers from the back, and run its new years forward. Then check them against the Lifetime Table.')
    ff=BY['FF']; d=ff['des']; L=Lg.Ledger(ff)
    y=H-M-74
    y-=para(c,'The calendars never ask you to calculate, but every printed year start can be rebuilt with a pencil, and doing it once is the quickest way to see how the method works. '
             'Fill in the top line from the back of any calendar (Raw Cycle and Whole Days boxes). Then work down the rows: add the step to the start hour, add a tier correction in the years it names (▲), '
             'and if the total is more than 24, take away 24: that year is long. The new hour is the next year’s start hour; the next start date is this start date plus this year’s length. '
             'When you have a few rows, find the same years in the Lifetime Table: they must agree to the digit.',M,y,W-2*M,size=10.5*K,leading=14*K)+12*K
    fields=['Sheet No.','Short year','Hour step','Factor','Tier 1 (yr, h)','Tier 2 (yr, h)','Tier 3 (yr, h)','Year 1 date','Year 1 hour']
    fw=(W-2*M)/len(fields); c.setLineWidth(0.6)
    for i,f in enumerate(fields):
        x=M+i*fw; fill(c,SECT); c.rect(x,y-30*K,fw-4,30*K,stroke=0,fill=1); fill(c,(0,0,0))
        c.setFont('DejaVuSans-Bold',7.5*K); c.drawString(x+4,y-10*K,f)
    y-=42*K
    head=['Year','Start date','Start hour','+ step','+ correction (▲)','Total','More than 24? Long / short','Length (days)','Next start date','Lifetime Table agrees?']
    ws=[0.06,0.13,0.08,0.07,0.11,0.07,0.13,0.09,0.13,0.13]; ws=[w*(W-2*M) for w in ws]
    rows=[head]
    A=ff['start']['hour']; date=ff['start']['date']
    import datetime as _dt
    for yy in (1,2):
        corr=sum(cc for N,cc in d['tiers'] if yy%N==0); tot=A+d['s']+corr; lng=tot>24
        ln=d['d']+(1 if lng else 0); nd=date+_dt.timedelta(ln)
        rows.append([str(yy),SH.fmt(date),str(A),f"+{d['s']}",(f'{corr:+d}' if corr else '–'),str(tot),('long' if lng else 'short'),str(ln),SH.fmt(nd),'yes'])
        A=tot-24 if lng else tot; date=nd
    nrows=int((y-(M+60*K))/(20*K))-1
    rows+=[['']*10 for _ in range(max(0,nrows-2))]
    t=tbl(rows,ws,size=8.5)
    t.setStyle(TableStyle([('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BANDC]),('GRID',(0,0),(-1,-1),0.3,colors.Color(*MIDGREY)),('TEXTCOLOR',(0,1),(-1,2),colors.Color(0.45,0.45,0.45)),
                           ('TOPPADDING',(0,1),(-1,-1),5*K),('BOTTOMPADDING',(0,1),(-1,-1),5*K)]))
    w,h=t.wrap(W-2*M,2000); assert y-h>=M+40*K; t.drawOn(c,M,y-h); y-=h+8*K
    para(c,f'The two grey rows are worked for you: '+('FF' if E.EMP else 'Mercury')+f' (No. {ff["no"]}), whose Year 1 began on {SH.fmt(ff["start"]["date"])} in hour {ff["start"]["hour"]}, with a step of +{d["s"]} h. '
           'Carry on from row 3, or rub them out and start any sheet of your own.',M,y,W-2*M,size=9*K)
    foot(c)

def history(c):
    title_band(c,'WHERE THIS COMES FROM · the history of the method','Whole days, intercalation, synodic cycles and tables: every part of the 36 calendars has a long ancestry.')
    story=[
     Paragraph('BABYLON: THE SKY AND THE MARKET IN ONE DIARY',H2),
     Paragraph('From about 650 BCE, scribes in Babylon kept the Astronomical Diaries: night by night, the positions of the Moon and planets, and beside them the weather, the level of the Euphrates, '
               'the prices of barley, dates, wool and other goods, and the events of the city. It is the oldest long empirical journal of sky and world side by side, and the Journal of this pack follows it. '
               'From those records came the Goal-Year texts, which predict a planet’s phenomena by its period of return: Venus after 8 years, Mercury after 46, Saturn after 59, Jupiter after 71 or 83, '
               'Mars after 47 or 79, the Moon after 18. A calendar of mean cycles, read from a table rather than from the sky, begins there.',P),
     Paragraph('METON AND THE WHOLE-DAY YEAR',H2),
     Paragraph('In Athens in 432 BCE, Meton matched 19 solar years to 235 lunar months, and Callippus refined it to 76 years. Fitting whole days and whole months to cycles that are not whole is the '
               'problem every sheet here solves with its short and long years and its intercalary day.',P),
     Paragraph('PTOLEMY: THE SECOND INEQUALITY',H2),
     Paragraph('In the 2nd century CE, Ptolemy’s Almagest and Handy Tables gave each planet a mean motion and two corrections: one for the orbit’s eccentricity, one for the planet’s place in its cycle with '
               f'the Sun. The second is the distance from the Sun printed on the Mercury–Sun (No. {no("FD")}) and Venus–Sun (No. {no("ED")}) sheets. The orb on every sheet is the first: the eccentricity '
               'these mean calendars leave aside on purpose.',P),
     Paragraph('THE ZĪJES',H2),
     Paragraph('Astronomers writing in Arabic and Persian, from al-Khwārizmī in the 9th century onward, compiled zījes: books of tables from which anyone could find a planet’s place with no more than addition. '
               'The Date Finders and Lifetime Tables follow the same idea: everything solved in advance, nothing left to calculate.',P),
     Paragraph('KHAYYAM AND GREGORY: CORRECTIONS IN TIERS',H2),
     Paragraph(f'The Jalali calendar of 1079, associated with Omar Khayyam, places 8 leap days in 33 years. The Gregorian reform of 1582 uses three tiers: a leap day every 4 years, none every 100, one again every 400. '
               f'The Sun’s sheet here steps 6 hours a year and takes 6 hours back every {BY["DD"]["des"]["tiers"][0][0]} years, a year of {BY["DD"]["period"]:.4f} days; every other sheet uses the same shape '
               'of correction, each with its own factor of 24.',P),
     Paragraph('THE FOLVASIN COUNT',H2),
     Paragraph('The years are counted from Year 0, the March equinox of 4888 BCE, taken as the dawn of civilisation; the year that began at the March equinox of 2025 is Folvasin 6912. The epoch of all 36 '
               'calendars is the Saturn–Neptune conjunction of 8 December 2025.',P),
     Paragraph('WHAT IS NEW HERE',H2),
     Paragraph('Thirty-six cycles, every single body and every pair, counted side by side in whole days on paper; each pair’s year marked by its mutual exaltation; the heliocentric, barycentric cycles '
               'kept as the instrument and the sky as seen from Earth read beside them; and a journal built to be kept honestly, event first, so that patterns can be counted from first principles, '
               'as Babylon counted them.',P)]
    two_cols(c,story,[],H-M-74,M+16); foot(c)

# ------------------------------------------------------------------ A4 halves: separation table and almanacs
AW,AH=W,H/2; AM=26
def half_frame(c,top):
    c.saveState(); c.translate(0,AH if top else 0)
def sep_table(c):
    fill(c,GOLD); c.rect(AM,AH-AM-38,AW-2*AM,38,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',15); c.drawString(AM+10,AH-AM-20,'SEPARATION TABLE · degrees to days for the 28 pairs')
    c.setFont('DejaVuSans',7.5); c.drawString(AM+10,AH-AM-32,'Mean motions · separation = angle between the two mean longitudes · whole numbers, real days unless the box column says otherwise'); fill(c,(0,0,0))
    head=['Almanac','No.','Pair (faster – slower)','Degrees per day','Days per 10°','Days per 30°','Conjunction every (days)','About years','Calendar month','Year S / L','1 box =','° per box']
    rows=[head]; groups={'G':'Moon','F':'Mercury','E':'Venus','D':'Sun','C':'Mars','B':'Jupiter','A':'Saturn/Nodes'}
    last=None
    for s in S:
        if s['code'][0]==s['code'][1]: continue
        a,b=E.bodies(s['code']); vis=s['code'] in ('GF','GE')
        rr=abs(E.rate('G')-E.rate('D')) if vis else abs(E.rate(a)-E.rate(b)); syn=360/rr
        g=groups[a] if a!=last else ''; last=a
        dpd=f'{rr:.0f}' if rr>=1 else 'under 1'
        yrs=syn/365.2422; ms=s['months']
        unit='1 lunation' if s['slow'] else '1 d'; deg=rr*(float(E.SYNODIC) if s['slow'] else 1)
        rows.append([g,str(s['no']),f"{E.GLYPH[a]} {E.NAMES[a]} – {E.GLYPH[b]} {E.NAMES[b]}"+(' (Nodes retrograde)' if b=='H' else ' (as seen from Earth)' if vis else ''),dpd,f'{10/rr:.0f}',f'{30/rr:.0f}',num(round(syn)),
                     f'{yrs:.0f}' if yrs>=1 else 'under 1',f'{min(ms)}–{max(ms)}' if min(ms)!=max(ms) else str(ms[0]),f"{s['des']['d']} / {s['des']['d']+1}",unit,f'{deg:.0f}' if deg>=1 else 'under 1'])
    st=ParagraphStyle('t',fontName='DejaVuSansCondensed',fontSize=6.6*K,leading=7.6*K); sh=ParagraphStyle('h',parent=st,fontName='DejaVuSansCondensed-Bold')
    data=[[Paragraph(x,sh if i==0 else st) for x in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=[x*(AW-2*AM)/660 for x in [52,22,170,46,40,40,60,40,52,52,46,40]])
    sty=[('BACKGROUND',(0,0),(-1,0),SECTC),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BANDC]),('TOPPADDING',(0,0),(-1,-1),0.6*K),('BOTTOMPADDING',(0,0),(-1,-1),0.6*K),('LEFTPADDING',(0,0),(-1,-1),2)]
    t.setStyle(TableStyle(sty)); w,h=t.wrap(AW-2*AM,400); t.drawOn(c,AM,AH-AM-44-h)
    txt=('<b>What this is.</b> For each of the 28 pairs, how fast the faster body gains on the slower one, written as whole days you can count on a calendar. After two bodies meet (a conjunction), the angle '
         'between them grows by the same amount every day; this table tells you when it reaches each size. <b>The columns.</b> Degrees per day: the daily gain. Days per 10° and per 30°: how many days '
         'after a conjunction the two are 10° or 30° apart; 30° is one house. Conjunction every: one cycle of the pair. Calendar month: the month printed on the pair’s calendar (on the Moon’s pairs a whole '
         'conjunction, not 30°). On the six slow calendars one box is one New Moon. <b>Example: Sun – Mars.</b> After a conjunction they are 30° apart '
         f'{30/abs(E.rate("D")-E.rate("C")):.0f} days later, opposite (180°) {180/abs(E.rate("D")-E.rate("C")):.0f} days later, and they meet again {360/abs(E.rate("D")-E.rate("C")):.0f} days later. '
         'The Nodes move backward (about −0.053° a day), so each Node pair separates at the sum of the two rates. All figures are mean; the sky differs by up to the orb printed on each calendar.')
    hh=para(c,txt,AM,AH-AM-50-h,AW-2*AM,size=7*K,leading=8.8*K)
    assert AH-AM-50-h-hh>=AM
    c.setFont('DejaVuSans',5.5); c.drawString(AM,AM-10,LIC)

ALMANACS=[('MOON',['GG','GF','GE','GD','GC','GB','GA','GH']),('MERCURY',['FF','FE','FD','FC','FB','FA','FH']),('VENUS',['EE','ED','EC','EB','EA','EH']),
          ('SUN',['DD','DC','DB','DA','DH']),('MARS',['CC','CB','CA','CH']),('JUPITER',['BB','BA','BH']),('SATURN & NODES',['AA','HH','AH'])]
def month_rule(s):
    code=s['code']; bs=E.bodies(code)
    if code=='GG': return 'twelve lunations'
    if code=='HH': return 'equal, backwards (1 box = 1 New Moon)'
    if len(bs)==1: return 'uneven (real apsides)'+(' (1 box = 1 New Moon)' if s['slow'] else '')
    if code[0]=='G': return '12 conjunctions, equal'
    if code=='FD': return '36 houses, equal'
    return 'houses, equal'+(' (1 box = 1 New Moon)' if s['slow'] else '')
def alm_cover(c,name,codes,first_page):
    fill(c,GOLD); c.rect(AM,AH-AM-52,AW-2*AM,52,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',22); c.drawString(AM+12,AH-AM-28,f'{name} CULT ALMANAC'); c.setFont('DejaVuSans',10); c.drawString(AM+12,AH-AM-44,f'{len(codes)} printable calendars · whole days · universal template'); fill(c,(0,0,0))
    y=AH-AM-66
    y-=para(c,'The same calendars as the A3 pack, at A4 and grouped by body: the body, then its pairs with the bodies that move slower. Blank templates to reprint whenever you need a fresh sheet.',AM,y,AW-2*AM,size=9*K)+8*K
    c.setFont('DejaVuSans-Bold',11*K); c.drawString(AM,y-10*K,'Contents'); y-=16*K
    rows=[['Page','A3 no.','Calendar','Short / long year','Month rule']]
    for i,cd in enumerate(codes):
        s=BY[cd]; u='New Moons' if s['slow'] else 'days'
        rows.append([str(i+2),f"{s['no']} ({cd})",f"{s['glyphs']} {s['title'].upper()}",f"{s['des']['d']} / {s['des']['d']+1} {u}",month_rule(s)])
    t=tbl(rows,[x*(AW-2*AM)/620 for x in [40,60,200,120,200]],size=8); w,h=t.wrap(AW,400); t.drawOn(c,AM,y-h); y-=h+12*K
    c.setFont('DejaVuSans-Bold',11*K); c.drawString(AM,y-10*K,'How to use these pages'); y-=14*K
    how=['1. Every page is a blank template and never changes. Print it again each year.',
         '2. Fill the top blanks (year, Gregorian date, new-year hour) from the back of the matching A3 calendar (Date Finder, Month Starts, Lifetime Table), and tick short or long year from its Lifetime Table.',
         '3. Write each month’s starting date in its “starts ____” blank, counting the day numbers from that calendar’s Month Starts.',
         '4. The last box of the year is split: in a short year the year ends on the top-left number; in a long year it ends on the bottom-right number (the Intercalary Day). The calendar has exactly as many boxes as a short year has days, and day 1 of month 1 appears once, in its own place.',
         '5. Uneven months (single-body calendars): the twelve lengths are the real ones at the epoch, long where the planet moves slowly and short where it moves fast. The apsides drift very slowly, so the back of the matching A3 calendar says until when the twelve lengths hold.',
         '6. Days begin at 18:00 by your own clock, and each day carries the Gregorian date of the day it ends in. Slow calendars move one box at each New Moon, the 1st of every month of the Moon calendar.',
         '7. Pair calendars have equal months. Each month is a house, 30° of separation between the two, with a sign beside it counted from the mutual exaltation (a fixed label, not where the pair stands); on the Moon’s pairs each month is one full conjunction cycle, '
         'and the conjunction falls on the 1st of every month.']
    for t_ in how: y-=para(c,t_,AM,y,AW-2*AM,size=8.4*K)+2*K
    assert y>=AM
    c.setFont('DejaVuSans',5.5); c.drawString(AM,AM-10,LIC)
def alm_page(c,s,name):
    band(c,AM,AH-AM,AW-2*AM,40,f"{s['glyphs']} {s['title'].upper()}",sheet_kind(s),f"CALENDAR {s['no']} OF 36  ·  {name.title()} almanac",yl(s),s['code'],tsize=17)
    y=AH-AM-46
    y-=para(c,intro(s),AM,y,AW-2*AM,size=7.6)+10
    xx=fields_line(c,s,AM,y,size=7.6); y-=13; checkboxes(c,s,AM,y,size=7.4); y-=9
    draw_calendar(c,s,AM,y,AW-2*AM,y-(AM+6),3,hb=12,colgap=14,mingap=6)
    c.setFont('DejaVuSans',5.6)
    c.drawString(AM,AM-4,'Small number = day of the year. The last box is split: the top-left number is the last day of a SHORT year, the bottom-right number the last day of a LONG year (the Intercalary Day). Day 1 of month 1 appears only once.')
    c.drawRightString(AW-AM,AM-11,f"Complete the blanks from A3 calendar {s['no']} of 36 (year, dates, new-year hour).")
def a4_halves():
    out=[('sep',None)]
    for name,codes in ALMANACS:
        out.append(('cover',(name,codes)))
        for cd in codes: out.append(('cal',(cd,name)))
    return out

def journal_a3(c,name,day):
    c.setPageSize(landscape(A3)); c.saveState(); k=landscape(A3)[0]/J.W; c.scale(k,k); J.page(c,name,day); c.restoreState(); c.showPage()
    c.setPageSize(landscape(A3)); c.showPage()

def build(out):
    global cover,journal_key,method1,method2,history,sep_table,alm_cover,alm_page,ALMANACS
    if E.EMP:
        import emp_a3 as X; X.B=sys.modules[__name__]
        cover,journal_key,method1,method2,history,sep_table,alm_cover,alm_page,ALMANACS=X.cover,X.key,X.method1,X.method2,X.protocol,X.sep_table,X.alm_cover,X.alm_page,X.ALMANACS
    c=canvas.Canvas(out,pagesize=A3); c.setTitle('The 36 Calendar Analog Ephemeris · '+('Empirical Edition · ' if E.EMP else '')+'A3 pack'); c.setAuthor('Aidan John Walsh')
    c.setPageSize(A3); fitted(c,cover); c.showPage(); c.setPageSize(A3); fitted(c,journal_key); c.showPage(); c.setPageSize(A3); fitted(c,method1); c.showPage(); c.setPageSize(A3); fitted(c,method2); c.showPage(); c.setPageSize(A3); fitted(c,practice,0.9,1.5); c.showPage(); c.setPageSize(A3); fitted(c,history); c.showPage()
    for s in S:
        c.setPageSize(landscape(A3)); SH.front(c,s); c.showPage(); c.setPageSize(landscape(A3)); SH.back(c,s); c.showPage()
    halves=a4_halves(); assert len(halves)%2==0
    for i in range(0,len(halves),2):
        c.setPageSize(A3)
        for top,(kind,arg) in zip((True,False),halves[i:i+2]):
            c.saveState(); c.translate(0,AH if top else 0)
            if kind=='sep': fitted(c,sep_table,0.9,1.8)
            elif kind=='cover': fitted(c,alm_cover,0.9,1.9,*arg,True)
            else: alm_page(c,BY[arg[0]],arg[1])
            c.restoreState()
        c.setDash(3,4); c.setLineWidth(0.4); stroke(c,MIDGREY); c.line(14,AH,W-14,AH); c.setDash(); stroke(c,(0,0,0))
        c.showPage()
    if E.EMP:
        c.setPageSize(landscape(A3)); c.saveState(); k=landscape(A3)[0]/J.W; c.scale(k,k); J.page_emp(c); c.restoreState(); c.showPage(); c.setPageSize(landscape(A3)); c.showPage()
    else:
        for name,day in J.DAYS: journal_a3(c,name,day)
    c.save()
if __name__=='__main__': build(sys.argv[1])
