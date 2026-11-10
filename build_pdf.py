import sys; sys.path.insert(0,'.')
from data import *
from solar import solar_of, MONS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import os
FD=os.environ.get('DEJAVU_DIR','/usr/share/fonts/truetype/dejavu/')
for n,f in (('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVC','DejaVuSansCondensed.ttf'),('DVCB','DejaVuSansCondensed-Bold.ttf'),('DVI','DejaVuSans-Oblique.ttf')):
    pdfmetrics.registerFont(TTFont(n,FD+f))
W,H=A4; M=30
NAVY=HexColor('#1F3864'); GREY=HexColor('#595959'); LG=HexColor('#E7E6E6'); LB=HexColor('#D9E1F2'); YEL=HexColor('#FFF2CC'); RULE=HexColor('#BFBFBF')
FOLV=4887
def sty(size=8,font='DVC',lead=None,color=black): return ParagraphStyle('x',fontName=font,fontSize=size,leading=lead or size*1.28,textColor=color)
def para(c,text,x,ytop,w,style):
    p=Paragraph(text,style); pw,ph=p.wrap(w,1000); p.drawOn(c,x,ytop-ph); return ph
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def sign_deg(deg): return f"{int(deg%30)}° {SIGNS[int(deg//30)]}"
def names(X):
    bs=X['bs']
    return [NAMES[b] for b in bs]
def title_of(X):
    code=X['code']; bs=X['bs']
    if len(bs)==1: return f"{GLYPH[bs[0]]} {NAMES[bs[0]].upper()}", TITLES[code]
    a,b=bs
    return f"{GLYPH[a]}{GLYPH[b]}  {NAMES[a].upper()} – {NAMES[b].upper()}", "Conjunction cycle"
def desc_of(X):
    code=X['code']; bs=X['bs']; slow=X['slow']; d=X['des']['d']
    if code=='DD': t="New year: the Sun reaches 0° Aries (the March equinox). The 12 months are 12 arcs of 30° of the Sun's true position, so they are long where it moves slowly and short where it moves fast."
    elif code=='GG': t="New year: the regular-pace New Moon in Taurus, where the Moon is exalted. A year is 12 lunations (12 New Moons), about 354 days; each month is one lunation, named by the sign of its New Moon. Each year the New Moon falls about 11° earlier in the zodiac."
    elif code=='HI': t="New year: the mean Node reaches 3° Gemini. One year is one full turn of the Nodes (about 18.6 real years), split into 12 near-equal months."
    elif len(bs)==1:
        deg=EXALT[bs[0]]; t=f"New year: {NAMES[bs[0]]} reaches {sign_deg(deg)} (its exaltation). The 12 months are 12 arcs of 30° of its true position, so they are long where it moves slowly and short where it moves fast."
    elif X['moonpair']:
        a,b=bs; mid=midpoint_sign(code)[1]; other=NAMES[[x for x in bs if x!='G'][0]] if code!='HGI' else 'Nodes'
        t=f"New year: a regular-pace conjunction of the Moon and {other}. A year is <b>12 conjunctions</b>, so each month is one full cycle from conjunction to conjunction and the Moon is conjunct {other} on the 1st of every month. Month names run on from {SIGNS[X['first']]}, the sign of the midpoint of the two exaltations ({sign_deg(mid)})."
    else:
        a,b=bs; mid=midpoint_sign(code)[1]; F=NAMES[X['fast']]; S=NAMES[X['slowb']]
        t=f"New year: the regular-pace conjunction of {NAMES[a]} and {NAMES[b]} (both at the same position). A year is one conjunction cycle. <b>Each month is a house</b>: {F}, the faster, moves through the houses of {S}, the slower, 30° at a time from the conjunction (month 1 = {F} in the 1st house of {S})."
        if X['back']: t+=f" The Nodes move backward, so their houses are counted backward."
        t+=f" Month names run on from {SIGNS[X['first']]}, the sign of the midpoint of the two exaltations ({sign_deg(mid)})."
    if slow: t+=" <b>On this calendar one day = 30 real days and one hour = 1¼ real days.</b>"
    return t
def draw_cal(c,X,npage):
    code=X['code']; des=X['des']; d=des['d']; slow=X['slow']
    # header band
    c.setFillColor(NAVY); c.rect(M,H-M-48,W-2*M,48,stroke=0,fill=1)
    t1,t2=title_of(X)
    c.setFillColor(white); c.setFont('DVB',9); c.drawString(M+10,H-M-14,f"CALENDAR {X['no']} OF 36")
    c.setFont('DVB',18); c.drawString(M+10,H-M-34,t1)
    c.setFont('DV',9); c.drawString(M+10,H-M-45,t2)
    c.setFont('DVB',26); c.drawRightString(W-M-10,H-M-28,code)
    g0=X['grid'][0]
    c.setFont('DVC',8); c.drawRightString(W-M-10,H-M-42,f"Year 1 begins {fmt(g0['date'])}  ·  Solar {solar_of(g0['date'])[0]}, {solar_of(g0['date'])[2]} {MONS[solar_of(g0['date'])[1]]}")
    y=H-M-48-6
    ph=para(c,desc_of(X),M,y,W-2*M,sty(8))
    y-=ph+8
    # key boxes
    orb=X['orb_d']; boxes=[("YEAR LENGTH",f"{d} / {d+1}","short / long year, in days"),
        ("HOUR STEP",f"+{des['s']}",f"hours each year (fix {des['L']:+d} h, every {des['K']} yr)"),
        ("ORB",f"±{orb}","days, true vs regular pace"+(f" (≈ ±{max(1,round(orb/30))} mo.)" if slow else "")),
        ("ACCURACY",f"±{X['acc']}","day of the regular-pace cycle"+("s" if X['acc']>1 else "")),
        ("ONE DAY IS","30 days" if slow else "1 day","of real time")]
    bw=(W-2*M-4*6)/5; bh=40
    for i,(a,b,s) in enumerate(boxes):
        x=M+i*(bw+6); c.setFillColor(LB); c.setStrokeColor(RULE); c.rect(x,y-bh,bw,bh,stroke=1,fill=1)
        c.setFillColor(GREY); c.setFont('DVCB',6.5); c.drawCentredString(x+bw/2,y-9,a)
        c.setFillColor(black); c.setFont('DVB',14); c.drawCentredString(x+bw/2,y-24,b)
        c.setFillColor(GREY); 
        fs=6.2
        while pdfmetrics.stringWidth(s,'DVC',fs)>bw-6: fs-=0.2
        c.setFont('DVC',fs); c.drawCentredString(x+bw/2,y-35,s)
    y-=bh+10
    # month table
    ytab=y; cw=[30,68,28,56,78]; rh=14
    c.setFillColor(NAVY); c.setFont('DVB',8); c.drawString(M,ytab-8,"MONTHS")
    ytab-=12
    hdrs=['House' if X['houses'] else 'Mo','Month','Days','Day nos.','Starts, year 1']
    x=M; c.setFillColor(LB); c.rect(M,ytab-rh,sum(cw),rh,stroke=0,fill=1)
    c.setFillColor(black); c.setFont('DVCB',7.5)
    for hname,w in zip(hdrs,cw): c.drawCentredString(x+w/2,ytab-10,hname); x+=w
    ytab-=rh
    for k,(m,(a,b,dd)) in enumerate(zip(X['months'],X['mrows'])):
        if k%2: c.setFillColor(HexColor('#F7F7F7')); c.rect(M,ytab-rh,sum(cw),rh,stroke=0,fill=1)
        c.setFillColor(black); c.setFont('DVC',8)
        vals=[ordn(k+1) if X['houses'] else str(k+1),SIGNS[(X['first']+k)%12],str(m),f"{a}–{b}",fmt(dd)]
        x=M
        for j,(v,w) in enumerate(zip(vals,cw)):
            if j==1: c.drawString(x+4,ytab-10,v)
            else: c.drawCentredString(x+w/2,ytab-10,v)
            x+=w
        ytab-=rh
    # intercalary row
    c.setFillColor(YEL); c.rect(M,ytab-rh,sum(cw),rh,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVCB',7.5)
    c.drawCentredString(M+cw[0]/2,ytab-10,'+'); c.drawString(M+cw[0]+4,ytab-10,'Intercalary'); c.drawCentredString(M+cw[0]+cw[1]+cw[2]/2,ytab-10,'1')
    c.setFont('DVC',7); c.drawString(M+cw[0]+cw[1]+cw[2]+3,ytab-10,f"day {d+1}, long years only")
    ytab-=rh
    c.setStrokeColor(RULE); c.rect(M,ytab,sum(cw),12+rh*14-12+0,stroke=1,fill=0) if False else None
    c.rect(M,ytab,sum(cw),(y-12)-ytab,stroke=1,fill=0)
    # right column
    rx=M+sum(cw)+14; rw=W-M-rx; yr=y
    c.setFillColor(NAVY); c.setFont('DVB',8); c.drawString(rx,yr-8,"CORRECTIONS")
    yr-=12
    c.setFillColor(LB); c.rect(rx,yr-rh,rw,rh,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVCB',7.5)
    cws=[34,64,rw-98]; xx=rx
    for hname,w in zip(['Tier','Every','Move the new-year hour'],cws): c.drawCentredString(xx+w/2,yr-10,hname); xx+=w
    yr-=rh
    for i,t in enumerate(des['tiers']):
        c.setFillColor(black); c.setFont('DVC',8); xx=rx
        if t:
            sym=t[2]<0.5
            n=f"{t[0]:,} yr" if t[0]<10**8 else "never (symbolic)"
            move=("forward " if t[1]>0 else "back ")+str(abs(t[1]))+" hours"
            if sym: move+=" (symbolic)"
            vals=[str(i+1),n,move]
        else: vals=[str(i+1),'—','none needed']
        for j,(v,w) in enumerate(zip(vals,cws)):
            if j==2: c.drawString(xx+4,yr-10,v)
            else: c.drawCentredString(xx+w/2,yr-10,v)
            xx+=w
        yr-=rh
    c.setStrokeColor(RULE); c.rect(rx,yr,rw,rh*4,stroke=1,fill=0)
    yr-=8
    howto=(f"<b>How to use.</b> 1) Find the year in the grid: the big number is how many days it has, the small number is the hour its new year begins. "
           f"2) Count the days through the 12 months. A year longer than {d} days adds the Intercalary Day after month 12; a year shorter than {d} days loses the last day of month 12. "
           f"<br/><b>To go beyond year 100.</b> Each year add {des['s']} to the hour. In a correction year (▲) also move it as the table says. "
           f"If the hour reaches 24 or more, subtract 24 and give that year one extra day. If it drops below 0, add 24 and take a day off.")
    para(c,howto,rx,yr,rw,sty(7.4,'DVC',9.3))
    y=min(ytab,yr)-8
    # grid
    y=ytab-12
    c.setFillColor(NAVY); c.setFont('DVB',8); c.drawString(M,y-8,"100-YEAR LOOKUP  (big number = days in the year · small number = new-year hour)")
    y-=12
    hw=88; cwid=(W-2*M-hw)/10; rh2=33
    c.setFillColor(LB); c.rect(M,y-14,W-2*M,14,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVCB',7.5)
    c.drawCentredString(M+hw/2,y-10,'Years')
    for j in range(10): c.drawCentredString(M+hw+cwid*j+cwid/2,y-10,str(j+1))
    y-=14
    G=X['grid']
    for r in range(10):
        yb=y-rh2*(r+1)
        g0=G[r*10]; 
        c.setFillColor(black); c.setFont('DVCB',7.5); c.drawString(M+4,yb+rh2-10,f"{r*10+1}–{r*10+10}")
        c.setFont('DVC',6.6); c.drawString(M+4,yb+rh2-20,fmt(g0['date'])); c.setFillColor(GREY); c.drawString(M+4,yb+rh2-30,f"Solar {solar_of(g0['date'])[0]} · {solar_of(g0['date'])[2]} {MONS[solar_of(g0['date'])[1]][:3]}")
        for j in range(10):
            g=G[r*10+j]; xc=M+hw+cwid*j
            long_=g['len']>d; odd=(g['len']<d or g['len']>d+1)
            if odd: c.setFillColor(HexColor('#F8CBAD'))
            elif long_: c.setFillColor(HexColor('#D9D9D9'))
            else: c.setFillColor(white)
            c.rect(xc,yb,cwid,rh2,stroke=0,fill=1)
            c.setFillColor(black); c.setFont('DVB',10); c.drawCentredString(xc+cwid/2,yb+rh2-16,str(g["len"]))
            c.setFont('DVC',7); c.setFillColor(GREY); c.drawCentredString(xc+cwid/2,yb+5,f"{g['hr']:02d}h")
            if g['fired']:
                c.setFillColor(black); c.setFont('DV',6); c.drawString(xc+2,yb+rh2-9,'▲'+(''.join(str(i) for i in g['fired']) if g['fired']!=[1] else ''))
    # grid lines
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    ytop=y; ybot=y-rh2*10
    for r in range(11): c.line(M,y-rh2*r,W-M,y-rh2*r)
    for j in range(11): c.line(M+hw+cwid*j,ytop,M+hw+cwid*j,ybot)
    c.line(M,ytop,M,ybot); c.line(M+hw,ytop+14,M+hw,ybot)
    c.setLineWidth(0.5); c.rect(M,ybot,W-2*M,ytop-ybot+14,stroke=1,fill=0)
    yl=ybot-10
    c.setFont('DVC',7); c.setFillColor(GREY)
    c.drawString(M,yl,f"Grey cell = long year ({d+1} days, with the Intercalary Day).  ▲ = correction year (▲12 = tiers 1+2 together: apply both).  Hour = {'1/24 of a calendar day' if slow else 'hour from 18:00 UTC (0 = 18:00 UTC), 0–23'}.")
    if slow: c.drawString(M,yl-9,"Dates are approximate (to about 30 days): one calendar day on this page is 30 real days.")
    c.drawString(M,M-8,f"Regular-pace (mean-motion) calendar · epoch: Saturn–Neptune conjunction, 8 Dec 2025 · days begin 18:00 UTC, dated by the day they end in")
    c.drawRightString(W-M,M-8,f"page {npage}")
    c.showPage()
def draw_howto(c):
    c.setFillColor(NAVY); c.rect(M,H-M-48,W-2*M,48,stroke=0,fill=1); c.setFillColor(white)
    c.setFont('DVB',20); c.drawString(M+10,H-M-30,"36 CALENDARS"); c.setFont('DV',9); c.drawString(M+10,H-M-43,"Hand-reckoning pack · regular-pace planetary time in whole numbers")
    y=H-M-60; S=sty(9,'DV',12.5); B=sty(9.6,'DVB',13)
    blocks=[
    ("What this is","Each page is one calendar. It counts time in whole days only. The calendar follows a planet, or a pair of planets, at the regular pace they keep on average. Real events never happen exactly on time; the gap between the regular-pace date and the observed one is the planet's <b>orb</b>, printed on each page. The calendar marks the <i>floating centre</i> in time; the real event floats around it."),
    ("Reading a page","Every page has the same parts. <b>Months</b>: twelve of them, with whole-day lengths and the first and last day number of each. On pair calendars the months are the twelve houses (1st to 12th). <b>Year length</b>: a short year and a long year; the long one has the Intercalary Day after month 12. <b>Hour step</b> and <b>Corrections</b>: the rules that keep the calendar true. <b>100-year lookup</b>: all of it already worked out for you."),
    ("The new-year hour","<b>Every day begins at 18:00 UTC</b>, so hour 0 is 18:00 UTC and each day carries the Gregorian date of the day it ends in. A year does not have to begin at hour 0. It begins at some hour. Every year, that hour moves forward by the <b>hour step</b>. When the hour passes 24 it starts again at 0 and that year had one extra day: the Intercalary Day. That is the whole leap system. Where the printed hour step is large, it is the same as turning the clock back and adding a day."),
    ("Corrections: tiers 1, 2 and 3","The orbit is never an exact number of whole hours. So in certain years the new-year hour is nudged forward or back, by the same number of hours each time. <b>Tier 1</b> fixes the largest slip and comes round soonest. <b>Tier 2</b> fixes what Tier 1 leaves behind. <b>Tier 3</b> is nearly symbolic: it is smaller than anything we can measure today, and is left for future people to adjust as they learn more. Only the correction years inside the 100-year lookup are marked ▲; the tables tell you the rest."),
    ("Orb","The orb is the largest gap, in whole days, between the regular-pace position and where the planet really is (for pairs: when the real conjunction happens). It comes from the shape of the orbits. Treat the calendar date as the middle of a window, plus and minus the orb."),
    ("Slow calendars","Six calendars follow cycles of thousands of days (Jupiter, Saturn, the Nodes and three pairs). On these, one calendar day = 30 real days and one hour = 1¼ real days. Everything is still whole numbers; the page says so at the top."),
    ("Where it starts","Year 1 on every page is the calendar year in progress at the epoch, the Saturn–Neptune conjunction of 8 December 2025. For the Sun that year began on the March 2025 equinox (Folvasin year 6912). <b>Only the Sun calendar (No. 1) fixes the year.</b> The count of years begins with <b>Year 0, the year dot</b>, attached to the March equinox of 4888 BCE (symbolically, the dawn of civilisation); Year 1 begins at the March equinox of 4887 BCE, and Year 6912 is the year that began at the March 2025 equinox. Every start date in this pack is therefore also given as a Solar date (Solar year, day and sign-month of the Sun calendar), so a cycle that starts in March before the equinox belongs to the previous Solar year. For planets, a year begins when the planet reaches its exaltation degree; for the Sun, at 0° Aries. For pairs, a year begins at the regular-pace conjunction. The Moon calendar (No. 2) begins at the regular-pace New Moon in Taurus, the Moon's exaltation sign, and runs 12 lunations."),
    ("Houses","On every pair calendar except the Moon's, the faster planet moves through the houses of the slower one. (On the Moon's pairs each month is one full conjunction cycle, 12 per year.) House 1 starts at their conjunction and each house is 30° of separation, so month n is house n. The Nodes move backward; in the one pair where they are the faster body (Nodes–Saturn) the houses are counted backward."),
    ("Worked example","Sun, year 3. In the lookup, year 3 shows 366 and 21h. So the year has 366 days (the Intercalary Day is included) and its new year begins at hour 21, on 20 March 2027. Year 4 shows 365 and 03h: add 6 to 21, get 27, subtract 24, and that year was one day longer. Year 32 would also carry a correction mark: move the hour back 6 hours.")]
    for h,t in blocks:
        y-=4; ph=para(c,h.upper(),M,y,W-2*M,sty(9,'DVB',12,NAVY)); y-=ph+1
        ph=para(c,t,M,y,W-2*M,S); y-=ph+6
    c.setFont('DVC',7); c.setFillColor(GREY)
    c.drawString(M,M-8,"Model: JPL mean elements (Standish 1800–2050) for phases and eccentricity; periods from the 36 Calendars sheet. Dates are not DE440-checked.")
    c.showPage()
def draw_index(c,Xs):
    c.setFillColor(NAVY); c.rect(M,H-M-34,W-2*M,34,stroke=0,fill=1); c.setFillColor(white); c.setFont('DVB',14); c.drawString(M+10,H-M-23,"INDEX OF THE 36 CALENDARS")
    y=H-M-44; cw=[26,36,190,64,62,40,56]; rh=17
    hd=['No.','Code','Calendar','Year (days)','Hour step','Orb (d)','Year 1 starts']
    c.setFillColor(LB); c.rect(M,y-rh,sum(cw),rh,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVCB',8)
    x=M
    for h,w in zip(hd,cw): c.drawCentredString(x+w/2,y-11.5,h); x+=w
    y-=rh
    for i,X in enumerate(Xs):
        if i%2: c.setFillColor(HexColor('#F7F7F7')); c.rect(M,y-rh,sum(cw),rh,stroke=0,fill=1)
        t1,t2=title_of(X); nm=t1.title().replace('  ',' ') 
        bs=X['bs']; label=(NAMES[bs[0]] if len(bs)==1 else NAMES[bs[0]]+'–'+NAMES[bs[1]])
        if len(bs)==1: label+=' · '+TITLES[X['code']]
        vals=[str(X['no']),X['code'],label,f"{X['des']['d']} / {X['des']['d']+1}"+('*' if X['slow'] else ''),f"+{X['des']['s']} h",str(X['orb_d']),fmt(X['grid'][0]['date'])]
        c.setFillColor(black); x=M
        for j,(v,w) in enumerate(zip(vals,cw)):
            c.setFont('DVC',8)
            if j==2: c.drawString(x+4,y-11.5,v)
            else: c.drawCentredString(x+w/2,y-11.5,v)
            x+=w
        y-=rh
    c.setStrokeColor(RULE); c.rect(M,y,sum(cw),rh*37,stroke=1,fill=0)
    c.setFont('DVC',7.5); c.setFillColor(GREY)
    c.drawString(M,y-12,"* Slow calendar: days in units of 30 real days; hour = 1¼ real days. Orb is always in real days. Year-1 dates for slow calendars are the real date.")
    c.showPage()
if __name__=='__main__':
    Xs=[build(code) for no,code,Ps in CAL]
    out=sys.argv[1]
    c=canvas.Canvas(out,pagesize=A4); c.setTitle('36 Calendars - Hand Reckoning Pack'); c.setAuthor('Claude')
    draw_howto(c); draw_index(c,Xs)
    for i,X in enumerate(Xs): draw_cal(c,X,i+3)
    c.save(); print('ok',len(Xs))
