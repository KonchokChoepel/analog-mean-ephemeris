import sys,os; sys.path.insert(0,'.')
from data import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import os
FD=os.environ.get('DEJAVU_DIR','/usr/share/fonts/truetype/dejavu/')
for n,f in (('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVC','DejaVuSansCondensed.ttf'),('DVCB','DejaVuSansCondensed-Bold.ttf')):
    pdfmetrics.registerFont(TTFont(n,FD+f))
W,H=landscape(A4); M=24
NAVY=HexColor('#1F3864'); GREY=HexColor('#7F7F7F'); LG=HexColor('#EDEDED'); LB=HexColor('#D9E1F2'); YEL=HexColor('#FFF2CC'); RULE=HexColor('#8C8C8C')
PERI_MONTH=4; APO_MONTH=10          # user's rule: perigee in month 4, apogee in month 10
ORDER=['G','F','E','D','C','B','A','H']
PACKS=[('Moon','G',['G']),('Mercury','F',['F']),('Venus','E',['E']),('Sun','D',['D']),('Mars','C',['C']),('Jupiter','B',['B']),('Saturn_and_Nodes','A',['A','H'])]
def sty(size=8,font='DVC',color=black,align=0): return ParagraphStyle('x',fontName=font,fontSize=size,leading=size*1.3,textColor=color,alignment=align)
def para(c,text,x,ytop,w,style):
    p=Paragraph(text,style); pw,ph=p.wrap(w,1000); p.drawOn(c,x,ytop-ph); return ph
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def ecc_of(b):
    nm={'A':'Saturn','B':'Jupiter','C':'Mars','D':'Earth','E':'Venus','F':'Mercury'}[b]; el=EL[nm]; T=jd2T(EPOCH_JD)
    return el[1]+el[7]*T
def apse_months(e,d):
    """12 arcs of 30 deg true anomaly, perigee at the middle of month 4 (apogee middle of month 10)."""
    v=np.radians(30*(np.arange(13)-PERI_MONTH+1)-15)   # month k spans v[k-1]..v[k]
    E=2*np.arctan2(np.sqrt(1-e)*np.sin(v/2),np.sqrt(1+e)*np.cos(v/2)); Mn=E-e*np.sin(E)
    Mn=np.unwrap(Mn); fr=np.diff(Mn)/(2*np.pi)
    return largest_remainder(list(fr),d)
def months_of(code,X):
    d=X['des']['d']
    if code in SINGLE_ECC:
        import apse; f,ev=apse.events(code,X); return f,True
    return X['months'],False
def members(pack):
    _,_,owners=pack; out=[]
    for (no,code,_) in CAL:
        bs=bodies(code)
        inf=min(bs,key=lambda b:ORDER.index(b)) if len(bs)==2 else bs[0]
        if code in('GG','HI'): inf=code[0]
        if inf in owners: out.append((len(bs)==2 and 1 or 0,ORDER.index(max(bs,key=lambda b:ORDER.index(b))) if len(bs)==2 else -1,no,code))
    out.sort(); return [(n,c) for _,_,n,c in out]
def title_of(X):
    code=X['code']; bs=X['bs']
    if len(bs)==1: return f"{GLYPH[bs[0]]} {NAMES[bs[0]].upper()}", TITLES[code]
    a,b=bs; return f"{GLYPH[a]}{GLYPH[b]}  {NAMES[a].upper()} – {NAMES[b].upper()}", ("12 conjunctions per year" if X.get("moonpair") else "Conjunction cycle · months are houses")
def short_desc(X,ecc):
    code=X['code']; bs=X['bs']; slow=X['slow']
    if ecc:
        import apse; p,a=apse.apse_month(code[0],jd2T(EPOCH_JD)); T0=f"Longest months are around the {ordn(a)} month (apogee), shortest around the {ordn(p)} (perigee)."
    if code=='DD': t="Year begins at 0° Aries. "+T0+" Months change very slowly: see the Month-Length Table."
    elif code=='GG': t="Year begins at the New Moon in Taurus. Twelve lunations; month 1 is Taurus."
    elif code=='HI': t="Year begins at 3° Gemini (the Nodes' exaltation). Twelve equal months of one Nodal cycle."
    elif ecc: t=f"Year begins when {NAMES[bs[0]]} reaches its exaltation, {EXALT[bs[0]]%30}° {SIGNS[EXALT[bs[0]]//30]}. "+T0+" Months change slowly: see the Month-Length Table."
    elif X['moonpair']:
        t=f"Year begins at a conjunction of the Moon and {NAMES[[x for x in bs if x!='G'][0]] if code!='HGI' else 'the Nodes'}. A year is 12 conjunctions: each month is one conjunction cycle, and the conjunction falls on the 1st of every month."
    else:
        F=NAMES[X['fast']]; S=NAMES[X['slowb']]
        t=f"Year begins at the {NAMES[bs[0]]}–{NAMES[bs[1]]} conjunction. Month n is house n: {F} in the nth house of {S}."
        if X['back']: t+=" Nodes move backward, so houses count backward."
    if slow: t+=" <b>One box = 30 real days.</b>"
    return t
def draw_calendar(c,X,months,ecc,pack_name):
    code=X['code']; d=X['des']['d']; slow=X['slow']; sun=(code=='DD')
    c.setFillColor(NAVY); c.rect(M,H-M-34,W-2*M,34,stroke=0,fill=1)
    t1,t2=title_of(X); c.setFillColor(white)
    c.setFont('DVB',16); c.drawString(M+8,H-M-20,t1); c.setFont('DV',8); c.drawString(M+8,H-M-30,t2)
    c.setFont('DVB',22); c.drawRightString(W-M-8,H-M-24,code)
    c.setFont('DVC',8); c.drawRightString(W-M-70,H-M-14,f"CALENDAR {X['no']} OF 36  ·  {pack_name.replace('_',' ')} almanac")
    c.drawRightString(W-M-70,H-M-26,f"short year {d} days · long year {d+1} days · hour step +{X['des']['s']}")
    y=H-M-34-4
    ph=para(c,short_desc(X,ecc),M,y,W-2*M,sty(8)); y-=ph+3
    # blank fields
    c.setFillColor(black); c.setFont('DVC',8)
    fy=y-12
    fx=M; 
    for lab,wd in (("Year (Folvasin)",110),("Gregorian date",120),("New year hour",130)):
        c.drawString(fx,fy,lab+":"); lw=c.stringWidth(lab+":",'DVC',8); c.setStrokeColor(RULE); c.setLineWidth(.6); c.line(fx+lw+3,fy-1.5,fx+lw+3+wd-lw-8,fy-1.5); fx+=wd+30
    c.setLineWidth(.6)
    for lab in (f"short year ({d} d)",f"long year ({d+1} d)"):
        c.rect(fx,fy-1.5,8,8,stroke=1,fill=0); c.drawString(fx+12,fy,lab); fx+=c.stringWidth(lab,'DVC',8)+28
    y=fy-8
    # grid layout: 4 x 3 blocks
    top=y; bottom=M+16; bw=(W-2*M)/4; bh=(top-bottom)/3
    last=max(months); ncol=7 if sun else (last if last<=10 else 10)
    if sun: pass
    offset=0
    ic_total=None
    for k,m in enumerate(months):
        col=k%4; row=k//4; bx=M+col*bw; by=top-row*bh
        pad=3; gw=bw-2*pad
        # title bar
        c.setFillColor(LB); c.rect(bx+pad,by-12,gw,12,stroke=0,fill=1)
        c.setFillColor(black); c.setFont('DVB',7.5)
        sg=SIGNS[(X['first']+k)%12]
        lab=(f"{ordn(k+1)} house · {sg}" if X['houses'] else f"{ordn(k+1)} · {sg}")
        c.drawString(bx+pad+3,by-9,lab); c.setFont('DVC',7); c.drawRightString(bx+pad+gw-52,by-9,f"{m} d")
        c.setFont('DVC',6.5); c.setFillColor(GREY); c.drawRightString(bx+pad+gw-3,by-9,"starts ______"); c.setFillColor(black)
        n_cells=m
        off=offset if sun else 0
        rows=(off+n_cells+ncol-1)//ncol
        if sun: rows=max(rows,5)
        areah=bh-12-(10 if sun else 0)-8
        cw_=min(gw/ncol,34); ch=min(areah/max(rows,1),30 if not sun else 22)
        gx=bx+pad+(gw-cw_*ncol)/2; gy=by-12-(10 if sun else 0)
        if sun:
            c.setFont('DVC',5.5); c.setStrokeColor(RULE)
            for j in range(ncol):
                c.setFillColor(white); c.rect(gx+j*cw_,by-12-10,cw_,10,stroke=1,fill=1)
        c.setStrokeColor(RULE); c.setLineWidth(.5)
        for i in range(n_cells):
            p=off+i; r_=p//ncol; cc=p%ncol; x0=gx+cc*cw_; y0=gy-(r_+1)*ch
            ic=(k==11 and i==m-1)
            c.setFillColor(YEL if ic else white); c.rect(x0,y0,cw_,ch,stroke=1,fill=1)
            if ic:
                c.setStrokeColor(RULE); c.line(x0,y0,x0+cw_,y0+ch)
                c.setFillColor(black); c.setFont('DVB',8); c.drawString(x0+1.5,y0+ch-8,str(m))
                c.drawRightString(x0+cw_-1.5,y0+2,str(m+1))
            else:
                yd=sum(months[:k])+i+1
                c.setFillColor(black); c.setFont('DVB',9 if cw_>14 else 7); c.drawCentredString(x0+cw_/2,y0+ch/2-3,str(i+1))
                c.setFillColor(GREY); c.setFont('DVC',5); c.drawString(x0+1.5,y0+ch-5.5,str(yd))
        offset=(offset+m)%7
    c.setFillColor(GREY); c.setFont('DVC',6.5)
    c.drawString(M,M+4,"Small grey number = day of the year. The last box is split: the top-left number is the last day of a SHORT year, the bottom-right number is the last day of a LONG year (the Intercalary Day). Day 1 of month 1 appears only once.")
    if sun: c.drawString(M,M-4+2+0,"")
    c.setFont('DVC',6.5)
    foot=f"Complete the blanks from Master calendar {X['no']} of 36 (year, dates, new-year hour)."
    if sun: foot="Weekdays: write the weekday names in the 7 header boxes (column 1 = weekday of day 1 of the year). Dates and new-year hour from Master calendar 1. "
    c.drawRightString(W-M,M+4-10,foot)
def cover(c,pack,items,data):
    name=pack[0].replace('_',' & '); c.setFillColor(NAVY); c.rect(M,H-M-70,W-2*M,70,stroke=0,fill=1)
    c.setFillColor(white); c.setFont('DVB',26); c.drawString(M+14,H-M-38,f"{name.upper()} CULT ALMANAC")
    c.setFont('DV',10); c.drawString(M+14,H-M-58,f"{len(items)} printable calendar{'s' if len(items)>1 else ''} · whole days · universal template")
    y=H-M-90
    c.setFillColor(black); c.setFont('DVB',11); c.drawString(M,y,"Contents"); y-=16
    c.setFont('DVB',8); 
    for x,t in ((M,'Page'),(M+90,'Master no.'),(M+160,'Calendar'),(M+420,'Short / long year'),(M+560,'Month rule')): c.drawString(x,y,t)
    y-=4; c.setStrokeColor(RULE); c.line(M,y,W-M,y); y-=12; c.setFont('DVC',9)
    pg=2
    for i,(no,code) in enumerate(items):
        X,months,ecc=data[code]; t1,_=title_of(X); d=X['des']['d']
        import apse
        nsh=(-(-(1+len(apse.events(code,X)[1]))//26)) if ecc else 0
        c.drawString(M,y,str(pg)+(f" (table {pg+1}–{pg+nsh})" if nsh>1 else (f" (table {pg+1})" if nsh else ''))); pg+=1+nsh
        c.drawString(M,y,'') if False else None
        c.setFont('DVC',9); c.drawString(M+90,y,f"{no} ({code})"); c.drawString(M+160,y,t1); c.drawString(M+420,y,f"{d} / {d+1} days"+(" (1 day = 30 real days)" if X['slow'] else ""))
        c.drawString(M+560,y,"real apsides + table" if ecc else ("houses, equal" if X['houses'] else ("12 conjunctions, equal" if X.get("moonpair") else "equal"))); y-=14
    y-=10; c.setFont('DVB',11); c.drawString(M,y,"How to use these pages"); y-=6
    txt=("1. Every page is a blank template and never changes. Print it again each year.<br/>"
     "2. Fill the top blanks (year, Gregorian date, new-year hour) from the matching Master calendar, and tick short or long year from its 100-year grid.<br/>"
     "3. Write each month's starting date in its “starts ______” blank, counting the day numbers from the Master's month table.<br/>"
     "4. The last box of the year is split and yellow. In a short year the year ends on the top-left number; in a long year it ends on the bottom-right number (the Intercalary Day). The calendar has exactly as many boxes as a short year has days, and day 1 of month 1 appears once, in its own place.<br/>5. Eccentric months: the twelve lengths are the real ones at the epoch (long months where the planet is slow, short where it is fast). The planet's apsides drift very slowly, so the Month-Length Table page after each such calendar lists the years from which the twelve lengths change.<br/>"
     "6. Days begin at 18:00 UTC, so hour 0 is 18:00 UTC and each day carries the Gregorian date of the day it ends in.<br/>7. Pair calendars have equal months. Each month is a house of the slower planet, except on the Moon's pairs, where each month is one full conjunction cycle (the conjunction falls on the 1st of every month)."
     +("<br/>8. The Sun calendar is the only one with weekdays. Write the seven weekday names in the header boxes once per year when printing; they stay the same in every month." if any(c_=='DD' for _,c_ in items) else ""))
    para(c,txt,M,y,W-2*M,sty(9))
def draw_shift(c,X,first,ev,pack_name):
    import apse
    code=X['code']; d=X['des']['d']; t1,_=title_of(X)
    rows=[(1,6912,first,[0]*12)]+ev; per=26; pages=[rows[i:i+per] for i in range(0,len(rows),per)]
    for pi,pg in enumerate(pages):
        c.setFillColor(NAVY); c.rect(M,H-M-34,W-2*M,34,stroke=0,fill=1); c.setFillColor(white)
        c.setFont('DVB',14); c.drawString(M+8,H-M-18,f"MONTH-LENGTH TABLE  ·  {t1}  ({code})")
        c.setFont('DV',8); c.drawString(M+8,H-M-29,f"Calendar {X['no']} of 36 · page {pi+1} of {len(pages)} · short year {d} days")
        c.setFont('DVB',20); c.drawRightString(W-M-8,H-M-24,code)
        y=H-M-34-4
        ph=para(c,"The planet's apsides drift slowly against the fixed month boundaries, so month lengths change now and then (a day moves from one month to another, so the year stays "+str(d)+" days). Find the latest row whose own-year number is not more than the current year; use that row's twelve lengths from the start of that year. Yellow cells show what changed. Rows cover about 5,000 years after the epoch"+(" and the last row stays in force after that." if pi==len(pages)-1 else "; continued overleaf."),M,y,W-2*M,sty(8)); y-=ph+6
        cols=[('From own year',70),('Folvasin yr ≈',70)]+[(f"{ordn(i+1)} {SIGNS[(X['first']+i)%12][:3]}",44) for i in range(12)]+[('Total',40)]
        x=M; rh=17; c.setFont('DVB',7.5)
        c.setFillColor(LB); c.rect(M,y-rh,sum(w for _,w in cols),rh,stroke=0,fill=1); c.setFillColor(black)
        for lab,w in cols: c.drawCentredString(x+w/2,y-11,lab); x+=w
        y-=rh
        for (yr,fy,L,df) in pg:
            x=M; vals=[("1 (epoch)" if yr==1 else str(yr)),("6912" if yr==1 else str(fy))]+[str(v) for v in L]+[str(sum(L))]
            xs=M
            for j,(v,(lab,w)) in enumerate(zip(vals,cols)):
                chg=(2<=j<=13 and df[j-2]!=0)
                c.setFillColor(YEL if chg else white); c.setStrokeColor(RULE); c.setLineWidth(.4); c.rect(xs,y-rh,w,rh,stroke=1,fill=1)
                c.setFillColor(black); c.setFont('DVB' if chg or j<2 else 'DVC',9); c.drawCentredString(xs+w/2,y-12,v)
                if chg: c.setFont('DVC',5.5); c.setFillColor(GREY); c.drawString(xs+2,y-6,f"{df[j-2]:+d}")
                xs+=w
            y-=rh
        c.setFillColor(GREY); c.setFont('DVC',6.5)
        c.drawString(M,M+4,"Year counts are this calendar's own years, counted from the epoch (year 1 = Folvasin 6912). Calculated from mean orbital elements; the far future is approximate.")
        c.showPage()
def build_pack(pack,outdir):
    items=members(pack); data={}
    for no,code in items:
        X=build(code); months,ecc=months_of(code,X); assert sum(months)==X['des']['d'],(code,sum(months)); data[code]=(X,months,ecc)
    fn=os.path.join(outdir,f"{pack[0]}_Cult_Almanac.pdf"); c=canvas.Canvas(fn,pagesize=landscape(A4)); c.setTitle(f"{pack[0].replace('_',' & ')} Cult Almanac")
    cover(c,pack,items,data); c.showPage()
    for no,code in items:
        X,months,ecc=data[code]; draw_calendar(c,X,months,ecc,pack[0]); c.showPage()
        if ecc:
            import apse; f,ev=apse.events(code,X); draw_shift(c,X,f,ev,pack[0])
    c.save(); return fn,items,data
if __name__=='__main__':
    out=sys.argv[1]; os.makedirs(out,exist_ok=True); tot=0
    for p in PACKS:
        fn,items,data=build_pack(p,out); tot+=len(items); print(p[0],[c for _,c in items])
        for _,code in items:
            X,m,ecc=data[code]; print('  ',code,X['des']['d'],m)
    print('total',tot)
