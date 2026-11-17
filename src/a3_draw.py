"""Shared drawing for the A3 pack: colours, fonts, the calendar grid, panels."""
import math
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import engine2 as E
FD='/usr/share/fonts/truetype/dejavu/'
for n in ['DejaVuSans','DejaVuSans-Bold','DejaVuSans-Oblique','DejaVuSans-BoldOblique','DejaVuSansCondensed','DejaVuSansCondensed-Bold']:
    pdfmetrics.registerFont(TTFont(n,FD+n+'.ttf'))
from reportlab.lib.fonts import addMapping
addMapping('DejaVuSans',0,0,'DejaVuSans'); addMapping('DejaVuSans',1,0,'DejaVuSans-Bold')
addMapping('DejaVuSans',0,1,'DejaVuSans-Oblique'); addMapping('DejaVuSans',1,1,'DejaVuSans-BoldOblique')
GOLD=(0.7296,0.559,0.0304); RED1=(1,0.6,0.6); REDLINE=(0.72,0.1,0.1); PINK=(1,0.8,0.8)
BAND=(0.9725,0.9649,0.9412); SECT=(0.949,0.9318,0.8784); GOLDCELL=(0.9098,0.86,0.7059); GREY=(0.8157,0.8157,0.8157)
MIDGREY=(0.549,0.549,0.549)
LIC='© 2026 Aidan John Walsh · CC BY-SA 4.0: use, share and modify freely, commercially too, with credit; share changes under the same licence · github.com/KonchokChoepel/analog-mean-ephemeris'
def sw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
def num(n): return f'{n:,}'.replace(',',' ')
def para(c,text,x,ytop,w,size=9,leading=None,font='DejaVuSans',color=(0,0,0),align=0):
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.3,textColor=color,alignment=align)
    p=Paragraph(text,st); _,h=p.wrap(w,10000); p.drawOn(c,x,ytop-h); return h
def fill(c,rgb): c.setFillColorRGB(*rgb)
def stroke(c,rgb): c.setStrokeColorRGB(*rgb)

def band(c,x,ytop,w,h,title,sub,right1,right2,code,tsize=24):
    fill(c,GOLD); c.rect(x,ytop-h,w,h,stroke=0,fill=1); fill(c,(1,1,1))
    c.setFont('DejaVuSans-Bold',tsize); c.drawString(x+14,ytop-h*0.48,title)
    c.setFont('DejaVuSans',tsize*0.46); c.drawString(x+14,ytop-h+8,sub)
    cs=tsize*1.35; c.setFont('DejaVuSans-Bold',cs); cw=sw(code,'DejaVuSans-Bold',cs); c.drawRightString(x+w-12,ytop-h*0.68,code)
    c.setFont('DejaVuSans',tsize*0.43)
    if right1: c.drawRightString(x+w-24-cw,ytop-h*0.38,right1)
    if right2: c.drawRightString(x+w-24-cw,ytop-h*0.72,right2)
    fill(c,(0,0,0))

def section(c,x,ytop,w,text,h=17,size=10):
    fill(c,SECT); c.rect(x,ytop-h,w,h,stroke=0,fill=1); fill(c,(0,0,0))
    c.setFont('DejaVuSans-Bold',size); c.drawString(x+6,ytop-h+h*0.3,text)
    return h

# ---------------- the calendar grid (A3 fronts, almanac pages, A4 home set)
SUNPAIRS=('FD','ED','DC','DB','DA')
def grid_rows(s,k,week):
    n=s['months'][k]
    if week:
        off=sum(s['months'][:k])%7; return math.ceil((off+n)/7)
    return math.ceil(n/10)
def calendar_fit(s,w,h,cols,hb,colgap,week,mingap):
    """box width and height that fill the area; box height never exceeds its width"""
    ms=s['months']; nmon=len(ms); ncol=7 if week else 10
    rows=[list(range(r,min(r+cols,nmon))) for r in range(0,nmon,cols)]
    colw=(w-(cols-1)*colgap)/cols; bw=colw/ncol
    whf=0.42 if week else 0
    per=sum(max(grid_rows(s,k,week) for k in r)+whf for r in rows)
    fixed=len(rows)*hb+(len(rows)-1)*mingap
    bh=min(bw,(h-fixed)/per)
    return bw,bh,rows,colw
def draw_calendar(c,s,x,ytop,w,h,cols,small=True,starts=True,hb=15,colgap=12,mono=False,week=None,mingap=None,fixed_bh=None):
    code=s['code']; ms=s['months']; names=s['names']; nmon=len(ms)
    week=(code=='DD') if week is None else week
    mingap=hb*0.7 if mingap is None else mingap
    bw,bh,rows,colw=calendar_fit(s,w,h,cols,hb,colgap,week,mingap)
    if fixed_bh: bh=min(bh,fixed_bh)
    ncol=7 if week else 10; whf=0.42 if week else 0
    used=sum(hb+(max(grid_rows(s,k,week) for k in r)+whf)*bh for r in rows)
    gap=(h-used)/(len(rows)-1) if len(rows)>1 else 0
    gap=max(mingap,min(gap,hb*3.2))
    total=used+gap*(len(rows)-1)
    if total<h: ytop-=(h-total)/2          # centre what cannot stretch further
    unit='boxes' if s['slow'] else 'd'
    cum=[0]
    for m in ms: cum.append(cum[-1]+m)
    countdown=code=='HH'; y=ytop; bs=min(bw,bh)
    for r in rows:
        nr=max(grid_rows(s,k,week) for k in r)
        for j,k in enumerate(r):
            mx=x+j*(colw+colgap); first=k==0; gw=ncol*bw
            nm,gl=names[k]; fs=min(hb*0.62,11)
            if mono:
                fill(c,(0,0,0)); c.setFont('DejaVuSans-Bold',fs); c.drawString(mx,y-hb*0.68,nm)
                if gl: c.setFont('DejaVuSans',fs*1.05); c.drawString(mx+4+sw(nm,'DejaVuSans-Bold',fs),y-hb*0.7,gl)
                c.setFont('DejaVuSans',fs*0.9); c.drawRightString(mx+gw,y-hb*0.68,f'{ms[k]} {unit}')
                c.setLineWidth(1.4 if first else 0.6); c.line(mx,y-hb*0.92,mx+gw,y-hb*0.92)
            else:
                fill(c,RED1 if first else GOLD); c.rect(mx,y-hb,gw,hb,stroke=0,fill=1)
                fill(c,(0.15,0.15,0.15) if first else (1,1,1))
                c.setFont('DejaVuSans-Bold',fs); c.drawString(mx+4,y-hb*0.7,nm)
                if gl: c.setFont('DejaVuSans',fs*1.05); c.drawString(mx+8+sw(nm,'DejaVuSans-Bold',fs),y-hb*0.72,gl)
                c.setFont('DejaVuSans',fs*0.9); rt='starts ____' if starts else ''
                if rt: c.drawRightString(mx+gw-3,y-hb*0.7,rt)
                c.drawRightString(mx+gw-(sw(rt,'DejaVuSans',fs*0.9)+16 if rt else 3),y-hb*0.7,f'{ms[k]} {unit}')
                fill(c,(0,0,0))
            yy=y-hb
            if week:
                c.setLineWidth(0.6); stroke(c,MIDGREY)
                for q in range(7): c.rect(mx+q*bw,yy-bh*whf,bw,bh*whf,stroke=1,fill=0)
                stroke(c,(0,0,0)); yy-=bh*whf
            off=(cum[k]%7) if week else 0
            n=ms[k]
            for i in range(n):
                p=off+i; bx=mx+(p%ncol)*bw; by=yy-(p//ncol+1)*bh
                last=(k==nmon-1 and i==n-1); ex=(first and s['exbox']==i+1)
                if not mono:
                    if code=='DH' and not last and E.box_eclipse(s,cum[k]+i): fill(c,SECT); c.rect(bx,by,bw,bh,stroke=0,fill=1)
                    if ex: fill(c,RED1); c.rect(bx,by,bw,bh,stroke=0,fill=1)
                    if last: fill(c,PINK); c.rect(bx,by,bw,bh,stroke=0,fill=1)
                fill(c,(0,0,0)); c.setLineWidth(0.5); stroke(c,(0.3,0.3,0.3) if mono else MIDGREY); c.rect(bx,by,bw,bh,stroke=1,fill=0); stroke(c,(0,0,0))
                if ex:
                    stroke(c,(0,0,0) if mono else REDLINE); c.setLineWidth(2.0 if mono else 1.4)
                    c.rect(bx+1,by+1,bw-2,bh-2,stroke=1,fill=0); stroke(c,(0,0,0))
                big=(n-i) if countdown else (i+1)
                rich=(code in SUNPAIRS or code=='DH') and not last and not E.EMP
                if rich:
                    # three bands: top = day of the year | distance (or eclipse mark); middle = day; bottom = Moon days
                    pad=(0.75 if bw<20 else max(0.8,bs*0.06))+(1.6 if ex else 0)
                    tl=str(cum[k]+i+1) if small else ''
                    tr=E.box_elong(s,cum[k]+i) if code in SUNPAIRS else ('◐' if E.box_eclipse(s,cum[k]+i) else '')
                    ms_=E.box_moonshift(s,cum[k]+i) if code in SUNPAIRS else 0
                    # printed on the first day of each month and wherever it changes; it holds until the next one
                    showm=code in SUNPAIRS and code!='DA' and (i==0 or ms_!=E.box_moonshift(s,cum[k]+i-1))
                    bl=(f"☽{ms_:+d}" if ms_ else '☽0').replace('-','−') if (code in SUNPAIRS and code!='DA') else ''
                    sf=min(6.5,max(3.6,min(bh*0.22,bw*0.2)))
                    fT,fR='DejaVuSansCondensed','DejaVuSansCondensed-Bold' if tr!='◐' else 'DejaVuSans'
                    room=bw-2*pad-0.7
                    W_=lambda t,f,z: sw(t,f,z) if t else 0
                    fM='DejaVuSans'
                    # rows as (left, left font, right, right font); A, B, C in order of preference
                    arrs={'A':((tl,fT,tr,fR),('','',bl,fM)),'B':((tl,fT,bl,fM),(tr,fR,'','')),'C':((tl,fT,'',''),(tr,fR,bl,fM))}
                    def ok(arr,z):
                        return all(W_(l,lf,z)+W_(r,rf,z)<=(room if (l and r) else bw-2*pad) for l,lf,r,rf in arrs[arr])
                    best=None
                    for name in 'ABC':
                        z=sf
                        while z>3.6 and not ok(name,z): z-=0.1
                        if ok(name,z) and (best is None or z>best[1]+0.05): best=(name,z)
                    arr,sf=best if best else ('C',3.6)
                    yt=by+bh-pad-0.74*sf
                    (t1l,t1lf,t1r,t1rf),(b1l,b1lf,b1r,b1rf)=arrs[arr]
                    resv=bool(b1l or b1r) and (showm or not ex)   # keep the band (except in the framed reference box), so day numbers match
                    if bl and not showm:
                        t1r=t1r if t1r!=bl else ''; b1l=b1l if b1l!=bl else ''; b1r=b1r if b1r!=bl else ''
                    if t1l: c.setFont(t1lf,sf); c.drawString(bx+pad,yt,t1l)
                    if t1r: c.setFillGray(0.25); c.setFont(t1rf,sf); c.drawRightString(bx+bw-pad,yt,t1r); c.setFillGray(0)
                    ybot=by+pad
                    if resv:
                        c.setFillGray(0.25)
                        if b1l: c.setFont(b1lf,sf); c.drawString(bx+pad,by+pad+0.02*sf,b1l)
                        if b1r: c.setFont(b1rf,sf); c.drawRightString(bx+bw-pad,by+pad+0.02*sf,b1r)
                        c.setFillGray(0); ybot=by+pad+0.76*sf+0.6
                    ytop=yt-0.02*sf-0.6
                    rh_=max(1.0,ytop-ybot); txt=str(big)
                    fs2=min(rh_/0.74,(bw-2*pad-(sw(bl,'DejaVuSans',sf) if False else 0))/(0.64*len(txt)),bs*0.5)
                    c.setFont('DejaVuSans-Bold',fs2)
                    c.drawCentredString(bx+bw/2,ybot+(rh_-0.73*fs2)/2,txt)
                    continue
                if small:
                    sf=max(3.6,bs*0.21); ins=3.0 if ex else 0
                    c.setFont('DejaVuSansCondensed',sf); c.drawString(bx+1.4+ins,by+bh-sf-0.6-ins*0.8,str(cum[k]+i+1))
                if last:
                    c.setLineWidth(0.6); c.line(bx+bw,by+bh,bx,by)
                    a,bb=(1,0) if countdown else (n,n+1)
                    fa=bs*0.3; c.setFont('DejaVuSans-Bold',fa)
                    ya=by+bh*(0.42 if small else 0.58)
                    if small: ya=min(ya,by+bh-max(3.6,bs*0.21)-0.6-0.6-0.74*fa)
                    c.drawString(bx+bw*0.1,ya,str(a)); c.drawRightString(bx+bw*0.94,by+bh*0.1,str(bb))
                else:
                    fs2=bs*(0.46 if big<100 else 0.38); c.setFont('DejaVuSans-Bold',fs2)
                    c.drawCentredString(bx+bw/2+(bw*0.05 if small else 0),by+(bh*0.5-fs2*0.5 if small else bh/2-fs2*0.36),str(big))
        y-=hb+(bh*whf if week else 0)+nr*bh+gap
    return y

# ---------------- text helpers for sheets
def sheet_kind(s):
    if E.EMP: return emp_kind(s)
    code=s['code']; bs=E.bodies(code)
    if len(bs)==1:
        return {'D':'Solar year','G':'12 lunations','F':'Mercurial year','E':'Venusian year','C':'Martian year','B':'Jovian year · 1 box = 1 New Moon','A':'Saturnian year · 1 box = 1 New Moon','H':'Nodal cycle · 1 box = 1 New Moon'}[bs[0]]
    if code in ('GF','GE'): return '12 lunations per year · as seen from Earth'
    if code[0]=='G': return '12 conjunctions per year'
    if code=='FD': return 'three conjunction cycles per year · 36 houses'
    return 'Conjunction cycle · months are houses'+(' · 1 box = 1 New Moon' if s['slow'] else '')
def nm_lower(b): return {'D':'the Sun','G':'the Moon','H':'the Nodes'}.get(b,E.NAMES[b])
def sheetno(code): return [x for x in E.all_sheets() if x['code']==code][0]['no']
def intro(s):
    if E.EMP: return emp_intro(s)
    code=s['code']; bs=E.bodies(code); ms=s['months']
    if code=='GG': return ('Year begins at the New Moon with the Sun in Taurus. Twelve lunations; month 1 is Taurus, and every month begins at a New Moon. '
                           '<b>In the sky:</b> the Full Moon falls near the 15th.')
    if code=='HH': return ('Year begins as the Nodes enter Gemini backwards (exaltation 3°, month 1). Months run in reverse and the days count down. One box is one New Moon: '
                           f'cross off a box on the 1st of every month of the Moon sheet ({sheetno("GG")}). <b>In the sky:</b> the month is the sign of the North Node.')
    if len(bs)==1:
        b=bs[0]; sign=E.SIGNS[E.EXALT[b]//30]
        lo=ms.index(min(ms))+1; hi=ms.index(max(ms))+1
        ap=('apogee','perigee') if b=='D' else ('aphelion','perihelion')
        start='Year begins at the March equinox (the Sun at 0° Aries).' if b=='D' else f'Year begins as {E.NAMES[b]} enters {sign} (heliocentric), the sign of its exaltation.'
        slow=f' One box is one New Moon: cross off a box on the 1st of every month of the Moon sheet ({sheetno("GG")}).' if s['slow'] else ''
        sky=(' <b>In the sky:</b> the month is the Sun’s sign and the day, less one, is about its degree.' if b=='D' else
             f' <b>In the sky:</b> {E.NAMES[b]} stands at the Sun’s degree ± its distance from the Sun on the {E.NAMES[b]}–Sun sheet ({sheetno(E.SUNPAIR[b])}).' if b in E.SUNPAIR else '')
        return f'{start} Longest months are around the {E.ORD[hi-1]} month ({ap[0]}), shortest around the {E.ORD[lo-1]} ({ap[1]}). Months change very slowly: the back of this sheet says when.{slow}{sky}'
    a,b=bs
    sign=E.SIGNS[int(E.midpoint(code)//30)]
    if a=='G' and b in E.SUNPAIR:
        pn=E.NAMES[b]; sp=E.SUNPAIR[b]; src=f"{'Sun–'+pn if sp[0]=='D' else pn+'–Sun'} sheet ({sheetno(sp)})"
        acc={'F':'within a day in 97 months out of 100','E':'within a day every month','C':'within a day in 95 months out of 100','B':'within a day in 96 months out of 100','A':'within a day in 98 months out of 100'}[b]
        if b in ('F','E'):
            head=(f'Seen from Earth, {pn} keeps close to the Sun, so the Moon meets it once a month, near the New Moon. Year begins with the month in which they meet in {sign}, '
                  f'the sign of their mutual exaltation; twelve lunations, every month beginning at a New Moon.')
        else:
            head=(f'Year begins as the Moon meets {pn} in {sign}, the sign of their mutual exaltation. A year is 12 conjunctions: each month is one conjunction cycle, and the conjunction falls on the 1st, on average.')
        if b=='A': rule=f' <b>In the sky:</b> Saturn is slow and far, and the Moon meets it on the 1st itself, {acc}.'
        else: rule=f' <b>In the sky:</b> the Moon meets {pn} on the 1st, moved by the ☽ figure in force that day on the {src}, the last one printed on or before it: {acc}.'
        return head+rule+' The sign beside each month is counted from the mutual exaltation; it is not where the Moon meets the planet.'
    if a=='G':
        if b=='D': return ('Year begins at the New Moon in Aries, the sign of the mutual exaltation of the Moon and the Sun. Twelve lunations: the New Moon falls on the 1st of every month, '
                           'the Full Moon near the 15th. <b>In the sky:</b> the Moon stands about 12° east of the Sun for every day since the 1st.')
        return (f'Year begins as the Moon meets {nm_lower(b)} in {sign}, the sign of their mutual exaltation. A year is 12 conjunctions: each month is one conjunction cycle, and the conjunction falls on the 1st of every month. '
                '<b>In the sky:</b> on the 1st the Moon crosses the ecliptic, going north; near the middle of the month it crosses going south.')
    if code in E.SUNPAIR.values():
        pl=a if a!='D' else b; pn=E.NAMES[pl]
        cyc=('A year is three conjunction cycles, 36 houses: house n of each cycle is Mercury in the nth house of the Sun. One intercalary day, after the 36th house. ' if code=='FD'
             else f'Month n is house n: {nm_lower(a)} in the nth house of {nm_lower(b)}. ')
        conj=' (the planet behind the Sun)' if pl in ('F','E') else ''
        moon=(f'<b>☽ figure</b> (bottom right): the days to move the Moon’s meeting with {pn} from the 1st of the Moon–{pn} month (sheet {sheetno("G"+pl)}), printed on the first day of each month and wherever it changes; it holds until the next one.' if pl!='A' else
              'Saturn needs no ☽ figure: the Moon meets it on the 1st of the Moon–Saturn month.')
        return (f'Year begins at the {E.NAMES[a]}–{E.NAMES[b]} conjunction{conj} in {sign}, their mutual exaltation. {cyc}'
                f'<b>Figure bottom left:</b> {pn}’s distance from the Sun as seen from Earth, in degrees: E = east, in the evening sky; W = west, in the morning sky'
                + (', 180 = opposition, retrograde around it' if pl in 'CBA' else '') + f'. {pn} in the sky = the Sun’s degree ± that figure; under about 12 it is lost in the Sun’s glare. {moon} '
                'Two planets meet in the sky when their distances read the same, on the same side. The sign beside each house is counted from the mutual exaltation; it is not where the pair stands.')
    if code=='DH':
        return ('Year begins as the Sun meets the North Node in Taurus, their mutual exaltation. Month n is house n: the Sun in the nth house of the Nodes. '
                '<b>◐ Eclipse seasons:</b> the marked boxes are the days when the Sun stands close enough to a Node for an eclipse. Every eclipse, solar or lunar, falls in a marked box: '
                'a New Moon in a marked box brings an eclipse of the Sun, a Full Moon an eclipse of the Moon.')
    if b=='H':
        txt=f'Year begins as {nm_lower(a)} meets the North Node in {sign}, their mutual exaltation. Month n is house n, counted forward from {nm_lower(a)}: {nm_lower(a)} in the nth house of the Nodes.'
    else:
        txt=f'Year begins at the {E.NAMES[a]}–{E.NAMES[b]} conjunction in {sign}, their mutual exaltation. Month n is house n: {nm_lower(a)} in the nth house of {nm_lower(b)}.'
    if s['slow']: txt+=f' One box is one New Moon: cross off a box on the 1st of every month of the Moon sheet ({sheetno("GG")}).'
    return txt+' The sign beside each house is counted from the mutual exaltation (house 1); it is not where the pair stands, which moves on with every conjunction.'

# ---------------- empirical edition texts (codes only; the key is sealed in the guide)
def emp_kind(s):
    code=s['code']; u=' · 1 box = 1 GG month' if s['slow'] else ''
    if code=='FD': return 'one year = 3 cycles · 36 months'
    if code in ('GF','GE'): return '12 months, each one GG month'
    if s['cycles']==12: return 'one year = 12 cycles · equal months'
    if len(E.bodies(code))==1: return ('12 months, alternating' if code=='GG' else '12 months, equal' if code=='HH' else '12 months, unequal')+u
    return '12 months, equal'+u
def emp_intro(s):
    code=s['code']; bs=E.bodies(code); ms=s['months']; n=len(ms)
    st=s['names'][0][1]
    t=f'Cycle {code}. The year begins with month 1 (sector {st}) and runs {n} months'
    if code=='FD': t+=': three cycles of twelve, with one intercalary day after month 36.'
    elif code in ('GF','GE'): t+=f': each month begins with a month of cycle GG (sheet {sheetno("GG")}), and the cycle’s start point falls in month 1.'
    elif s['cycles']==12: t+=', one cycle each: the cycle starts again on day 1 of every month.'
    elif len(bs)==1 and code not in ('GG','HH'):
        lo=ms.index(min(ms))+1; hi=ms.index(max(ms))+1
        t+=f' of unequal length, longest around month {hi} and shortest around month {lo}. Month lengths change very slowly: the back of this sheet says when.'
    elif code=='GG': t+=' of 29 and 30 days.'
    else: t+=' of equal length.'
    if code=='HH': t+=' Months run in reverse and the days count down.'
    if s['slow']: t+=f' One box is one month of cycle GG (sheet {sheetno("GG")}): cross off a box on day 1 of every GG month.'
    t+=' The letter beside each month is a fixed label counted from the start point; it does not move.'
    return t
def emp_shaded(s): return f'Shaded box: reference day, {s["exlabel"]}, on average.'
def shaded(s):
    if E.EMP: return emp_shaded(s)
    code=s['code']; bs=E.bodies(code)
    if len(bs)==1: return f'Shaded box: {nm_lower(bs[0])} {"reach" if bs[0]=="H" else "reaches"} {s["exlabel"]}, the exaltation, on average.'
    return f'Shaded box: {s["exlabel"]}, the midpoint of the two exaltations, on average.'
def yl(s):
    u='boxes' if s['slow'] else 'd'; d=s['des']
    return f"short year {d['d']} {u} · long year {d['d']+1} {u} · hour step +{d['s']}"
def fields_line(c,s,x,y,size=10,boxes_same_line=False):
    d=s['des']; u='boxes' if s['slow'] else 'd'
    c.setFont('DejaVuSans',size)
    items=['Year (Folvasin):','Gregorian date:','New year hour:']; xx=x
    for t in items:
        c.drawString(xx,y,t); w=sw(t,'DejaVuSans',size); c.setLineWidth(0.5); c.line(xx+w+4,y-2,xx+w+4+size*10,y-2); xx+=w+size*12
    return xx
def checkboxes(c,s,x,y,size=10):
    d=s['des']; u='boxes' if s['slow'] else 'd'; c.setFont('DejaVuSans',size); c.setLineWidth(0.6)
    xx=x
    for t in [f"short year ({d['d']} {u})",f"long year ({d['d']+1} {u})"]:
        c.rect(xx,y-1,size*1.1,size*1.1); c.drawString(xx+size*1.6,y,t); xx+=sw(t,'DejaVuSans',size)+size*4
    fill(c,RED1); stroke(c,REDLINE); c.rect(xx,y,size*0.9,size*0.9,fill=1); stroke(c,(0,0,0)); fill(c,(0,0,0))
    c.setFont('DejaVuSans',size*0.8); c.drawString(xx+size*1.4,y+1,shaded(s))
