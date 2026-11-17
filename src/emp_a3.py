"""Empirical (blind) edition pages for the A3 pack. Imported by build_a3 when AME_EDITION=empirical."""
import datetime as dt
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import engine2 as E, ledger as Lg
import a3_sheets as SH
from a3_draw import *
B=None   # set by build_a3 to its running module
SLOW=[s['code'] for s in E.all_sheets() if s['slow']]
def no(c): return [s for s in E.all_sheets() if s['code']==c][0]['no']

def cover(c):
    W,H,M,K=B.W,B.H,B.M,B.K
    fill(c,GOLD); c.rect(M,H-M-96,W-2*M,96,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',30); c.drawString(M+16,H-M-40,'THE 36 CALENDAR ANALOG EPHEMERIS')
    c.setFont('DejaVuSans-Bold',16); c.drawString(M+16,H-M-62,'EMPIRICAL EDITION · A3 PACK')
    c.setFont('DejaVuSans',11); c.drawString(M+16,H-M-82,'Thirty-six fixed cycles in whole days, known by code alone. Record first; count later.'); fill(c,(0,0,0))
    y=H-M-114
    y-=para(c,'<b>What this is.</b> Each calendar counts one fixed cycle in whole days, so the stage of every cycle can be read for any day. The cycles carry codes, not names, and this edition '
           'says nothing about what any stage might mean. It is built for blind, retrospective pattern analysis: you keep a plain daily record, and only later, by a plan written before you began, '
           'are the entries counted against the stages of each cycle. The key to the codes is printed once, on the last page of the A4 home set, to be sealed until the analysis is done.',M,y,W-2*M,size=10.5*K)+16*K
    steps=[('SET YOUR DAY, ONCE','A day begins at 18:00 by your own clock, wherever you are, and takes the date of the day it ends in. Every printed time is counted the same way everywhere: '
            'from then on, cross off a box each time your clock passes 18:00. Hours are numbered 1 to 24 from 18:00.'),
           ('LOOK UP TODAY','Turn to a calendar’s back. In its Date Finder, find today’s date: the cell says month · day. Nothing to add, subtract or count. '
            'When the Date Finder runs out, the Lifetime Table below it carries on for a hundred years.'),
           ('CROSS OFF THE BOX',f'On the front of the sheet, cross off that month and day. Next day, the next box. The six slow sheets ({", ".join(SLOW)}) move one box on day 1 of every month '
            f'of cycle GG (sheet {no("GG")}). Lost your place? Look today up again.')]
    for i,(t,b) in enumerate(steps):
        bh=Paragraph(b,ParagraphStyle('x',fontName='DejaVuSans',fontSize=9.6*K,leading=12.5*K)).wrap(W-2*M-72*K,500)[1]+30*K
        fill(c,BAND); c.rect(M,y-bh,W-2*M,bh,stroke=0,fill=1); fill(c,GOLD); c.setFont('DejaVuSans-Bold',30*K); c.drawString(M+12,y-bh/2-10*K,str(i+1))
        c.setFont('DejaVuSans-Bold',11.5*K); c.drawString(M+60*K,y-17*K,t); fill(c,(0,0,0)); para(c,b,M+60*K,y-23*K,W-2*M-72*K,size=9.6*K,leading=12.5*K); y-=bh+9*K
    y-=6*K; c.setFont('DejaVuSans-Bold',13*K); c.drawString(M,y-12*K,'The sheets'); y-=20*K
    half=18; cw=(W-2*M)/2; c.setFont('DejaVuSans',9*K)
    for i,s in enumerate(B.S):
        x=M+(i//half)*cw; yy=y-(i%half)*13.2*K
        c.drawString(x,yy-10,f"{s['no']}"); c.setFont('DejaVuSans-Bold',9*K); c.drawString(x+20*K,yy-10,s['code']); c.setFont('DejaVuSans',9*K)
        c.drawString(x+46*K,yy-10,emp_kind(s)); c.drawRightString(x+cw-20,yy-10,f"sheet {s['no']+3}")
    y-=half*13.2*K+14*K
    txt=['<b>To print.</b> Print the whole file double-sided, flipping on the LONG edge, so each back sits upright behind its front. Sheets 1–3, 40–50 and 52 are A3 portrait; the 36 calendars (sheets 4–39) '
         'and the Journal (sheet 51) are A3 landscape. The Journal sheet has a blank back: print as many copies as you need, one per day. Sheet 1 is this page and the Recording Key; '
         'sheet 2 is the method and the tables; sheet 3 is a practice ledger and the analysis protocol.',
         '<b>Choose your cycles before you begin.</b> Keep all 36 if you can. If you keep fewer, choose them before the first entry and write the choice into your plan: a blind study must not pick '
         'its cycles after seeing the data. <b>Journal first, sheets last:</b> write the day before you look at any sheet, then fill in each cycle’s month and day.',
         '<b>How long it lasts.</b> The Date Finders cover Nov 2026 for two years. The Lifetime Tables carry every year start (every box start, on the six slow sheets) for a hundred years, '
         'to 2125, so no sheet needs replacing in a lifetime. When a Date Finder runs out, a new one can be printed from the project repository.',
         '<b>Also in the pack.</b> Sheets 40–50: the Separation Table, then seven Almanacs, which are A4 pages, two to an A3 sheet, double-sided. Sheet 51: the Journal, two A4 pages, one day. Sheet 52: the afterword, <i>What the proof against Astrology might look like, and its usefulness regardless</i>, with a blank back.',
         '<b>Copyright and licence.</b> © 2026 Aidan John Walsh. Licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0). You may use, copy, print, '
         'sell and modify this work, commercially too, provided that you credit Aidan John Walsh and the Analog Mean Ephemeris, say what you changed, and release your changes, and anything built '
         'on this work, under the same licence. Licence text: creativecommons.org/licenses/by-sa/4.0. The code that builds the pack is under the GNU General Public Licence v3.0. '
         'Source: github.com/KonchokChoepel/analog-mean-ephemeris.']
    for t in txt: y-=para(c,t,M,y,W-2*M,size=9.4*K)+8*K
    assert y>=M+18
    B.foot(c)

def key(c):
    W,H,M,K,P,H2=B.W,B.H,B.M,B.K,B.P,B.H2
    B.title_band(c,'RECORDING KEY · codes, blinding and the words used','Everything a recorder needs, and nothing that says what a cycle is.')
    st=ParagraphStyle('k',fontName='DejaVuSans',fontSize=10*K,leading=13*K)
    rows=[[Paragraph('<b>Mark</b>',st),Paragraph('<b>What it is</b>',st)],
          [Paragraph('<b>A B C D E F G H</b>',st),Paragraph('The eight cycle codes. They are labels only; the letters carry no order of importance.',st)],
          [Paragraph('<b>GG, FF, …</b>',st),Paragraph('A sheet whose code is one letter doubled counts a single cycle (8 sheets).',st)],
          [Paragraph('<b>GF, FD, …</b>',st),Paragraph('A sheet with two different letters counts the joint cycle of that pair: the time for the first to gain one full turn on the second (28 sheets).',st)],
          [Paragraph('<b>a b c … l</b>',st),Paragraph('Twelve fixed sectors, in order, each 30° of a full turn. The letter beside a month is counted on from the sector in which that cycle’s year begins. It is a fixed label: it does not move.',st)],
          [Paragraph('<b>Shaded box</b>',st),Paragraph('The reference day: a fixed point in month 1 of each cycle, on average. It is printed for counting, not because anything is expected of it.',st)]]
    t=Table(rows,colWidths=[110*K,W-2*M-110*K])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.Color(*SECT)),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.Color(*BAND)]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('TOPPADDING',(0,0),(-1,-1),6*K),('BOTTOMPADDING',(0,0),(-1,-1),6*K),('LINEBELOW',(0,0),(-1,0),0.8,colors.Color(*GOLD))]))
    words=('<b>Box:</b> one day on a calendar (one GG month on a slow sheet). <b>Own year:</b> one turn of a sheet’s cycle. <b>Month:</b> one of the twelve parts of an own year (36 on FD). '
           '<b>Start:</b> the day an own year begins; box 1 again. <b>Ledger:</b> the list of year-start hours, one per year, that decides which years are long. <b>Step:</b> the hours each new year moves on. '
           '<b>Factor:</b> the whole-number factor of 24 that every step and correction on a sheet is built on. <b>Tier:</b> a correction that falls every N own years. <b>Wobble:</b> how far, in hours, '
           'the printed year start floats from the exact cycle. <b>Mean:</b> regular pace. <b>GG month:</b> one month of cycle GG, the unit of the six slow sheets. '
           '<b>Intercalary day:</b> the extra last day of a long year. <b>Folvasin year:</b> the year count of sheet DD.')
    story=[t,Spacer(1,12*K),
       Paragraph('WHY THE KEY IS SEALED',H2),
       Paragraph('What each code stands for is printed on one page only: the last page of the A4 home set, made to be cut off and sealed. Give it, sealed, to someone who is not keeping the '
                 'journal, and open it only when the analysis is finished and written down. Knowing what a cycle is changes what you notice, what you write down and the words you choose. '
                 'Not knowing keeps the record clean. For the same reason, do not look up the periods printed on the backs: they are there for the arithmetic only.',P),
       Paragraph('THE STUDY IN FOUR STEPS',H2),
       Paragraph('<b>1. Plan.</b> Before the first entry, write down what you will count, which cycles you will keep, which stages you will compare (months, the reference day, the first day of a year), '
                 'and what result you would call a pattern. Date it, sign it, and give a copy to the key holder. <b>2. Record.</b> Every day, the day first, the calendars last. '
                 '<b>3. Tally.</b> At the end of each month and year, copy each cycle’s month and day beside every entry. <b>4. Count, then unseal.</b> Run the plan exactly as written, '
                 'write the result down, and only then open the key. Sheet 3 sets this out in full.',P),
       Spacer(1,6*K),Paragraph('WORDS USED IN THIS PACK',H2),Paragraph(words,P)]
    B.flow(c,story,M,M+20,W-2*M,H-2*M-88); B.foot(c)

def method1(c):
    W,H,M,K,P,PS,H2=B.W,B.H,B.M,B.K,B.P,B.PS,B.H2
    B.title_band(c,'HOW THE CALENDARS ARE MADE · 1 · the method','From the raw cycle on each sheet to its year, its months and its corrections. Every sheet can be rebuilt with a pencil.')
    gd=B.BY['GD']; d=gd['des']; sec=round(gd['period']*86400); dd,hh,mm,ss=SH.hms(gd['period']); left=float(d['hrs'])
    rows=[['Year','Start hr','+ step','+ corr.','Total','Length']]; H_=gd['start']['hour']
    for y in range(1,11):
        corr=sum(cc for N,cc in d['tiers'] if y%N==0); tot=H_+d['s']+corr; lng=tot>24
        rows.append([str(y),f'{H_:02d}',f"+{d['s']}",(f'{corr:+d}' if corr else '–'),str(tot),f"{d['d']+lng} {'L' if lng else 'S'}"])
        H_=tot-24 if lng else tot
    hs=[[str(h) for h in range(12)],[str(B.step_for(h)) for h in range(12)],[str(h) for h in range(12,24)],[str(B.step_for(h)) for h in range(12,24)]]
    ht=Table(hs,colWidths=[(W-2*M-24)/2/12]*12)
    ht.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),B.SECTC),('BACKGROUND',(0,2),(-1,2),B.SECTC),('FONTNAME',(0,0),(-1,-1),'DejaVuSans'),('FONTSIZE',(0,0),(-1,-1),8.5*K),
                            ('FONTNAME',(0,1),(-1,1),'DejaVuSans-Bold'),('FONTNAME',(0,3),(-1,3),'DejaVuSans-Bold'),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
    t1=d['tiers']
    L_=[Paragraph('1 · WHAT A SHEET COUNTS',H2),
     Paragraph('Each of the 36 sheets counts the whole days of one mean cycle: a single cycle (8 sheets) or the joint cycle of a pair (28 sheets). One turn of that cycle is the sheet’s own year; '
               f'a box is one day. Only sheet DD’s own year is the calendar year. The mean cycle runs at a regular pace. On the six slow sheets ({", ".join(SLOW)}) a box is one GG month instead of one day.',P),
     Paragraph('2 · ONE CLOCK, ONE EPOCH',H2),
     Paragraph('<b>Clock.</b> A day begins at 18:00 by your own clock, wherever you are, and takes the date of the day it ends in; hours are numbered 1 to 24 from 18:00. Every printed time is the '
               'same everywhere. <b>Epoch.</b> All sheets share one epoch, 8 Dec 2025 (Folvasin Year 6912). Year 1 of each sheet begins at the last time its cycle passed its start point before the epoch. '
               'Each start point was fixed once and never changes.',P),
     Paragraph('3 · THE RAW DATA ON EVERY SHEET',H2),
     Paragraph('The period in seconds is the one number a sheet is built from. For a single cycle it is the mean period. For a joint cycle it is the time for the first to gain one full turn on the second: '
               '1 ÷ (1/Pa − 1/Pb), with HH counted as negative, since it runs backwards. The G pairs count twelve cycles as one year; FD counts three; GF and GE count twelve GG months. '
               'Everything else on the sheet follows from this number and the Hour-Step Table.',P),
     Paragraph(f'4 · SECONDS TO WHOLE DAYS (GD, No. {gd["no"]})',H2),
     Paragraph(f'{num(sec)} s ÷ 86 400 = {gd["period"]:.6f} days = {dd} d {hh} h {mm} min {ss} s. The whole days are the short year: {d["d"]}. The leftover, {gd["period"]-d["d"]:.6f} d = {left:.4f} h, '
               f'is {int(left)} whole hours. Look {int(left)} up in the Hour-Step Table: the factor is {d["factor"]} and the step is {d["s"]}. Each year begins {d["s"]} hours later than the one before. '
               f'When the start hour passes 24, take away 24: the year just ended gains a day and is the long year, {d["d"]+1}.',P),
     Paragraph('<b>Hour-Step Table</b> · shaded rows: whole leftover hours · beneath: the step (leftover under ½ h: no step, factor 1; 23½ h or more: 24). Every step is a factor of 24, or 24 less a factor.',PS),
     ht,
     Paragraph('5 · THE YEAR LEDGER (GD, years 1–10)',H2),
     Paragraph('Start with Year 1’s start hour, printed in the Raw Cycle box on the back of the sheet. Add the step; add any correction (section 6). If the total is more than 24, the year is long, '
               'and you take away 24 for the next start.',P),
     B.tbl(rows,[x*min(K,1.45) for x in [50,50,50,50,50,60]]),
     Paragraph('These ten rows are the beginning of the same ledger that the Lifetime Table is cut from: continue it for as long as you like.',PS)]
    R_=[Paragraph('6 · CORRECTION TIERS',H2),
     Paragraph(f'A whole-hour step cannot hold a cycle exactly: a small drift is left over each year. A tier removes it: every N years, the new-year hour moves forward or back by the sheet’s own factor, '
               f'always the same amount on that sheet. Tier 1 comes round most often and removes the largest drift; tier 2 removes what tier 1 leaves; tier 3 what is left of that. The values of N keep '
               f'the printed year start nearest the exact cycle over 40 000 years. GD, for instance: '+', '.join(f'every {SH.ordn(N)} year {cc:+d} h'.replace('-','−') for N,cc in t1)+'. Years that carry a correction are marked ▲. '
               f'EB (No. {no("EB")}) leaves 23.8 h a year, so its factor is 24: every year is long, except every {SH.ordn(B.BY["EB"]["des"]["tiers"][0][0])} year, when the tier takes the day back. '
               f'AH (No. {no("AH")}) leaves almost nothing, so it has no step and corrects by +1 h.',P),
     Paragraph('7 · WOBBLE',H2),
     Paragraph('The <b>wobble</b>, printed on every sheet, is how far, in hours, the printed year start floats from the exact cycle because only whole days are counted. It stays within a day, never builds up, '
               'and returns to centre.',P),
     Paragraph('8 · MONTHS',H2),
     Paragraph('Joint cycles have twelve equal months: the short year divided by twelve, with the extra days spread evenly. On the G pairs each month is one whole cycle. FD runs 36 months, three cycles, '
               'with one intercalary day after the 36th. The single cycles, except GG and HH, have twelve unequal months: each is the time the cycle takes to cross one 30° sector, rounded so that the twelve '
               'add to the short year exactly. GG’s months alternate 29 and 30 days; HH’s are equal, run backwards, and their days count down. The letter beside each month is counted on from the '
               'sector in which the year begins: a fixed label. The heavy box in month 1 is the reference day, on average.',P),
     Paragraph('9 · THE SLOW SHEETS',H2),
     Paragraph(f'Six sheets ({", ".join(SLOW)}) have cycles of thousands of days. On them one box is one GG month: you cross off a box on day 1 of every month of GG (No. {no("GG")}). The method is '
               'unchanged; only the unit differs. Short years are counted in GG months, one hour is a 24th of a GG month (about 29½ hours), and a correction falls due only when a full GG month of drift has built up.',P),
     Paragraph('10 · REBUILDING OR CHECKING A SHEET',H2),
     Paragraph('1. Take the period in seconds (the Raw Cycle box) and divide by 86 400 (or by the GG month, 2 551 443 s, on a slow sheet): the short year and the leftover hours. '
               '2. Look up the leftover hours in the Hour-Step Table: the step. 3. Take Year 1’s start hour from the Raw Cycle box and build the ledger: add the step, wrap at 24. '
               '4. Apply the tiers on the years they name (▲). 5. Compare with the Lifetime Table: the year starts must agree to the digit.',P),
     Paragraph('11 · THE THREE CHECKS',H2),
     Paragraph('<b>The sum.</b> A sheet’s months add to its short year. <b>The ledger.</b> Every year start in the Lifetime Table follows from Year 1 by the rule above. <b>The two counts.</b> '
               'Count the days (or GG months) from any year start to today: that is today’s box, and it must match the Date Finder. The pack is checked against itself, never against anything outside it.',P)]
    B.two_cols(c,L_,R_,H-M-74,M+16); B.foot(c)

def method2(c):
    W,H,M,K,P,H2=B.W,B.H,B.M,B.K,B.P,B.H2
    B.title_band(c,'HOW THE CALENDARS ARE MADE · 2 · the tables','How every table on every sheet was prepared in advance, so that you never have to work anything out.')
    ff=B.BY['FF']; L=Lg.Ledger(ff); ex=dt.date(2031,5,22); dn=ex.timetuple().tm_yday
    st=[(d.timetuple().tm_yday,hr) for d,hr,y in L.year_starts_in(2031)]; jan=L.locate(dt.date(2031,1,1))[1]
    a=[q for q,_ in st if q<=dn][-1]; box=dn-a+1; assert box==L.locate(ex)[1]
    sun=Lg.sun_ledger(); s2=sun.start_date(2)
    L_=[Paragraph('1 · THE DATE FINDER',H2),
     Paragraph('<b>What it is.</b> Every real date of two years, each solved in advance to its box on that sheet: month · day. It is the calendar run forward one day at a time and written down.',P),
     Paragraph('<b>How it was made.</b> For each date: count the days since Year 1 began; run the ledger to find the own year; take the date’s place inside that year; find its month from the month '
               'lengths; write month · day. On the slow sheets the count is in GG months, run back and forward from GG’s own Year 1. Every entry was then checked against a second, independent count.',P),
     Paragraph('<b>Reading it.</b> Gold cells are the first day of a month, red the first day of an own year, and the bands alternate with each own year so you can see where a year turns. A grey cell '
               'is a date that does not exist. An intercalary day shows as month 12, day N, marked +.',P),
     Paragraph('<b>The window.</b> Two years, from the month of printing. Beyond it, the Lifetime Table takes over.',P),
     Paragraph('2 · THE LIFETIME TABLE',H2),
     Paragraph('<b>What it is.</b> One row for each real year, for a hundred years from printing. Jan 1 is the box (the small number on the front) in which that year opens. After it come the year starts '
               'of that real year, each as a day of the year and an hour (1–24, from 18:00). On the six slow sheets the entries are instead every box start (day 1 of each GG month), and a ★ marks a new year. '
               'A row marked L is a leap year.',P),
     Paragraph('<b>How it was made.</b> The ledger was run forward for the whole century and every date turned into its box number. The table lists only the points where that number changes.',P),
     Paragraph(f'<b>Worked example (FF, No. {ff["no"]}, 22 May 2031).</b> The 2031 row reads: 1 Jan = {jan}; year starts (day · hour) '
               + ', '.join(f'{q}·{h:02d}' for q,h in st)+f'. Day of the year: days before May (120) + 22 = {dn}. The last start not later than day {dn} is {a}. Box = {dn} − {a} + 1 = {box}. Find box {box} on the front.',P),
     Paragraph('3 · MONTH STARTS',H2),
     Paragraph('The real date on which each month begins, for the year in progress and the next, with the days in each month and the Folvasin year. These are the dates for the “starts” blanks on the front.',P),
     Paragraph(f'4 · SHEET DD (No. {no("DD")})',H2),
     Paragraph(f'Sheet DD fixes the year, and it is the one sheet owed a reprint each year: write its year (6913 from {s2.day} March {s2.year}) and the seven weekday names once. '
               'Weekdays appear on this sheet alone; every other sheet counts days only.',P),
     Paragraph('5 · HOW EACH SHEET’S START WAS FOUND',H2),
     Paragraph('Year 1 of every sheet was fixed once, before printing, from published astronomical tables: the last moment before the epoch at which the cycle passed its start point, found by bisection. '
               'On the slow sheets, Year 1 begins in the GG month that holds that moment. From there each sheet runs on its own count at mean pace, and nothing outside the pack is consulted again.',P)]
    R_=[Paragraph('6 · THE FOLVASIN YEAR',H2),
     Paragraph(f'Folvasin years follow sheet DD. The DD year that began on 20 March 2025 is 6912, and one is added at each following DD year start: 6913 began on {s2.day} March {s2.year}. '
               'On the Month Starts table, the Folvasin year is the DD year in which that own year begins.',P),
     Paragraph('7 · THE HOUR',H2),
     Paragraph('Hours count from the start of the 18:00 day: hour 1 is 18:00 to 19:00 on the evening before the date, hour 7 begins at midnight, hour 13 at 06:00 on the date itself, and hour 21 at 14:00. '
               'A year that starts in hour 21 begins at 14:00 on the date printed. On the slow sheets one hour is one twenty-fourth of a GG month box, about 29½ real hours.',P),
     Paragraph('8 · THE FRONT',H2),
     Paragraph('The months stand in a grid of rows of three, in order from month 1 at top left. Month 1 has a red title; its shaded box is the reference day, on average. The letter beside each month is a fixed label.',P),
     Paragraph('9 · THE BACK AT A GLANCE',H2),
     Paragraph('Date Finder (top): today → month · day. Month Starts, Raw Cycle, Whole Days and Tiers (right). Lifetime Table (below the Date Finder): every year start, or box start, for a hundred years, '
               'with the way to read it. Checking (foot): how the sheet is checked against its own ledger.',P),
     Paragraph('10 · KEEPING THE PACK TRUE',H2),
     Paragraph('<b>Day by day.</b> Cross off a box when your clock passes 18:00 (on the slow sheets, on day 1 of each GG month). Lost days? Look today up in the Date Finder, or in the Lifetime Table once the '
               'Date Finder has run out, and cross off through to it. <b>Year’s end.</b> The last box is split: the top-left number ends a short year, the bottom-right a long one. <b>Each cycle.</b> Rub out and '
               'begin again: the sheet is a template, made for light pencil and an eraser.',P),
     Paragraph('11 · WHAT TO TRUST',H2),
     Paragraph('If two printed figures ever differ, rebuild the year from the ledger (page 3, section 10): it settles the matter. The Date Finder, the Lifetime Table and the Month Starts are all cut from the '
               'same ledger, and every entry was checked against an independent count.',P),
     Paragraph('12 · CALIBRATING ONCE',H2),
     Paragraph('You do this once. Find today’s box in the Date Finder. From then on, cross off a box each time your own clock passes 18:00: the count is the same for everyone. '
               'The A4 home set counts from the same ledger: its calibration guide prints every sheet’s year in progress.',P),
     Paragraph('13 · SEE ALSO',H2),
     Paragraph('Recording Key (page 2): the codes and the blinding. Sheet 3: a practice ledger and the analysis protocol. After the calendars come the Separation Table and the seven Almanacs '
               '(A4 pages, two to a sheet), then the Journal sheet, two A4 pages, with a blank back.',P)]
    B.two_cols(c,L_,R_,H-M-74,M+16); B.foot(c)

def protocol(c):
    H,M,P,H2=B.H,B.M,B.P,B.H2
    B.title_band(c,'ANALYSIS PROTOCOL · from daily record to counts','A plan before the first entry, a plain record every day, and the key opened last.')
    story=[
     Paragraph('WHY BLIND, AND WHY AFTERWARDS',H2),
     Paragraph('A record kept by someone who expects a pattern tends to find it: in what gets noticed, what gets written down and how it is worded. This edition removes the expectation. The recorder knows '
               'the cycles only by code, and no stage is said to mean anything. Patterns are looked for afterwards, in the finished record, by a method fixed before it began.',P),
     Paragraph('1 · BEFORE THE FIRST ENTRY: THE PLAN',H2),
     Paragraph('Write down, in a few lines: what kinds of entry you will count; which cycles you will keep (all 36, or a list); which stages you will compare (the months of each cycle, the reference day, '
               'the first and last day of the year, the intercalary day); how long you will record; and what you would accept as a pattern, and what not. Date and sign it, and give a copy to the '
               'key holder. Changing the plan later is allowed only if the change is dated and kept with the original.',P),
     Paragraph('2 · EVERY DAY: THE RECORD',H2),
     Paragraph('Use the Journal sheet. Write the day first, in plain words, by the hour (1–24 from 18:00). Then, last, copy each cycle’s month and day from the calendars. Keep empty days too: '
               '“nothing” is a result. Never change an old entry; add a dated correction beside it.',P),
     Paragraph('3 · AT EACH MONTH AND YEAR END: THE TALLY',H2),
     Paragraph('List the entries of each kind, and beside each one the month (and day) of each cycle you keep. A spreadsheet, or one sheet of paper per cycle, does the job.',P),
     Paragraph('4 · COUNTING FAIRLY',H2),
     Paragraph('<b>Days, not months.</b> Months differ in length, and so does the number of days you actually recorded in each. The fair expectation for a month is the total count × (days recorded in that month '
               '÷ days recorded in all). Compare what you counted with that, not with an equal share. <b>Many cells.</b> 36 cycles of 12 months make 432 cells, and some will look striking by chance alone. '
               'Decide in the plan which comparisons count, or split the record: look for patterns in the first half, then test only those in the second. <b>Enough data.</b> Slow cycles need years of '
               'records before every month has been seen even once; the plan should say which cycles your recording period can test.',P),
     Paragraph('5 · UNSEALING',H2),
     Paragraph('Run the plan exactly as written and write the results down, including what found nothing. Only then open the key, the last page of the A4 home set. If you share the work, share the plan, '
               'the record and the tallies together, so that anyone can count again.',P),
     Paragraph('THE FOLVASIN COUNT',H2),
     Paragraph('The years are counted on sheet DD from Year 0, 4888 BCE, taken as the dawn of civilisation; the DD year that began on 20 March 2025 is Folvasin 6912. The epoch of all 36 calendars is 8 December 2025.',P)]
    B.two_cols(c,story,[],H-M-74,M+16); B.foot(c)

ALMANACS=[('G',['GG','GF','GE','GD','GC','GB','GA','GH']),('F',['FF','FE','FD','FC','FB','FA','FH']),('E',['EE','ED','EC','EB','EA','EH']),
          ('D',['DD','DC','DB','DA','DH']),('C',['CC','CB','CA','CH']),('B',['BB','BA','BH']),('A & H',['AA','HH','AH'])]
def month_rule(s):
    code=s['code']; bs=E.bodies(code); u=' (1 box = 1 GG month)' if s['slow'] else ''
    if code=='GG': return '29 and 30 days, alternating'
    if code=='HH': return 'equal, backwards'+u
    if len(bs)==1: return 'unequal'+u
    if code in ('GF','GE'): return '12 GG months'
    if code[0]=='G': return '12 cycles, equal'
    if code=='FD': return '36, equal'
    return 'equal'+u
def alm_cover(c,name,codes,first_page):
    AW,AH,AM,K=B.AW,B.AH,B.AM,B.K
    fill(c,GOLD); c.rect(AM,AH-AM-52,AW-2*AM,52,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',22); c.drawString(AM+12,AH-AM-28,f'ALMANAC {name}'); c.setFont('DejaVuSans',10); c.drawString(AM+12,AH-AM-44,f'{len(codes)} printable calendars · whole days · universal template'); fill(c,(0,0,0))
    y=AH-AM-66
    y-=para(c,f'The same calendars as the A3 pack, at A4, grouped by first letter: the single cycle, then its pairs.',AM,y,AW-2*AM,size=9*K)+8*K
    c.setFont('DejaVuSans-Bold',11*K); c.drawString(AM,y-10*K,'Contents'); y-=16*K
    rows=[['Page','A3 no.','Calendar','Short / long year','Months']]
    for i,cd in enumerate(codes):
        s=B.BY[cd]; u='GG months' if s['slow'] else 'days'
        rows.append([str(i+2),f"{s['no']}",cd,f"{s['des']['d']} / {s['des']['d']+1} {u}",month_rule(s)])
    t=B.tbl(rows,[x*(AW-2*AM)/620 for x in [40,60,120,160,240]],size=8); w,h=t.wrap(AW,400); t.drawOn(c,AM,y-h); y-=h+12*K
    c.setFont('DejaVuSans-Bold',11*K); c.drawString(AM,y-10*K,'How to use these pages'); y-=14*K
    how=['1. Every page is a blank template and never changes. Print it again each year.',
         '2. Fill the top blanks (year, Gregorian date, new-year hour) from the back of the matching A3 calendar, and tick short or long year from its Lifetime Table.',
         '3. Write each month’s starting date in its “starts ____” blank, from that calendar’s Month Starts.',
         '4. The last box of the year is split: in a short year the year ends on the top-left number; in a long year it ends on the bottom-right number (the Intercalary Day).',
         '5. Unequal months (single cycles): the back of the matching A3 calendar says until when the twelve lengths hold.',
         '6. Days begin at 18:00 by your own clock, and each day carries the date of the day it ends in. Slow calendars move one box on day 1 of every GG month.',
         '7. The letter beside each month is a fixed label counted on from the start point; it does not move.']
    for t_ in how: y-=para(c,t_,AM,y,AW-2*AM,size=8.4*K)+2*K
    assert y>=AM
    c.setFont('DejaVuSans',5.5); c.drawString(AM,AM-10,LIC)
def alm_page(c,s,name):
    AW,AH,AM=B.AW,B.AH,B.AM
    band(c,AM,AH-AM,AW-2*AM,40,s['title'].upper(),sheet_kind(s),f"CALENDAR {s['no']} OF 36  ·  almanac {name}",yl(s),s['code'],tsize=17)
    y=AH-AM-46
    y-=para(c,intro(s),AM,y,AW-2*AM,size=7.6)+10
    fields_line(c,s,AM,y,size=7.6); y-=13; checkboxes(c,s,AM,y,size=7.4); y-=9
    draw_calendar(c,s,AM,y,AW-2*AM,y-(AM+6),3,hb=12,colgap=14,mingap=6)
    c.setFont('DejaVuSans',5.6)
    c.drawString(AM,AM-4,'Small number = day of the year. The last box is split: the top-left number is the last day of a SHORT year, the bottom-right number the last day of a LONG year (the Intercalary Day).')
    c.drawRightString(AW-AM,AM-11,f"Complete the blanks from A3 calendar {s['no']} of 36 (year, dates, new-year hour).")
def sep_table(c):
    AW,AH,AM,K=B.AW,B.AH,B.AM,B.K
    fill(c,GOLD); c.rect(AM,AH-AM-38,AW-2*AM,38,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',15); c.drawString(AM+10,AH-AM-20,'SEPARATION TABLE · degrees to days for the 28 joint cycles')
    c.setFont('DejaVuSans',7.5); c.drawString(AM+10,AH-AM-32,'Mean rates · separation = how far the first has gained on the second, in degrees of a full turn (360°) · real days unless the box column says otherwise'); fill(c,(0,0,0))
    head=['Almanac','No.','Code','Degrees per day','Days per 10°','Days per 30°','Joint cycle (days)','About years','Calendar month','Year S / L','1 box =','° per box']
    rows=[head]; last=None
    for s in B.S:
        if s['code'][0]==s['code'][1]: continue
        a,b=E.bodies(s['code']); vis=s['code'] in ('GF','GE')
        rr=abs(E.rate('G')-E.rate('D')) if vis else abs(E.rate(a)-E.rate(b)); syn=360/rr
        g=('A & H' if a=='A' else a) if a!=last else ''; last=a
        dpd=f'{rr:.0f}' if rr>=1 else 'under 1'; yrs=syn/365.2422; ms=s['months']
        unit='1 GG month' if s['slow'] else '1 d'; deg=rr*(float(E.SYNODIC) if s['slow'] else 1)
        rows.append([g,str(s['no']),s['code'],dpd,f'{10/rr:.0f}',f'{30/rr:.0f}',num(round(syn)),f'{yrs:.0f}' if yrs>=1 else 'under 1',
                     f'{min(ms)}–{max(ms)}' if min(ms)!=max(ms) else str(ms[0]),f"{s['des']['d']} / {s['des']['d']+1}",unit,f'{deg:.0f}' if deg>=1 else 'under 1'])
    st=ParagraphStyle('t',fontName='DejaVuSansCondensed',fontSize=6.6*K,leading=7.6*K); sh=ParagraphStyle('h',parent=st,fontName='DejaVuSansCondensed-Bold')
    data=[[Paragraph(x,sh if i==0 else st) for x in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=[x*(AW-2*AM)/660 for x in [52,22,60,56,50,50,70,50,60,60,70,60]])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),B.SECTC),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,B.BANDC]),('TOPPADDING',(0,0),(-1,-1),0.6*K),('BOTTOMPADDING',(0,0),(-1,-1),0.6*K),('LEFTPADDING',(0,0),(-1,-1),2)]))
    w,h=t.wrap(AW-2*AM,400); t.drawOn(c,AM,AH-AM-44-h)
    r=abs(E.rate("D")-E.rate("C"))
    txt=('<b>What this is.</b> For each of the 28 joint cycles, how fast the first cycle gains on the second, written as whole days you can count on a calendar. From the start of a joint cycle, the '
         'separation grows by the same amount every day; this table tells you when it reaches each size. <b>The columns.</b> Degrees per day: the daily gain. Days per 10° and per 30°: how many days '
         'after the start the separation is 10° or 30°; 30° is one month of a joint cycle. Joint cycle: one full turn. Calendar month: the month printed on that calendar (on the G pairs, a whole cycle). '
         f'On the six slow calendars one box is one GG month. <b>Example: DC.</b> The separation is 30° after {30/r:.0f} days, 180° after {180/r:.0f} days, and a full turn after {360/r:.0f} days. '
         'HH runs backwards, so each H pair separates at the sum of the two rates. GF and GE are counted in GG months. All figures are mean.')
    hh=para(c,txt,AM,AH-AM-50-h,AW-2*AM,size=7*K,leading=8.8*K)
    assert AH-AM-50-h-hh>=AM
    c.setFont('DejaVuSans',5.5); c.drawString(AM,AM-10,LIC)
