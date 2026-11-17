"""A4 calibration guide (2 pages), generated from engine2 so the table and the sheets always agree."""
import sys, datetime as dt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import engine2 as E
FD='/usr/share/fonts/truetype/dejavu/'
for n in ['DejaVuSans','DejaVuSans-Bold','DejaVuSans-Oblique','DejaVuSans-BoldOblique','DejaVuSansCondensed','DejaVuSansCondensed-Bold']:
    pdfmetrics.registerFont(TTFont(n,FD+n+'.ttf'))
addMapping('DejaVuSans',0,0,'DejaVuSans'); addMapping('DejaVuSans',1,0,'DejaVuSans-Bold')
addMapping('DejaVuSans',0,1,'DejaVuSans-Oblique'); addMapping('DejaVuSans',1,1,'DejaVuSans-BoldOblique')
W,H=A4; M=28
LIC='© 2026 Aidan John Walsh · CC BY-SA 4.0 · github.com/KonchokChoepel/analog-mean-ephemeris · Empirical Edition'
T1=ParagraphStyle('t1',fontName='DejaVuSans-Bold',fontSize=15,leading=18)
SUB=ParagraphStyle('sub',fontName='DejaVuSans',fontSize=8.2,leading=11,spaceAfter=5)
H2=ParagraphStyle('h2',fontName='DejaVuSans-Bold',fontSize=8.6,leading=10.4,spaceBefore=3.5,spaceAfter=1.2)
P=ParagraphStyle('p',fontName='DejaVuSans',fontSize=7.3,leading=9.3,spaceAfter=1.8)
SM=ParagraphStyle('sm',parent=P,fontSize=6.9,leading=8.6)
TC=ParagraphStyle('tc',fontName='DejaVuSans',fontSize=6.8,leading=8)
TH=ParagraphStyle('th',fontName='DejaVuSans-Bold',fontSize=7,leading=8.4)
TC2=ParagraphStyle('tc2',fontName='DejaVuSansCondensed',fontSize=6.7,leading=7.6)
TH2=ParagraphStyle('th2',fontName='DejaVuSansCondensed-Bold',fontSize=6.7,leading=7.6)
S=E.all_sheets(); byc={s['code']:s for s in S}
def ordn(k): return f"{k}{'th' if 10<=k%100<=20 else {1:'st',2:'nd',3:'rd'}.get(k%10,'th')}"
def nm(c): s=byc[c]; return f"{s['glyphs']} {s['title']} ({s['no']})"
def n(c): return byc[c]['no']
def fmt_date(d): return f"{d.day} {d.strftime('%b')} {d.year}"

# ---- worked example, checked against the engine's own ledger
import ledger as Lg
PRINT=dt.date(2026,11,14)
LED={x['code']:Lg.Ledger(x) for x in S}
def in_progress(code):
    L=LED[code]; y=L.year_of(PRINT); return y,L.start_date(y),L.hours[y-1]
sun=byc['DD']; des=sun['des']; st=sun['start']
def step(H,y):
    tot=H+des['s']+sum(c for N,c in des['tiers'] if y%N==0)
    return (tot-24,True) if tot>24 else (tot,False)
Y0,d1,H1=in_progress('DD'); H2_,long1=step(H1,Y0); d2=d1+dt.timedelta(des['d']+long1)
H3,long2=step(H2_,Y0+1); d3=d2+dt.timedelta(des['d']+long2)
assert d2==LED['DD'].start_date(Y0+1) and H2_==LED['DD'].hours[Y0] and d3==LED['DD'].start_date(Y0+2) and H3==LED['DD'].hours[Y0+1]
def ordn(k): return f"{k}{'th' if 10<=k%100<=20 else {1:'st',2:'nd',3:'rd'}.get(k%10,'th')}"
ex=(f"<b>Example, sheet DD ({sun['no']}).</b> Year {Y0} began {fmt_date(d1)}, hour {H1}. {H1} + {des['s']} = {H1+des['s']}, "
    f"{'more than 24' if long1 else 'not more than 24'}{', and '+str(H1+des['s'])+' − 24 = '+str(H2_) if long1 else ''}, so year {Y0} is {'long' if long1 else 'short'} ({des['d']+long1} days): "
    f"year {Y0+1} begins {fmt_date(d2)} in hour {H2_}. {H2_} + {des['s']} = {H2_+des['s']}, {'more than 24' if long2 else 'not more than 24'}, "
    f"so year {Y0+1} is {'long' if long2 else 'short'} ({des['d']+long2} days){', and '+str(H2_+des['s'])+' − 24 = '+str(H3) if long2 else ''}: "
    f"year {Y0+2} begins {fmt_date(d3)} in hour {H3}. In year {des['tiers'][0][0]} DD's tier {'adds' if des['tiers'][0][1]>0 else 'takes away'} {abs(des['tiers'][0][1])} h as well.")

def page_deco(c,doc):
    c.setFont('DejaVuSans',6); c.drawCentredString(W/2,M-12,LIC)

def tbl(rows,widths,head):
    data=[[Paragraph(x,TH) for x in head]]+[[Paragraph(x,TC) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('LINEBELOW',(0,1),(-1,-1),0.25,colors.grey),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),1.6),('BOTTOMPADDING',(0,0),(-1,-1),1.6),('LEFTPADDING',(0,0),(-1,-1),2)]))
    return t
FW=W-2*M
T1=ParagraphStyle('t1',fontName='DejaVuSans-Bold',fontSize=17,leading=21)
SUB=ParagraphStyle('sub',fontName='DejaVuSans',fontSize=9.6,leading=12.5,spaceAfter=7)
H2=ParagraphStyle('h2',fontName='DejaVuSans-Bold',fontSize=10.2,leading=12.6,spaceBefore=6,spaceAfter=2)
P=ParagraphStyle('p',fontName='DejaVuSans',fontSize=8.9,leading=11.6,spaceAfter=2.6)
SM=ParagraphStyle('sm',parent=P,fontSize=8,leading=10)
TC=ParagraphStyle('tc',fontName='DejaVuSans',fontSize=8.2,leading=10)
TH=ParagraphStyle('th',fontName='DejaVuSans-Bold',fontSize=8.2,leading=10)
TC2=ParagraphStyle('tc2',fontName='DejaVuSansCondensed',fontSize=7.6,leading=9.4)
TH2=ParagraphStyle('th2',fontName='DejaVuSansCondensed-Bold',fontSize=7.6,leading=9.4)

SLOW=[s_['code'] for s_ in S if s_['slow']]
story=[Paragraph('CALIBRATING THE 36 CYCLES · EMPIRICAL EDITION',T1),
 Paragraph('Set each sheet once by counting from the table on page 2, then cross off one box a day. Nothing outside the pack is needed, or used.',SUB),
 Paragraph('0 · First, seal the key',H2),
 Paragraph('The last page of this set says what every code stands for. It prints on a sheet of its own. <b>Before you set any sheet, cut it off unread, seal it in an envelope, and give it to someone who is not keeping the journal.</b> '
   'It is opened once, after the analysis is finished and written down (section 7). Knowing what a cycle is changes what you notice and how you word it; not knowing keeps the record clean. '
   'For the same reason, do not look up the periods printed on the sheets: they are there for the arithmetic only.',P),
 Paragraph('1 · The day',H2),
 Paragraph('A day begins at <b>18:00 by your own clock</b>, wherever you are, and takes the date of the day it ends in. '
   'Hours are numbered <b>1 to 24</b>: hour 1 begins at 18:00, hour 13 at 06:00. Every evening at 18:00, cross off one box on every daily sheet. '
   f'The six <b>slow sheets</b> ({", ".join(SLOW)}, marked “1 box = 1 GG month”) move on one box on day 1 of every month of GG ({n("GG")}).',P),
 Paragraph('2 · The codes',H2),
 Paragraph('<b>A–H</b> are the eight cycle codes, labels only. A sheet coded with one letter doubled (GG, FF …) counts a single cycle; a sheet with two letters (GF, FD …) counts the joint cycle '
   'of that pair, the time for the first to gain one full turn on the second. <b>a–l</b> are twelve fixed sectors of a full turn, 30° each, in order: the letter beside a month is counted on from the '
   'sector in which that cycle’s year begins, and never moves.',P),
 Paragraph('3 · Setting any sheet',H2),
 Paragraph('<b>a.</b> Find the sheet’s row in the table on page 2. Its <b>year in progress</b> began on the date given there: that day is box 1 of month 1. '
   'If that year has already ended by today, work out the next year’s start with the rule on page 2 (section 8) and use that.',P),
 Paragraph('<b>b.</b> Count the days that have passed from the start date to today. Today’s box in the year is that number <b>plus 1</b>.',P),
 Paragraph('<b>c.</b> Take away the month lengths printed in the headings (month 1, then month 2, and so on) until what is left is no bigger than the next month. '
   'That month is today’s month, and what is left is today’s box in it. Cross off every box before it.',P),
 Paragraph('<b>Slow sheets:</b> in b, count the GG months that have begun since the start date instead of days. Today’s box is that number plus 1; carry on with c.',P),
 Paragraph('<i>Example.</i> Start date 3 March, today 21 April: 49 days have passed, so today is box 50. Month 1 has 30 boxes: 50 − 30 = 20. Today is month 2, box 20.',P),
 Paragraph(f'Sheet <b>HH</b> ({n("HH")}) runs backwards and its numbers count down: count boxes in printed order exactly as above, and read the number in the box you land on. '
   f'Sheet <b>FD</b> ({n("FD")}) runs three cycles a year: count through all 36 months in printed order.',P),
 Paragraph('4 · On every sheet',H2),
 Paragraph('Month 1 is at the top left, and the months run in order, three to a row. The <b>heavy box</b> in month 1 is the reference day, on average: a fixed point, printed for counting, '
   'with nothing expected of it. The last box of the final month is split: the short year ends top left, the long year bottom right.',P),
 Paragraph('5 · Keeping in step',H2),
 Paragraph('The sheets run on the count alone. From the year in progress, start every new year by the rule on page 2. Never adjust a sheet to anything outside the pack. '
   'If a sheet ever disagrees with the table, a day or a GG month was missed: count it again from the table.',P),
 Paragraph('6 · The record',H2),
 Paragraph('Use the journal page. Write the day first, in plain words, by the hour; fill in each cycle’s month and day <b>last</b>, from the calendars. Record what can be counted: events with their '
   'hour, counts, measures with a unit, ratings on a scale fixed once, and absences. Keep empty days: “nothing” is a result. Never change an old entry; add a dated correction.',P),
 Paragraph('7 · The study',H2),
 Paragraph('<b>Plan first.</b> Before the first entry, write down what you will count, which cycles you keep (all 36, or a list chosen now), which stages you compare, for how long, and what you '
   'would call a pattern. Date and sign it; give a copy to the key holder. <b>Count fairly.</b> Months differ in length, and so do the days you recorded in each: expect total × (days recorded in '
   'that month ÷ days recorded in all), not an equal share. 36 cycles of 12 months make 432 cells, and some will look striking by chance: decide in the plan which comparisons count, or find patterns '
   'in the first half of the record and test only those in the second. Slow cycles need years before every month has been seen. <b>Unseal last.</b> Run the plan as written, write the results down, '
   'including what found nothing, and only then open the key.',P),
 PageBreak()]
story+=[Paragraph('THE ROTATING NEW YEAR AND CORRECTIONS',T1),
 Paragraph('Keep the count from one line of the table: every year start, for every sheet.',SUB),
 Paragraph('8 · Working out the next year',H2),
 Paragraph('<b>a.</b> The table gives each sheet’s year in progress at printing: its number, the date it began and its start hour. Number the years on from there. '
   'A year here means one full turn of that sheet, not a calendar year: some last weeks, some decades.',P),
 Paragraph('<b>b.</b> Hours run 1 to 24 from 18:00. On slow sheets the date is the day 1 of the GG month that began box 1, one hour is a 24th of a GG month (about 29½ hours), and the year is counted in GG months.',P),
 Paragraph('<b>c.</b> Add the step to this year’s start hour. If this year’s number is a multiple of a tier’s interval (“every … yr”, counted in that sheet’s own years), '
   'add that tier’s hours as well. Every step and correction is built on the sheet’s own factor of 24.',P),
 Paragraph('<b>d.</b> If the total is <b>more than 24</b>, take away 24: this year is long and ends in the bottom right of the split box. Otherwise it is short. '
   'What is left is next year’s start hour. Next year’s start date is this year’s start date plus the length of this year, in days or in GG months. '
   '(Where two tiers fall in the same year, thousands of years from now, the total can still be more than 24: take away 24 again and add one more day.)',P),
 Paragraph(ex,P),
 Paragraph(f'<b>EB ({n("EB")})</b> gains almost a whole day every year, so its step is a full 24 hours: every year is long and begins in the same hour, '
   f'except every {ordn(byc["EB"]["des"]["tiers"][0][0])} year, when the tier takes the 24 hours back and the year is short.',P),
 Paragraph('9 · The table',H2)]
rows=[]
def num(x): return f'{x:,}'.replace(',',' ')
for s in S:
    d=s['des']; sl=s['slow']
    y_,d_,h_=in_progress(s['code']); date=f"<b>{y_}</b> · "+('GG ' if sl else '')+f"{fmt_date(d_)} · {h_}"
    tiers=[f"{num(N)} yr: {c:+d} h".replace("-","−") for N,c in d['tiers']]+['—']*3
    rows.append([str(s['no']),f"<b>{s['code']}</b>",date,f"{d['d']} / {d['d']+1}"+(' GG' if sl else ''),f"+{d['s']} h",str(d['factor']),*tiers[:3]])
widths=[18,34,120,62,30,30,70,80,95]
data=[[Paragraph(x,TH2) for x in ['No','Sheet','Year in progress: no. · began · hour','Short / long','Step','Factor','Tier 1','Tier 2','Tier 3']]]+[[Paragraph(x.replace(' ',' ') if i in (0,2,3,4) else x,TC2) for i,x in enumerate(r)] for r in rows]
t=Table(data,colWidths=widths,repeatRows=1)
t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('LINEBELOW',(0,1),(-1,-1),0.2,colors.grey),
  ('LINEBELOW',(0,8),(-1,8),0.8,colors.black),('TOPPADDING',(0,0),(-1,-1),1.0),('BOTTOMPADDING',(0,0),(-1,-1),1.0),('LEFTPADDING',(0,0),(-1,-1),1.5),('RIGHTPADDING',(0,0),(-1,-1),1.5)]))
story+=[t,Spacer(1,4),Paragraph(f'Year in progress on {PRINT.day} Nov {PRINT.year}. GG: the GG month that began box 1 of a slow sheet. Tiers are counted in the sheet’s own years.',SM),PageBreak()]

# ---- page 3: the sealed key (the only page that names what the codes are)
KT=ParagraphStyle('kt',fontName='DejaVuSans-Bold',fontSize=13,leading=16)
NAMES={'A':'Saturn','B':'Jupiter','C':'Mars','D':'the Sun','E':'Venus','F':'Mercury','G':'the Moon','H':'the lunar Nodes (mean North Node, moving backwards)'}
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
EX={'D':19,'G':33,'C':298,'F':165,'B':105,'E':357,'A':201,'H':63}
def degsign(x):
    dd=x%30; half=abs(dd-int(dd)-0.5)<1e-9
    return (f'{int(dd) or ""}½°' if half else f'{int(dd)}°')+' '+SIGNS[int(x//30)]
codes=Table([[Paragraph('<b>Code</b>',TH),Paragraph('<b>Cycle</b>',TH),Paragraph('<b>Start point (year 1, month 1)</b>',TH),Paragraph('<b>Reference day</b>',TH)]]+
  [[Paragraph(f'<b>{b}{b}</b>',TC),Paragraph(NAMES[b],TC),Paragraph({'D':'the March equinox','G':'the New Moon with the Sun in Taurus','H':'the mean North Node entering Gemini, backwards'}.get(b,f'{NAMES[b]} entering {SIGNS[EX[b]//30]}, heliocentric'),TC),
    Paragraph(f'{degsign(EX[b])}, the exaltation',TC)] for b in E.ORDER],colWidths=[40,120,226,FW-386])
codes.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('LINEBELOW',(0,1),(-1,-1),0.2,colors.grey),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
sect=Table([[Paragraph(f'<b>{E.LETTERS[i]}</b> {SIGNS[i]}',TC) for i in range(6)],[Paragraph(f'<b>{E.LETTERS[i]}</b> {SIGNS[i]}',TC) for i in range(6,12)]],colWidths=[FW/6]*6)
mk=[]
for s_ in S:
    if s_['code'][0]==s_['code'][1]: continue
    mk.append(f"<b>{s_['code']}</b> {degsign(E.midpoint(s_['code']))}")
pairs=Table([[Paragraph(x,TC2) for x in mk[i::7]] for i in range(7)],colWidths=[FW/4]*4)
pairs.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),0.6),('BOTTOMPADDING',(0,0),(-1,-1),0.6),('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,colors.Color(0.95,0.95,0.95)])]))
story+=[Paragraph('✂ · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·',SM),
 Paragraph('SEALED KEY · open only when the analysis is written down',KT),
 Paragraph('Holder: ______________________   Sealed on: ______________   Opened on: ______________   Plan dated: ______________',SUB),
 Paragraph('What the codes stand for',H2),
 Paragraph('The 36 calendars are the mean cycles of the seven traditional planets and the lunar Nodes, singly and in pairs. Letters A–G run from the slowest planet to the fastest; H is the Nodes.',P),codes,
 Paragraph('What the sectors stand for',H2),
 Paragraph('a–l are the twelve signs of the tropical zodiac, 30° each from the March equinox:',P),sect,
 Paragraph('Joint cycles',H2),
 Paragraph('A joint cycle is the conjunction cycle of the pair (Moon–Mercury and Moon–Venus as seen from Earth, counted in lunations; FD from Mercury’s superior conjunction). Its months are houses: '
   'the first body in the nth house of the second, 30° of separation each (on the G pairs, one whole conjunction cycle). Year 1 began at a conjunction in the sign of the pair’s mutual exaltation, '
   'and the reference day is the midpoint of the two exaltation degrees:',P),pairs,
 Paragraph('The blank journal column',H2),
 Paragraph('The narrow blank column on the journal page is the planetary hour. Hour 13 (06:00) belongs to the ruler of the weekday (Sunday the Sun, Monday the Moon, Tuesday Mars, Wednesday Mercury, '
   'Thursday Jupiter, Friday Venus, Saturday Saturn); each later hour takes the next in the order Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, and repeats. Hours 1–12 continue the previous day’s sequence.',P),
 Paragraph('Why it was sealed',H2),
 Paragraph('This edition exists to test traditional astrological claims without letting them shape the record. The calendars are identical, day for day, to those of the standard edition, '
   'so a result found here can be compared directly with the traditional reading of the same cycles.',P)]

doc=SimpleDocTemplate(sys.argv[1],pagesize=A4,leftMargin=M,rightMargin=M,topMargin=M-6,bottomMargin=M,title='Calibrating the 36 cycles · Empirical Edition',author='Aidan John Walsh')
doc.build(story,onFirstPage=page_deco,onLaterPages=page_deco)
