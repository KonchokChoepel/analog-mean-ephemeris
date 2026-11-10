import sys,os; sys.path.insert(0,'.')
import pickle
from almanac import *
R=pickle.load(open('R.pkl','rb'))
f={b:motion(b) for b in 'GFEDCBAH'}
rows=[]; CODE={}
for pack in PACKS:
    for no,code in members(pack):
        bs=bodies(code)
        if len(bs)!=2 or code in('GG','HI'): continue
        x,y=sorted(bs,key=lambda b:-abs(f[b]))
        rate=abs(f[x]-f[y]); sc=R[code]['sc']
        CODE[no]=code
        rows.append(dict(pack={'Saturn_and_Nodes':'Saturn/Nodes'}.get(pack[0],pack[0]),no=no,x=x,y=y,rate=rate,sc=sc))
c=canvas.Canvas((sys.argv[1] if len(sys.argv)>1 else 'Separation_Table.pdf'),pagesize=landscape(A4)); c.setTitle('Separation Table: degrees to days')
c.setFillColor(NAVY); c.rect(M,H-M-40,W-2*M,40,stroke=0,fill=1); c.setFillColor(white)
c.setFont('DVB',17); c.drawString(M+10,H-M-20,"SEPARATION TABLE · degrees to days for the 28 pairs")
c.setFont('DV',8.5); c.drawString(M+10,H-M-33,"Mean heliocentric motions · separation = angle between the two mean longitudes · whole numbers, real days unless the 1-calendar-day column says otherwise")
cols=[("Almanac",62),("No.",26),("Pair (faster – slower)",172),("Degrees\nper day",46),("Days per\n10°",46),("Days per\n30°",50),("Conjunction\nevery (days)",66),("About\nyears",40),("Calendar\nmonth (days)",62),("Year S / L\n(cal. days)",62),("1 cal.\nday =",44),("° per\ncal. day",44)]
x0=M; y=H-M-40-8; rh=14.6
hdr=26; c.setFillColor(LB); c.rect(x0,y-hdr,sum(w for _,w in cols),hdr,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVB',7)
xs=x0
for lab,w in cols:
    ls=lab.split('\n')
    for i,l in enumerate(ls): c.drawCentredString(xs+w/2,y-10-i*8.5,l)
    xs+=w
y-=hdr; prev=None; shade=False
from data import build
for r in rows:
    if r['pack']!=prev: shade=not shade; prev=r['pack']
    c.setFillColor(LG if shade else white); c.setStrokeColor(RULE); c.setLineWidth(.3)
    c.rect(x0,y-rh,sum(w for _,w in cols),rh,stroke=0,fill=1)
    X=build(CODE[r['no']]); ms=X['months']; d0=X['des']['d']
    rt=r['rate']; per=360/rt; yrs=per/365.2422
    mo=f"{min(ms)}" if min(ms)==max(ms) else f"{min(ms)}–{max(ms)}"
    vals=[r['pack'],str(r['no']),f"{GLYPH[r['x']]} {NAMES[r['x']]} – {GLYPH[r['y']]} {NAMES[r['y']]}"+(" (Nodes retrograde)" if 'H' in (r['x'],r['y']) else ""),
          (f"{round(rt)}" if rt>=1 else "under 1"),f"{round(10/rt)}",f"{round(30/rt):,}",f"{round(per):,}",(f"{round(yrs)}" if yrs>=1 else "under 1"),mo,f"{d0} / {d0+1}",
          f"{r['sc']} d",(f"{round(rt*r['sc'])}" if rt*r['sc']>=1 else "under 1")]
    xs=x0
    for j,((lab,w),v) in enumerate(zip(cols,vals)):
        c.setFillColor(black); c.setFont('DVCB' if j==2 else 'DVC',7.4)
        if j==2: c.drawString(xs+4,y-10.3,v)
        elif j==0:
            if r['pack']!=getattr(c,'_lp',None): c.setFont('DVCB',7.2); c.drawString(xs+4,y-10.3,v)
        else: c.drawCentredString(xs+w/2,y-10.3,v)
        xs+=w
    c._lp=r['pack']; y-=rh
c.setStrokeColor(RULE); c.setLineWidth(.5); c.rect(x0,y,sum(w for _,w in cols),(H-M-40-8-hdr)-y,stroke=1,fill=0)
y-=10
txt=("<b>How to use.</b> Everything here is in whole numbers, rounded to the nearest. <b>Degrees per day</b> is how fast the faster planet gains on the slower; for the slow pairs it is under 1, so use <b>Days per 10°</b> instead: after a conjunction, the pair is 10° apart that many days later, 20° twice that, and so on. "
 "<b>Days per 30°</b> is one house of separation. <b>Calendar month</b> is the month length printed on the pair's Master page; on the Moon's pairs a month is one whole conjunction, not a 30° house. "
 "<b>Year S / L</b> is the short and long year in calendar days. On the calendars whose cycle is 1,000 days or more, one calendar day equals 30 real days, so the last two columns give the scale. "
 "The Nodes move backward (about −0.053° a day), so every Node pair separates at the sum of the two rates. "
 "Figures are mean (regular-pace); rounding costs under half a day per 10° on the fast pairs, so for long separations use Days per 30° rather than multiplying a rounded figure. "
 "The separation seen in the sky differs from these by up to the orb printed on each Master page.")
para(c,txt,M,y,W-2*M,sty(8))
c.setFillColor(GREY); c.setFont('DVC',6.5); c.drawString(M,M-4,"Days are mean-motion days (24 h). Conjunction every = 360° ÷ separation rate, rounded to a whole day.")
c.showPage(); c.save(); print(len(rows),'pairs')
