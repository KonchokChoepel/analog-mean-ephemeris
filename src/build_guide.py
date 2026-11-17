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
LIC='© 2026 Aidan John Walsh · CC BY-SA 4.0 · github.com/KonchokChoepel/analog-mean-ephemeris'
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
ex=(f"<b>Example, the Sun ({sun['no']}).</b> Year {Y0} began {fmt_date(d1)}, hour {H1}. {H1} + {des['s']} = {H1+des['s']}, "
    f"{'more than 24' if long1 else 'not more than 24'}{', and '+str(H1+des['s'])+' − 24 = '+str(H2_) if long1 else ''}, so year {Y0} is {'long' if long1 else 'short'} ({des['d']+long1} days): "
    f"year {Y0+1} begins {fmt_date(d2)} in hour {H2_}. {H2_} + {des['s']} = {H2_+des['s']}, {'more than 24' if long2 else 'not more than 24'}, "
    f"so year {Y0+1} is {'long' if long2 else 'short'} ({des['d']+long2} days){', and '+str(H2_+des['s'])+' − 24 = '+str(H3) if long2 else ''}: "
    f"year {Y0+2} begins {fmt_date(d3)} in hour {H3}. In year {des['tiers'][0][0]} the Sun's tier {'adds' if des['tiers'][0][1]>0 else 'takes away'} {abs(des['tiers'][0][1])} h as well.")

def page_deco(c,doc):
    c.setFont('DejaVuSans',6); c.drawCentredString(W/2,M-12,LIC)

story=[Paragraph('CALIBRATING THE 36 CALENDARS',T1),
 Paragraph('Set each sheet once by counting from the table on page 2, then cross off one box a day. An ephemeris is only for checking.',SUB),
 Paragraph('1 · The day',H2),
 Paragraph('A day begins at <b>18:00 by your own clock</b>, wherever you are, and takes the date of the day it ends in. '
   'Hours are numbered <b>1 to 24</b>: hour 1 begins at 18:00, hour 13 at 06:00. Every evening at 18:00, cross off one box on every daily sheet. '
   f'The six <b>slow sheets</b> (marked “1 box = 1 New Moon”) move on one box at each New Moon: the 1st of every month on the Moon sheet ({n("GG")}).',P),
 Paragraph('2 · What you need',H2),
 Paragraph('To set the sheets, the table on page 2. To check them, an ephemeris with <b>ordinary</b> and <b>heliocentric</b> positions and the <b>mean North Node</b>, tropical (astro.com has all three; times in UT).',P),
 Paragraph('3 · Setting any sheet',H2),
 Paragraph('<b>a.</b> Find the sheet’s row in the table on page 2. Its <b>year in progress</b> began on the date given there: that day is box 1 of month 1. '
   'If that year has already ended by today, work out the next year’s start with the rule on page 2 (section 8) and use that.',P),
 Paragraph('<b>b.</b> Count the days that have passed from the start date to today. Today’s box in the year is that number <b>plus 1</b>.',P),
 Paragraph('<b>c.</b> Take away the month lengths printed in the headings (1st month, then 2nd, and so on) until what is left is no bigger than the next month. '
   'That month is today’s month, and what is left is today’s box in it. Cross off every box before it.',P),
 Paragraph('<b>Slow sheets:</b> in b, count the New Moons that have passed since the start date instead of days. Today’s box is that number plus 1; carry on with c.',P),
 Paragraph('<i>Example.</i> Start date 3 March, today 21 April: 49 days have passed, so today is box 50. Month 1 has 30 boxes: 50 − 30 = 20. Today is month 2, box 20.',P),
 Paragraph(f'The <b>Nodes</b> sheet ({n("HH")}) moves backwards and its numbers count down: count boxes in printed order exactly as above, and read the number in the box you land on. '
   f'The <b>Mercury–Sun</b> year ({n("FD")}) runs three cycles: count through all 36 houses in printed order.',P),
]
def tbl(rows,widths,head):
    data=[[Paragraph(x,TH) for x in head]]+[[Paragraph(x,TC) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('LINEBELOW',(0,1),(-1,-1),0.25,colors.grey),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),1.6),('BOTTOMPADDING',(0,0),(-1,-1),1.6),('LEFTPADDING',(0,0),(-1,-1),2)]))
    return t
FW=W-2*M
singles=[[nm('GG'),'New Moon with the Sun in Taurus','ordinary'],
 [nm('FF'),'Mercury enters Virgo','heliocentric'],[nm('EE'),'Venus enters Pisces','heliocentric'],
 [nm('DD'),'March equinox: the Sun reaches 0° Aries','ordinary'],[nm('CC'),'Mars enters Capricorn','heliocentric'],
 [nm('BB'),'Jupiter enters Cancer','heliocentric'],[nm('AA'),'Saturn enters Libra','heliocentric'],
 [nm('HH'),'Mean North Node enters Gemini, moving backwards from 0° Cancer','mean node']]
story+=[Paragraph('4 · What day 1 marks, to check against the sky: single bodies',H2),tbl(singles,[FW*0.24,FW*0.56,FW*0.2],['Sheet','Day 1 of each year marks','Read from']),
 Paragraph('Use heliocentric positions for the five planets: an ordinary ephemeris shows them stopping and going backwards, which would give false ingresses.',SM)]
pairs=[[f"☽ Moon with ♂ ♃ ♄ ({n('GC')}–{n('GA')})",'the Moon meets the planet as seen from Earth, moved back by the ☽ figure in force that day on the Sun–planet sheet','ordinary, both'],
 [f"☽ Moon with ☿ ♀ ({n('GF')}, {n('GE')})",'<b>the New Moon</b> of the month in which the Moon meets the planet as seen from Earth','ordinary, both'],
 [nm('GD'),'New Moon','ordinary'],[nm('GH'),'the Moon reaches the mean North Node','ordinary'],
 [f"☿ ♀ ♂ ♃ ♄ with the ☉ Sun ({n('FD')}, {n('ED')}, {n('DC')}–{n('DA')})",'the Sun’s ordinary position equals the planet’s heliocentric position (Mercury, Venus: superior conjunction, behind the Sun)','Sun ordinary, planet heliocentric'],
 [nm('DH'),'the Sun reaches the mean North Node','ordinary'],
 [f"Two planets ({n('FE')}, {n('FC')}–{n('FA')}, {n('EC')}–{n('EA')}, {n('CB')}, {n('CA')}, {n('BA')})",'both planets at the same heliocentric position','heliocentric'],
 [f"A planet with the ☊ Nodes ({n('FH')}, {n('EH')}, {n('CH')}, {n('BH')}, {n('AH')})",'the planet’s heliocentric position reaches the mean North Node','planet heliocentric, mean node']]
mk=[]
for s_ in S:
    if s_['code'][0]==s_['code'][1]: continue
    sg=int(E.midpoint(s_['code'])//30); mk.append(f"<b>{s_['no']}</b> {s_['glyphs']} {E.SIGN_GLYPH[sg]} {E.SIGNS[sg]}")
cols=4; rows_=[mk[i::7] for i in range(7)]
mt=Table([[Paragraph(x,TC2) for x in r] for r in rows_],colWidths=[FW/cols]*cols)
mt.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),0.6),('BOTTOMPADDING',(0,0),(-1,-1),0.6),('LEFTPADDING',(0,0),(-1,-1),2),('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,colors.Color(0.95,0.95,0.95)])]))
story+=[Paragraph('5 · What day 1 marks: pairs (a conjunction; Year 1’s fell in the year-marker sign)',H2),tbl(pairs,[FW*0.30,FW*0.48,FW*0.22],['Sheets','The conjunction is the day…','Read from']),
 Paragraph('Every pair’s Year 1 began at a conjunction in the sign of its <b>mutual exaltation</b>, the midpoint of the two exaltations, as the Moon’s begins at the New Moon in Taurus:',SM),mt,
 Paragraph(f'<b>In the sky.</b> Sun: the Sun sheet’s month is its sign, day − 1 ≈ degree. Moon: 12° east of the Sun per day since the 1st of Moon–Sun ({n("GD")}). Planets: the Sun’s degree ± the figure bottom left of the day’s box on its Sun–planet sheet ({n("FD")}, {n("ED")}, {n("DC")}, {n("DB")}, {n("DA")}): '
 f'E evening sky, W morning, 180 opposition, under about 12 lost in the Sun’s glare. The Moon meets a planet on the 1st of its Moon–planet month, moved by the ☽ figure in force that day: the last one printed, which holds until the next. ◐ on Sun–Nodes ({n("DH")}): eclipse seasons.',SM),
 Paragraph('6 · Keeping in step',H2),
 Paragraph('The sheets run on the count, not on the sky. From the year in progress, start every new year by the rule on page 2. To check a sheet, look up its day 1 event in an ephemeris: '
   'it should fall within the orb listed for that sheet, ahead or behind. That is expected, and the sky swings both ways round the count over time: never reset a sheet to the sky, or its offset is kept for good. '
   'If a sheet is ever out by more than its orb, a day or a New Moon was missed: count it again from the table.',P),
 Paragraph('7 · On every sheet',H2),
 Paragraph('Month 1 is at the top left, and the months run in order, three to a row. A single body’s months are named for the sign it is transiting. '
   'On a pair sheet the months are the houses of the slower body that the faster one is transiting; the small sign beside each house counts from the sign of the midpoint of the two exaltations in house 1: '
   'a fixed label, not where the pair stands. On a Moon pair the pair meets on the 1st of every month. '
   'The <b>heavy box</b> in month 1 is the whole day in which the body reaches its exaltation degree, on average (on a pair sheet, the midpoint of the two exaltations). '
   'The last box of month 12 is split: the short year ends top left, the long year bottom right.',P),
 Paragraph('Starting out',H2),
 Paragraph(f'Begin with three sheets for a month: the Sun ({n("DD")}), the Moon ({n("GG")}) and Moon–Sun ({n("GD")}). Then add the sheets of one almanac, the body you most want to watch. '
   '<b>Journal first, sheets second:</b> write the day’s events before you look at the sheets, then fill in the month and day of each body. The record stays honest that way.',P),
 PageBreak()]

# ---- page 2
story+=[Paragraph('THE ROTATING NEW YEAR AND CORRECTIONS',T1),
 Paragraph('Keep the count without an ephemeris: every year start, for every sheet, from one line of the table.',SUB),
 Paragraph('8 · Working out the next year',H2),
 Paragraph('<b>a.</b> The table gives each sheet’s year in progress at printing: its number, the date it began and its start hour. Number the years on from there. '
   'A year here means one full turn of that sheet, not a calendar year: Mercury’s years are about 88 days, Saturn’s nearly 30 calendar years.',P),
 Paragraph('<b>b.</b> Hours run 1 to 24 from 18:00. On slow sheets the date is the New Moon that began box 1, one hour is a 24th of a lunation (about 29½ hours), and the year is counted in New Moons.',P),
 Paragraph('<b>c.</b> Add the step to this year’s start hour. If this year’s number is a multiple of a tier’s interval (“every … yr”, counted in that sheet’s own years), '
   'add that tier’s hours as well. Every step and correction is built on the sheet’s own factor of 24.',P),
 Paragraph('<b>d.</b> If the total is <b>more than 24</b>, take away 24: this year is long and ends in the bottom right of the split box. Otherwise it is short. '
   'What is left is next year’s start hour. Next year’s start date is this year’s start date plus the length of this year, in days or in New Moons. '
   '(Where two tiers fall in the same year, thousands of years from now, the total can still be more than 24: take away 24 again and add one more day.)',P),
 Paragraph(ex,P),
 Paragraph(f'<b>Venus–Jupiter ({n("EB")})</b> gains almost a whole day every year, so its step is a full 24 hours: every year is long and begins in the same hour, '
   f'except every {ordn(byc["EB"]["des"]["tiers"][0][0])} year, when the tier takes the 24 hours back and the year is short.',P),
 Paragraph('9 · The table',H2)]
rows=[]
def num(x): return f'{x:,}'.replace(',',' ')
for s in S:
    d=s['des']; st=s['start']; sl=s['slow']
    y_,d_,h_=in_progress(s['code']); date=f"<b>{y_}</b> · "+('NM ' if sl else '')+f"{fmt_date(d_)} · {h_}"
    tiers=[f"{num(N)} yr: {c:+d} h".replace("-","−") for N,c in d['tiers']]+['—']*3
    rows.append([str(s['no']),f"{s['glyphs']} {s['title'].upper()}",date,f"{d['d']} / {d['d']+1}"+(' NM' if sl else ''),
                 f"+{d['s']} h",str(d['factor']),f"{s['orb']:.0f} d" if s['orb']>=1.5 else '1 d',*tiers[:3]])
widths=[15,82,96,50,25,24,24,60,70,93]
data=[[Paragraph(x,TH2) for x in ['No','Sheet','Year in progress: no. · began · hour','Short / long','Step','Factor','Orb ±','Tier 1','Tier 2','Tier 3']]]+[[Paragraph(x.replace(' ','\u00a0') if i in (0,2,3,4,6) else x,TC2) for i,x in enumerate(r)] for r in rows]
t=Table(data,colWidths=widths,repeatRows=1)
t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('LINEBELOW',(0,1),(-1,-1),0.2,colors.grey),
  ('LINEBELOW',(0,8),(-1,8),0.8,colors.black),('TOPPADDING',(0,0),(-1,-1),1.0),('BOTTOMPADDING',(0,0),(-1,-1),1.0),('LEFTPADDING',(0,0),(-1,-1),1.5),('RIGHTPADDING',(0,0),(-1,-1),1.5)]))
story+=[t,Spacer(1,4),Paragraph(f'Year in progress on {PRINT.day} Nov {PRINT.year}. NM: the New Moon that began box 1 of a slow sheet. Orb: how far the sky may run ahead of or behind the sheet. '
  'Tiers are counted in the sheet’s own years.',SM)]
doc=SimpleDocTemplate(sys.argv[1],pagesize=A4,leftMargin=M,rightMargin=M,topMargin=M-6,bottomMargin=M,title='Calibrating the 36 calendars',author='Aidan John Walsh')
doc.build(story,onFirstPage=page_deco,onLaterPages=page_deco)
