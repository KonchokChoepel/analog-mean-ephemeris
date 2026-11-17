"""A3 calendar fronts and backs."""
import datetime as dt, math
from reportlab.lib.pagesizes import A3, landscape
import engine2 as E, ledger as Lg
from a3_draw import *
W,H=landscape(A3); M=30
PRINT_DATE=dt.date(2026,11,14)
DF_FIRST=(2026,11); DF_MONTHS=24
MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def window():
    y,m=DF_FIRST; m2=m+DF_MONTHS-1; y2=y+(m2-1)//12; m2=(m2-1)%12+1
    return f'{MON[m-1]} {y} to {MON[m2-1]} {y2}'
def fmt(d,short=False): return f"{d.day} {MON[d.month-1]} {str(d.year)[2:] if short else d.year}"
def ordn(k): return f"{k}{'th' if 10<=k%100<=20 else {1:'st',2:'nd',3:'rd'}.get(k%10,'th')}"

def front(c,s):
    d=s['des']
    band(c,M,H-M,W-2*M,52,f"{s['glyphs']} {s['title'].upper()}".strip(),sheet_kind(s),f"CALENDAR {s['no']} OF 36  ·  A3 sheet, front",yl(s),s['code'],tsize=24)
    y=H-M-62
    h=para(c,intro(s),M,y,W-2*M,size=11); y-=h+15
    xx=fields_line(c,s,M,y,size=10.5); y-=18; checkboxes(c,s,M,y,size=10); y-=12
    foot=M+30
    draw_calendar(c,s,M,y,W-2*M,y-foot,3,hb=18,colgap=16,mingap=10)
    note=('Small number = day of the year (the number the back’s tables give you). The last box is split: top-left = last day of a SHORT year, bottom-right = last day of a LONG year '
          '(the Intercalary Day). Months run in order from month 1 (red title) at top left, three to a row. Fill the blanks from the back of this sheet.')
    if s['code']=='DD': note+=(' Sheet DD:' if E.EMP else ' Sun:')+' write the weekday names in the 7 header boxes (column 1 = weekday of day 1 of the year).'
    if s['slow']: note+=(' One box = one GG month: cross off a box on day 1 of every month of cycle GG.' if E.EMP else ' One box = one New Moon: cross off a box on the 1st of every month of the Moon sheet.')
    para(c,note,M,M+24,W-2*M,size=7.4)
    c.setFont('DejaVuSans',6.2); c.drawString(M,M-2,LIC)

def cell_text(s,L,date):
    y,box,m,dd,ic=L.locate(date)
    if s['code']=='HH':
        n=s['months'][m-1]; dd=0 if ic else n-dd+1
    return y,box,m,dd,ic

def date_finder(c,s,L,x,ytop,w,rh=13.2):
    cols=[]
    yy,mm=DF_FIRST
    for i in range(DF_MONTHS):
        cols.append((yy,mm)); mm+=1
        if mm>12: mm=1; yy+=1
    lw=20; cw=(w-lw)/DF_MONTHS; hh=22
    c.setFont('DejaVuSans-Bold',7.5)
    for j,(Y,Mo) in enumerate(cols):
        cx=x+lw+j*cw; c.drawCentredString(cx+cw/2,ytop-9,MON[Mo-1]); c.setFont('DejaVuSans',6); c.drawCentredString(cx+cw/2,ytop-18,str(Y)); c.setFont('DejaVuSans-Bold',7.5)
    top=ytop-hh
    for r in range(31):
        ry=top-(r+1)*rh
        c.setFont('DejaVuSans-Bold',7.5); c.drawCentredString(x+lw/2,ry+rh*0.3,str(r+1))
        for j,(Y,Mo) in enumerate(cols):
            cx=x+lw+j*cw
            try: date=dt.date(Y,Mo,r+1)
            except ValueError:
                fill(c,GREY); c.rect(cx,ry,cw,rh,stroke=0,fill=1); fill(c,(0,0,0)); continue
            y,box,m,dd,ic=cell_text(s,L,date)
            firstm=(L.locate(date)[3]==1) or (s['code']=='HH' and dd==s['months'][m-1] and not ic)
            firsty=box==1
            bg=RED1 if firsty else GOLDCELL if firstm else (BAND if y%2 else (1,1,1))
            fill(c,bg); c.rect(cx,ry,cw,rh,stroke=0,fill=1); fill(c,(0,0,0))
            t=f'{m}·{dd}'+('+' if ic else '')
            f='DejaVuSansCondensed-Bold' if (firstm or firsty) else 'DejaVuSansCondensed'
            fs=7.4 if len(t)<=5 else 6.6; c.setFont(f,fs); c.drawCentredString(cx+cw/2,ry+rh*0.28,t)
    c.setLineWidth(0.3); stroke(c,MIDGREY)
    for j in range(DF_MONTHS+1): c.line(x+lw+j*cw,top,x+lw+j*cw,top-31*rh)
    for r in range(32): c.line(x,top-r*rh,x+w,top-r*rh)
    stroke(c,(0,0,0)); c.setLineWidth(0.8); c.rect(x,top-31*rh,w,31*rh+hh)
    return hh+31*rh

def month_starts(c,s,L,x,ytop,w):
    y0=L.year_of(PRINT_DATE); d1=L.month_start_dates(y0); d2=L.month_start_dates(y0+1)
    fv=Lg.folvasin(L.start_date(y0))
    h=section(c,x,ytop,w,f'MONTH STARTS · year {y0} (Folv. {fv}) and the next'); y=ytop-h-12
    ms=s['months']
    if s['code']=='FD':
        c.setFont('DejaVuSans-Bold',7); hd=['Month' if E.EMP else 'House','Days',f'Y{y0} cycle 1','cycle 2','cycle 3',f'Y{y0+1} cycle 1','cycle 2','cycle 3']
        xs=[0,40,62,112,162,212,264,314]
        for t,xx in zip(hd,xs): c.drawString(x+xx,y,t)
        for k in range(12):
            yy=y-11-k*10.2
            if k%2==0: fill(c,BAND); c.rect(x,yy-2.5,w,10.2,stroke=0,fill=1); fill(c,(0,0,0))
            c.setFont('DejaVuSans',7); c.drawString(x,yy,f'{ordn(k+1)} {s["names"][k][1]}'); c.drawString(x+44,yy,str(ms[k]))
            for q in range(3):
                c.drawString(x+xs[2+q],yy,fmt(d1[q*12+k],True)); c.drawString(x+xs[5+q],yy,fmt(d2[q*12+k],True))
        return ytop-(y-11-12*10.2)
    c.setFont('DejaVuSans-Bold',8); xs=[0,w*0.30,w*0.42,w*0.72]
    for t,xx in zip(['Month','Days' if not s['slow'] else 'Boxes',f'Year {y0}',f'Year {y0+1}'],xs): c.drawString(x+xx,y,t)
    for k in range(12):
        yy=y-12.5-k*11.2
        if k%2==0: fill(c,BAND); c.rect(x,yy-3,w,11.2,stroke=0,fill=1); fill(c,(0,0,0))
        c.setFont('DejaVuSans',8); nm=s['names'][k][0]+(' '+s['names'][k][1] if s['names'][k][1] else '')
        c.drawString(x,yy,nm); c.drawString(x+xs[1],yy,str(ms[k])); c.drawString(x+xs[2],yy,fmt(d1[k])); c.drawString(x+xs[3],yy,fmt(d2[k]))
    return ytop-(y-12.5-12*11.2)

def hms(days):
    sec=round(days*86400); d,r=divmod(sec,86400); h,r=divmod(r,3600); m,se=divmod(r,60); return d,h,m,se
def raw_cycle(c,s,L,x,ytop,w):
    h=section(c,x,ytop,w,'THE RAW CYCLE'); y=ytop-h-12
    P=s['period']; sec=round(P*86400); d,hh,m,se=hms(P)
    c.setFont('DejaVuSans',8); c.drawString(x,y,('Seconds (mean)' if E.EMP else 'Seconds (tropical, mean)')+((' · one year = 12 cycles' if E.EMP else ' · one year = 12 conjunctions') if s['cycles']==12 else ' · one year = 3 cycles' if s['cycles']==3 else ''))
    c.setFont('DejaVuSans-Bold',19); c.drawString(x,y-21,f'{num(sec)} s')
    rows=[('= time',f'{d} d {hh} h {m} m {se} s'),('= days',f'{P:.5f}')]
    if s['slow']: rows.append(('= GG months',f"{P/float(E.SYNODIC):.5f}") if E.EMP else ('= New Moons',f"{P/float(E.SYNODIC):.5f} lunations"))
    st=s['start']
    rows+=([] if E.EMP else [('Orb',f"± {s['orb']:.0f} days" if s['orb']>=1.5 else '± 1 day')])+[('Wobble',f"{s['des']['err_h']:.1f} h" + (' of a lunation-hour scale' if False else '')),
           ('Year 1',(('GG month of ' if E.EMP else 'New Moon of ') if s['slow'] else '')+fmt(st['date'])),('Year 1 hour',str(st['hour'])),('Epoch','8 Dec 2025')]
    yy=y-36
    for a,b in rows:
        c.setFont('DejaVuSans',8.4); c.drawString(x,yy,a); c.setFont('DejaVuSans-Bold',8.4); c.drawString(x+62,yy,b); yy-=11.6
    return ytop-yy

def tiers_panel(c,s,x,ytop,w):
    h=section(c,x,ytop,w,'WHOLE DAYS · STEP · TIERS'); y=ytop-h-12; d=s['des']; u='boxes' if s['slow'] else 'days'
    left=float(d['hrs'])
    rows=[('Short year',f"{d['d']} {u}"),('Leftover',f"{left:.3f} h → factor {d['factor']} h"),('Hour step',f"+{d['s']} h a year"),('Long year',f"{d['d']+1} {u}")]
    for k in range(3):
        if k<len(d['tiers']):
            N,cc=d['tiers'][k]; rows.append((f'Tier {k+1}',f"every {num(N)} yr: {'+' if cc>0 else '−'}{abs(cc)} h ▲"))
        else: rows.append((f'Tier {k+1}','not needed'))
    for i,(a,b) in enumerate(rows):
        f='DejaVuSans-Bold' if a.startswith('Tier') else 'DejaVuSans'
        c.setFont(f,8.4); c.drawString(x,y-i*12.2,a); c.setFont('DejaVuSans-Bold' if not a.startswith('Tier') else 'DejaVuSans',8.4); c.drawString(x+62,y-i*12.2,b)
    return ytop-(y-len(rows)*12.2)

def lifetime_text(s,L):
    slow=s['slow']; code=s['code']
    if not slow:
        how=('<b>How to use it.</b> Each row is one real year. A <b>start</b> is the day number on which this sheet begins a new year of its own (box 1 again); '
             'the small figure after the dot is the hour it begins (1–24, from 18:00), which you do not need to find a box. <b>Jan 1</b> is the box the sheet has reached on 1 January.<br/>'
             '<b>1.</b> Today’s day number = days before the month + the date.<br/><b>2.</b> In today’s row, find the last start that is not bigger than today’s day number. '
             '<b>Box = day number − start + 1.</b><br/><b>3.</b> No start yet this year? <b>Box = Jan 1 + day number − 1.</b><br/><b>4.</b> Find that box among the small numbers on the front.')
    else:
        how=('<b>How to use it.</b> Each row is one real year. <b>Jan 1</b> is the box the sheet is in on 1 January. Every number to its right is a day number on which the sheet moves on to its next box '
             +('(day 1 of a GG month). A ★' if E.EMP else '(a New Moon: the 1st of a month on the Moon sheet). A ★')+' means the sheet starts again at box 1 on that day.<br/>'
             '<b>1.</b> Today’s day number = days before the month + the date.<br/><b>2.</b> In today’s row, count the numbers that are not bigger than today’s day number.<br/>'
             '<b>3.</b> Box = the Jan 1 number + that count. After a ★, count again from 1.<br/><b>4.</b> Find that box among the small numbers on the front.')
    ex=dt.date(2031,5,22); dn=ex.timetuple().tm_yday; true=L.locate(ex)[1]
    if not slow:
        st=[(d.timetuple().tm_yday,hr) for d,hr,yy in L.year_starts_in(2031)]
        before=[a for a,_ in st if a<=dn]; jan=L.locate(dt.date(2031,1,1))[1]
        if before:
            a=before[-1]; box=dn-a+1
            txt=(f'<b>Example: 22 May 2031.</b> Day number = 120 + 22 = <b>{dn}</b>. The 2031 row has starts {", ".join(str(q) for q,_ in st)}. '
                 f'The last start not bigger than {dn} is <b>{a}</b>. Box = {dn} − {a} + 1 = <b>{box}</b>. Find box {box} on the front.')
        else:
            box=jan+dn-1
            txt=(f'<b>Example: 22 May 2031.</b> Day number = 120 + 22 = <b>{dn}</b>. The 2031 row has no start before day {dn}, and Jan 1 is {jan}. '
                 f'Box = {jan} + {dn} − 1 = <b>{box}</b>. Find box {box} on the front.')
    else:
        bs=[(d.timetuple().tm_yday,ny) for d,ny in L.box_starts_in_year(2031)]; jan=L.locate(dt.date(2031,1,1))[1]
        cnt=[(a,ny) for a,ny in bs if a<=dn]; stars=[i for i,(a,ny) in enumerate(cnt) if ny]
        if stars:
            box=len(cnt)-stars[-1]
            txt=(f'<b>Example: 22 May 2031.</b> Day number = 120 + 22 = <b>{dn}</b>. In the 2031 row the numbers up to {dn} are {", ".join(str(a)+("★" if ny else "") for a,ny in cnt)}. '
                 f'Count from the ★: <b>{box}</b>. Find box {box} on the front.')
        else:
            box=jan+len(cnt)
            txt=(f'<b>Example: 22 May 2031.</b> Day number = 120 + 22 = <b>{dn}</b>. In the 2031 row (Jan 1 = {jan}) the numbers not bigger than {dn} are '
                 f'{", ".join(str(a) for a,_ in cnt)}: {len(cnt)} of them. Box = {jan} + {len(cnt)} = <b>{box}</b>. Find box {box} on the front.')
    assert box==true,(code,box,true)
    days=('<b>Days before the month:</b> Jan 0 · Feb 31 · Mar 59 · Apr 90 · May 120 · Jun 151 · Jul 181 · Aug 212 · Sep 243 · Oct 273 · Nov 304 · Dec 334 '
          '(add 1 from March in the rows marked L, the leap years).')
    return how,txt,days

def lifetime_blocks(c,s,L,x,ytop,w,ybottom):
    slow=s['slow']
    h=section(c,x,ytop,w,'LIFETIME TABLE · 2026 to 2125 · '+('every box start' if slow else 'every year start')+', so this sheet outlives its Date Finder'); y=ytop-h-4
    nb=3 if slow else 4; per=math.ceil(100/nb); gap=10; bw=(w-(nb-1)*gap)/nb
    rh=min(11,(y-ybottom-3)/(per+1))
    fs=min(rh*0.82,7.6)
    years=list(range(2026,2126))
    for b in range(nb):
        bx=x+b*(bw+gap); stroke(c,GOLD); c.setLineWidth(0.8)
        c.rect(bx,y-(per+1)*rh-3,bw,(per+1)*rh+3); stroke(c,(0,0,0))
        fill(c,SECT); c.rect(bx,y-rh-1,bw,rh+1,stroke=0,fill=1); fill(c,(0,0,0))
        c.setFont('DejaVuSans-Bold',fs); c.drawString(bx+3,y-rh+1.5,'Year'); c.drawString(bx+34,y-rh+1.5,'Jan 1')
        c.drawString(bx+64,y-rh+1.5,'box starts' if slow else 'starts (day·hour)')
        for i,Y in enumerate(years[b*per:(b+1)*per]):
            ry=y-(i+2)*rh+rh*0.22
            leap=Y%4==0 and (Y%100!=0 or Y%400==0)
            c.setFont('DejaVuSans-Bold' if leap else 'DejaVuSans',fs); c.drawString(bx+3,ry,f'{Y}{"L" if leap else ""}')
            c.setFont('DejaVuSans-Bold',fs); c.drawRightString(bx+57,ry,str(L.locate(dt.date(Y,1,1))[1]))
            if slow: items=[f'{d.timetuple().tm_yday}{"★" if ny else ""}' for d,ny in L.box_starts_in_year(Y)]
            else: items=[f'{d.timetuple().tm_yday}·{hr:02d}{"▲" if L.is_tier_year(yy) else ""}' for d,hr,yy in L.year_starts_in(Y)]
            t='  '.join(items); f2=fs
            while sw(t,'DejaVuSansCondensed',f2)>bw-68 and f2>3.5: f2-=0.2
            c.setFont('DejaVuSansCondensed',f2); c.drawString(bx+63,ry,t)
            if i%5==4: stroke(c,MIDGREY); c.setLineWidth(0.25); c.line(bx,y-(i+2)*rh,bx+bw,y-(i+2)*rh); stroke(c,(0,0,0))
        c.setLineWidth(0.4); stroke(c,GOLD); c.line(bx+31,y,bx+31,y-(per+1)*rh-3); c.line(bx+60,y,bx+60,y-(per+1)*rh-3); stroke(c,(0,0,0))
    return y-(per+1)*rh-3

def sky_check(s,L):
    if E.EMP: return emp_check(s,L)
    code=s['code']; bs=E.bodies(code)
    ev={'GG':'the New Moon with the Sun in Taurus','DD':'the March equinox, when the Sun reaches 0° Aries','HH':'the mean North Node entering Gemini (moving backwards)'}.get(code)
    if ev is None:
        if len(bs)==1: ev=f'{E.NAMES[bs[0]]} entering {E.SIGNS[E.EXALT[bs[0]]//30]} (heliocentric)'
        elif code=='FD': ev='the Mercury–Sun superior conjunction with the Sun in Cancer'
        elif code=='GD': ev='the New Moon'
        elif code[0]=='G': ev=f'the Moon meeting {nm_lower(bs[1])}'
        elif bs[1]=='H': ev=f'{nm_lower(bs[0])} meeting the mean North Node'
        else: ev=f'the {E.NAMES[bs[0]]}–{E.NAMES[bs[1]]} conjunction'
    if s['slow']:
        t=f'<b>Sky check.</b> Day 1 of month 1 is {ev}. Look up (any ephemeris) the date it last did that: the box it falls in is box 1. Count the New Moons since (the 1st of each Moon-sheet month): the box number is 1 plus that count. The sky may stand up to the orb from the sheet.'
    else:
        t=f'<b>Sky check.</b> Day 1 of month 1 is {ev}. Look up (any ephemeris) the date it last did that: that date is day 1. Count on to today and cross off that day. The sky may stand up to the orb from the sheet.'
    hold=Lg.months_hold_until(s)
    if hold:
        fv=''
        if code=='DD': fv=f' (Folvasin {6911+hold})'
        t+=f'<br/><b>Month lengths</b> hold until own year {hold}{fv}; after that the apsides have moved far enough for a month to gain or lose a day. The front shows them.'
    elif len(bs)==2:
        t+='<br/><b>Month lengths</b> are equal and never change.'
    t+='<br/>▲ marks a correction year. Method pages 3–4 rebuild any year.'
    return t

def emp_check(s,L):
    t=(f'<b>Checking.</b> Year 1 began on {fmt(s["start"]["date"])} in hour {s["start"]["hour"]}'+(' (the GG month that held it)' if s['slow'] else '')+'. '
       'Every later year start follows from the rule on the method pages; the Lifetime Table must agree with it to the digit. The sheet runs on the count alone: never adjust it to anything outside the pack.')
    hold=Lg.months_hold_until(s)
    if hold: t+=f'<br/><b>Month lengths</b> hold until own year {hold}; after that a month gains or loses a day. The front shows them.'
    elif len(E.bodies(s['code']))==2: t+='<br/><b>Month lengths</b> are equal and never change.'
    return t+'<br/>▲ marks a correction year. The method pages rebuild any year.'

def back(c,s):
    L=Lg.Ledger(s)
    band(c,M,H-M,W-2*M,46,f"DATE FINDER & TABLES  ·  {(s['glyphs']+' ' if s['glyphs'] else '')}{s['title'].upper()}",f"Calendar {s['no']} of 36 · reverse of the day-boxes sheet · look up, do not count",None,None,s['code'],tsize=21)
    top=H-M-56; bot=M+26; gut=16
    LW=(W-2*M-gut)*0.64; RW=W-2*M-gut-LW; RX=M+LW+gut
    # left: Date Finder, then the Lifetime blocks
    y=top
    h=section(c,M,y,LW,'DATE FINDER · today’s date → month · '+('box' if s['slow'] else 'day')+f' · {window()}'); y-=h+1
    leg=('Find the date, read the cell: month · '+('box' if s['slow'] else 'day')+'. A new date begins at 18:00. Gold = first of a month · red = first of a year · bands = alternate own years · + = intercalary day.')
    if s['code']=='HH': leg+=' Days count down, as on the front.'
    c.setFont('DejaVuSans',7.2); c.drawString(M,y-8.5,leg); y-=13
    y-=date_finder(c,s,L,M,y,LW,rh=11.3)+10
    lifetime_blocks(c,s,L,M,y,LW,bot)
    # right: month starts, raw cycle and tiers, how to read the Lifetime Table, sky check
    y=top
    y-=month_starts(c,s,L,RX,y,RW)+10
    hw=(RW-10)/2
    h2=raw_cycle(c,s,L,RX,y,hw); h3=tiers_panel(c,s,RX+hw+10,y,hw); y-=max(h2,h3)+8
    how,ex,days=lifetime_text(s,L)
    h=section(c,RX,y,RW,'READING THE LIFETIME TABLE'); y-=h+5
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    sky=sky_check(s,L)
    def heights(fs):
        st=ParagraphStyle('e',fontName='DejaVuSans',fontSize=fs,leading=fs*1.3)
        ps=[Paragraph(t,st) for t in (how,ex,days,sky)]; hs=[p.wrap(RW-(12 if i==1 else 0),2000)[1] for i,p in enumerate(ps)]
        return ps,hs,sum(hs)+10+fs*0.7*3+8
    fs=11.0
    while fs>7 and heights(fs)[2]>y-bot: fs-=0.2
    ps,hs,_=heights(fs); g=fs*0.7
    ps[0].drawOn(c,RX,y-hs[0]); y-=hs[0]+g
    fill(c,BAND); stroke(c,GOLD); c.rect(RX,y-hs[1]-10,RW,hs[1]+10,fill=1); stroke(c,(0,0,0)); fill(c,(0,0,0)); ps[1].drawOn(c,RX+6,y-hs[1]-5); y-=hs[1]+10+g
    ps[2].drawOn(c,RX,y-hs[2]); y-=hs[2]+g
    ps[3].drawOn(c,RX,y-hs[3])
    c.setFont('DejaVuSans',6.4)
    if E.EMP: c.drawString(M,M+10,f'Dates checked to {PRINT_DATE.day} {MON[PRINT_DATE.month-1]} {PRINT_DATE.year}. A day begins at 18:00 by your own clock, everywhere. Year 1 of every cycle was fixed once from published tables; every later date follows from the printed rules alone.')
    else: c.drawString(M,M+10,f'Dates checked to {PRINT_DATE.day} {MON[PRINT_DATE.month-1]} {PRINT_DATE.year}. A day begins at 18:00 by your own clock, everywhere. Positions: Swiss Ephemeris (Moshier) for true ingresses, Meeus mean elements for the mean cycles; periods are tropical means.')
    c.setFont('DejaVuSans',6); c.drawString(M,M,LIC)
