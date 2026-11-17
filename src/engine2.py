"""The 36 Calendar Analog Ephemeris — engine v2.

One model for every printed document. Rules (SPECIFICATION):
- Mean (heliocentric/barycentric) tropical periods; retrogrades and stations live inside the orb.
- Short year = whole days (or whole New Moons on slow sheets); the leftover hours rotate the
  new-year hour by a step built on the nearest whole-number factor of 24; when 24 hours have
  accumulated the year is long (intercalary day = last box of month 12).
- Up to three correction tiers, each always equal to that sheet's own factor.
- Slow sheets (cycle > 1000 days): 1 box = 1 lunation; boxes are crossed off at each New Moon.
- Day begins 18:00 (symbolic, the same everywhere). Hours are numbered 1-24 from 18:00.
- Order: Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn, then the Nodes.
"""
import math, itertools, os, datetime as dt
from fractions import Fraction as Fr
import numpy as np
import swisseph as swe

# ---------------- constants
J2000 = 2451545.0
EPOCH_JD = 2461018.19          # heliocentric Saturn-Neptune conjunction, 8 Dec 2025
SYNODIC = Fr(29530588853, 10**9)   # mean lunation, days
SLOW_DAYS = 1000
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_GLYPH = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓']
ORDER = ['G','F','E','D','C','B','A','H']
VISIBLE_WITH_SUN = ('D','F','E')      # Moon pairs counted as lunations
RADIUS = {'F':0.387098,'E':0.723332,'C':1.523679,'B':5.202603,'A':9.554909}   # mean orbital radii (AU)            # Moon -> Saturn, Nodes last
NAMES = {'G':'Moon','F':'Mercury','E':'Venus','D':'Sun','C':'Mars','B':'Jupiter','A':'Saturn','H':'Nodes'}
GLYPH = {'G':'☽','F':'☿','E':'♀','D':'☉','C':'♂','B':'♃','A':'♄','H':'☊'}
EXALT = {'D':19,'G':33,'C':298,'F':165,'B':105,'E':357,'A':201,'H':63}
# mean longitudes of date (Meeus / Simon et al. 1994): deg, deg per Julian century
MEAN = {'F':(252.250906,149474.0722491),'E':(181.979801,58519.2130302),'D':(280.466457,36000.7698278),
        'C':(355.433000,19141.6964471),'B':(34.351519,3036.3027748),'A':(50.077444,1223.5110686),
        'G':(218.3164477,481267.88123421),'H':(125.0445479,-1934.1362891)}
# eccentricity and longitude of perihelion of date (Meeus table 31.A); Sun uses Earth's +180
ORBIT = {'F':(0.20563175,0.000020406,77.456119,1.5564775),'E':(0.00677188,-0.000047766,131.563707,1.4022188),
         'D':(0.01670862,-0.000042037,102.937348+180,1.7195269),'C':(0.09340062,0.000090483,336.060234,1.8410331),
         'B':(0.04849485,0.000163244,14.331309,1.6126668),'A':(0.05550862,-0.000346818,93.056787,1.9637694)}
# ---------------- empirical (blind) edition: same numbers, codes only
EMP = os.environ.get('AME_EDITION','')=='empirical'
LETTERS = list('abcdefghijkl')
if EMP:
    SIGNS = LETTERS[:]; SIGN_GLYPH = LETTERS[:]
    NAMES = {b:b for b in NAMES}; GLYPH = {b:'' for b in GLYPH}
SWE = {'F':swe.MERCURY,'E':swe.VENUS,'C':swe.MARS,'B':swe.JUPITER,'A':swe.SATURN}
LUT = {0:1,1:1,2:2,3:3,4:4,5:6,6:6,7:8,8:8,9:8,10:12,11:12,12:12,13:12,14:-8,15:-8,16:-8,17:-6,18:-6,19:-4,20:-4,21:-3,22:-2,23:-1}

def T(jd): return (jd-J2000)/36525
def wrap(x): return ((x+180)%360)-180
def geo_offsets(b,sep):
    """for mean separation sep = planet - Sun (deg): (distance from the Sun seen from Earth, shift from the mean planet)"""
    a=RADIUS[b]; th=math.radians(sep)
    g=math.degrees(math.atan2(a*math.sin(th),a*math.cos(th)+1))
    return g, wrap(g-sep)
def elongation(b,theta):
    """mean distance from the Sun seen from Earth (deg, + east / evening), theta = mean separation planet - Sun"""
    return geo_offsets(b,theta)[0]
SUNPAIR={'F':'FD','E':'ED','C':'DC','B':'DB','A':'DA'}
def sunpair_sep(s,t):
    """mean planet - Sun separation (deg) at box t (0-based) of a Sun-planet sheet"""
    code=s['code']; P=s['period']/s['cycles']; ph=360*(((t+0.5)/P)%1)
    return ph if code in ('FD','ED') else -ph            # Mercury, Venus run ahead of the Sun; Sun runs ahead of Mars, Jupiter, Saturn
def box_elong(s,t):
    """distance from the Sun for box t on a Sun-planet sheet: '18E', '22W', '180' or '0'"""
    b=s['code'][0] if s['code'] in ('FD','ED') else s['code'][1]
    e=elongation(b,sunpair_sep(s,t)); v=int(round(abs(e)))
    if v==0: return '0'
    if v>=180: return '180'
    return f"{v}{'E' if e>0 else 'W'}"
ECLIPSE_LIMIT=18.0
def box_eclipse(s,t):
    """Sun-Nodes: True if the Sun stands within the eclipse limit of either Node in box t"""
    P=s['period']; th=360*(((t+0.5)/P)%1)
    return min(th,abs(th-180),360-th)<=ECLIPSE_LIMIT
def box_moonshift(s,t):
    """days to move the Moon's meeting with this planet from the 1st of the Moon-planet month"""
    b=s['code'][0] if s['code'] in ('FD','ED') else s['code'][1]
    e,dlt=geo_offsets(b,sunpair_sep(s,t))
    if b in ('F','E'): d=e/(rate('G')-rate('D'))      # the Moon-planet month begins at the New Moon
    else: d=dlt/(rate('G')-rate(b))                   # the Moon-planet month begins at the mean meeting
    return int(round(d))
def visible_lon(b,jd):
    return (mean_lon('D',jd)+elongation(b,mean_lon(b,jd)-mean_lon('D',jd)))%360
def mean_lon(b,jd):
    a,n = MEAN[b]; return (a+n*T(jd))%360
def rate(b): return MEAN[b][1]/36525          # deg/day, of date (tropical)
def true_lon(b,jd):
    if b=='D': return swe.calc_ut(jd,swe.SUN,swe.FLG_MOSEPH)[0][0]
    return swe.calc_ut(jd,SWE[b],swe.FLG_MOSEPH|swe.FLG_HELCTR)[0][0]

# ---------------- the 36 sheets
def sheets():
    out=[(b+b) for b in ORDER]
    out+=[ORDER[i]+ORDER[j] for i in range(8) for j in range(i+1,8)]
    return out
def bodies(code): return [code[0]] if code[0]==code[1] else [code[0],code[1]]
def title(code):
    if EMP: return f'Cycle {code}'
    bs=bodies(code); return ' – '.join(NAMES[b] for b in bs)
def glyphs(code): return ''.join(GLYPH[b] for b in bodies(code))

def period_days(code):
    bs=bodies(code)
    if code=='GG': return 12*SYNODIC
    if code=='HH': return Fr(36525*360)/Fr(abs(MEAN['H'][1])).limit_denominator(10**12)
    if len(bs)==1: return Fr(36525*360)/Fr(MEAN[bs[0]][1]).limit_denominator(10**12)
    a,b=bs; rel=Fr(MEAN[a][1]).limit_denominator(10**12)-Fr(MEAN[b][1]).limit_denominator(10**12)
    if a=='G' and b in VISIBLE_WITH_SUN: return 12*SYNODIC   # seen from Earth, Mercury and Venus keep to the Sun
    P=Fr(36525*360)/abs(rel)
    if a=='G': return 12*P                 # Moon pairs: 12 conjunctions a year
    if code=='FD': return 3*P              # Sun-Mercury: 3 cycles a year
    return P
def cycles_per_year(code):
    if code[0]=='G' and code!='GG': return 12
    if code=='FD': return 3
    return 1
def is_slow(code): return period_days(code)>SLOW_DAYS
def unit(code): return SYNODIC if is_slow(code) else Fr(1)     # days per box

# ---------------- whole-number scheme
def factor_of(hrs):
    if hrs>=Fr(47,2): return 24           # nearest factor is 24 itself (Venus-Jupiter)
    return LUT[int(hrs)]
def _tiers(hrs,L,s,modes):
    drift=hrs-s; tiers=[]
    for m in modes:
        if drift==0: tiers.append(None); continue
        x=Fr(abs(L))/abs(drift)
        N=max(1,int(x//1) if m=='f' else -int(-x//1) if m=='c' else int(x+Fr(1,2)))
        corr=abs(L) if drift>0 else -abs(L)
        tiers.append((N,corr)); drift-=Fr(corr,N)
    return tiers
def max_error(p,d,s,tiers,Y=40000):
    ys=np.arange(1,Y+1,dtype=np.int64); inc=np.full(Y,24*d+s,dtype=np.float64)
    for t in tiers:
        if t: inc+=(ys%t[0]==0)*t[1]
    A=np.concatenate([[0],np.cumsum(inc)]); true=np.arange(Y+1)*float(p)*24
    return float(np.abs(A-true).max())
def design(code):
    p=period_days(code)/unit(code); d=p.numerator//p.denominator; hrs=(p-d)*24
    L=factor_of(hrs); s=L if L>0 else 24+L
    if hrs<Fr(1,2): L,s=1,0                 # almost nothing left over: no step, factor 1
    best=None
    for modes in (['ccc'] if s==0 else itertools.product('fc',repeat=3)):
        t=_tiers(hrs,L,s,modes); ns=[x[0] for x in t if x]
        if s==0 and any(x and x[1]<0 for x in t): continue
        if ns and ns[0]<2: continue
        if any(b<4*a for a,b in zip(ns,ns[1:])): continue
        e=max_error(p,d,s,t)
        if best is None or e<best[0]-1e-9: best=(e,t)
    if best is None: t=_tiers(hrs,L,s,'rrr'); best=(max_error(p,d,s,t),t)
    tiers=[x for x in best[1] if x and x[0]<10**13]
    return dict(p=p,d=d,hrs=hrs,L=L,factor=abs(L),s=s,tiers=tiers,err_h=best[0])
def year_hours(des,y):
    tot=24*des['d']+des['s']
    for N,c in des['tiers']:
        if y%N==0: tot+=c
    return tot

# ---------------- anchors (the start of year 1: last event before the epoch)
def find_last(f,jd_end,span,n=4000):
    jds=np.linspace(jd_end-span,jd_end,n); v=np.array([f(j) for j in jds])
    idx=[i for i in range(n-1) if v[i]<0<=v[i+1] and abs(v[i])<90 and abs(v[i+1])<90]
    i=idx[-1]; a,b=jds[i],jds[i+1]
    for _ in range(60):
        m=(a+b)/2
        if f(m)<0: a=m
        else: b=m
    return (a+b)/2
def conj_lon(x,y,t):
    """where a pair meets: the slower body's mean position (the node's for a Node pair)"""
    return mean_lon(y,t)
def anchor(code):
    """Year 1 begins at the last event before the epoch: a single body entering the sign of its exaltation;
    a pair meeting in the sign of its mutual exaltation (the midpoint of the two exaltations)."""
    bs=bodies(code); P=float(period_days(code))/cycles_per_year(code)
    if len(bs)==1:
        b=bs[0]; tgt=(EXALT[b]//30)*30
        if b=='G':
            f=lambda j: wrap(mean_lon('G',j)-mean_lon('D',j)); jd_end=EPOCH_JD
            for _ in range(60):
                t=find_last(f,jd_end,40)
                if int(mean_lon('D',t)//30)==1: return t
                jd_end=t-1
            raise RuntimeError(code)
        if b=='H': return find_last(lambda j: wrap(tgt+30-mean_lon('H',j)),EPOCH_JD,P*1.05)  # enters Gemini backwards
        return find_last(lambda j: wrap(true_lon(b,j)-tgt),EPOCH_JD,P*1.05,n=8000 if P>3000 else 4000)
    x,y=bs; sign=int(midpoint(code)//30)
    if x=='G' and y in ('F','E'):
        # the lunation in which the Moon meets the planet as seen from Earth in the mutual-exaltation sign;
        # the month begins at the mean New Moon, the meeting follows it by distance-from-the-Sun / 12 days
        f=lambda j: wrap(mean_lon('G',j)-mean_lon('D',j)); jd_end=EPOCH_JD
        for _ in range(400):
            t=find_last(f,jd_end,40)
            meet=t
            for _ in range(20): meet=t+elongation(y,mean_lon(y,meet)-mean_lon('D',meet))/(rate('G')-rate('D'))
            if int(visible_lon(y,meet)//30)==sign: return t
            jd_end=t-1
        raise RuntimeError(code)
    f=lambda j: wrap(mean_lon(x,j)-mean_lon(y,j)); jd_end=EPOCH_JD
    for _ in range(2000):
        t=find_last(f,jd_end,P*1.1+5)
        if int(conj_lon(x,y,t)//30)==sign: return t
        jd_end=t-min(P*0.5,1)
    raise RuntimeError(code)

# the mean New Moon grid that carries the slow sheets
NM0 = None
def new_moon_before(jd):
    global NM0
    if NM0 is None: NM0=find_last(lambda j: wrap(mean_lon('G',j)-mean_lon('D',j)),EPOCH_JD,40)
    k=math.floor((jd-NM0)/float(SYNODIC)); return NM0+k*float(SYNODIC)

def civil(jd):
    """symbolic civil day and hour (1-24): the day begins at 18:00 and takes the date it ends in"""
    x=jd+0.5+0.25   # JD -> days from midnight, +6 h
    d=math.floor(x); frac=x-d
    date=dt.date(2000,1,1)+dt.timedelta(days=d-2451545)
    return date,int(frac*24)+1,frac
# the Moon sheet's month starts carry the slow sheets: one box = one Moon-sheet month
MOON_MONTHS=None
def moon_month_starts():
    """ordinals of every Moon-sheet month start, its ledger run back and forward (years <=0 use the same rules)"""
    global MOON_MONTHS
    if MOON_MONTHS is None:
        code='GG'; des=design(code); m=months(code); cum=np.cumsum([0]+m[:-1])
        t=anchor(code); date,h,_=civil(t); D1=date.toordinal(); A=h-1
        ys={1:A}; a=A
        for y in range(1,260): a+=year_hours(des,y); ys[y+1]=a
        a=A
        for y in range(0,-420,-1): a-=year_hours(des,y); ys[y]=a
        out=[]
        for y in sorted(ys):
            if y+1 not in ys: break
            st=D1+ys[y]//24; nxt=D1+ys[y+1]//24
            out+=[st+int(c) for c in cum]
        MOON_MONTHS=sorted(set(out))
    return MOON_MONTHS
def moon_box(ordinal):
    import bisect
    mm=moon_month_starts(); return bisect.bisect_right(mm,ordinal)-1
def start_of(code):
    t=anchor(code)
    if is_slow(code):
        date,_,frac=civil(t); o=date.toordinal(); mm=moon_month_starts(); k=moon_box(o)
        start=mm[k]; length=mm[k+1]-mm[k]; f=((o-start)+frac)/length
        return dict(jd=t,date=dt.date.fromordinal(start),hour=int(f*24)+1,new_moon=True,k=k)
    date,h,_=civil(t); return dict(jd=t,date=date,hour=h,new_moon=False)

# ---------------- months
def cumround(raw):
    cum=np.cumsum(np.asarray(raw,dtype=float)); b=np.rint(cum).astype(int)
    return [int(x) for x in np.diff(np.concatenate([[0],b]))]
def bresenham(total,parts=12):
    base,ex=divmod(total,parts); return [base+(1 if ((k+1)*ex)//parts-(k*ex)//parts else 0) for k in range(parts)]
def kepler_fracs(b,start_deg):
    e0,e1,w0,w1=ORBIT[b]; tt=T(EPOCH_JD); e=e0+e1*tt; w=(w0+w1*tt)%360
    th=np.radians(start_deg+30*np.arange(13)); nu=th-np.radians(w)
    E=np.arctan2(np.sqrt(1-e*e)*np.sin(nu),e+np.cos(nu)); M=E-e*np.sin(E)
    dM=np.diff(np.unwrap(M)); dM=np.where(dM<0,dM+2*np.pi,dM)
    return dM/(2*np.pi), e, w
def time_to(b,start_deg,deg,P):
    """mean time (days) from true ingress at start_deg to true longitude deg"""
    e0,e1,w0,w1=ORBIT[b]; tt=T(EPOCH_JD); e=e0+e1*tt; w=(w0+w1*tt)%360
    def M(th):
        nu=math.radians(th-w); E=math.atan2(math.sqrt(1-e*e)*math.sin(nu),e+math.cos(nu)); return E-e*math.sin(E)
    dM=(M(deg)-M(start_deg))%(2*math.pi); return dM/(2*math.pi)*P
def midpoint(code):
    a,b=EXALT[code[0]],EXALT[code[1]]; return (a+wrap(b-a)/2)%360
def months(code):
    des=design(code); d=des['d']; bs=bodies(code)
    if len(bs)==1 and bs[0] in ORBIT:
        fr,_,_=kepler_fracs(bs[0],(EXALT[bs[0]]//30)*30); return cumround(fr*d)
    n=36 if code=='FD' else 12
    # equal months placed as close as possible to the mean cycle (the year starts, on average, half-way through box 1)
    P=float(period_days(code)/unit(code))
    cut=[int(math.floor(0.5+k*P/n)) for k in range(1,n)]+[d]
    return [b-a for a,b in zip([0]+cut[:-1],cut)]
def month_names(code):
    bs=bodies(code)
    if EMP:
        n=36 if code=='FD' else 12
        if len(bs)==1:
            s0=EXALT[bs[0]]//30; sg=-1 if bs[0]=='H' else 1
        else: s0=int(midpoint(code)//30); sg=1
        return [(f'Month {k+1}',LETTERS[(s0+sg*k)%12]) for k in range(n)]
    if len(bs)==1:
        s0=EXALT[bs[0]]//30
        if bs[0]=='H': return [(f'{ORD[k]} · {SIGNS[(s0-k)%12]}',None) for k in range(12)]
        return [(f'{ORD[k]} · {SIGNS[(s0+k)%12]}',None) for k in range(12)]
    s0=int(midpoint(code)//30); word='month' if code[0]=='G' else 'house'
    n=36 if code=='FD' else 12
    if code=='FD': return [(f'{k+1} · {ORD[k%12]} house',SIGN_GLYPH[(s0+k)%12]) for k in range(n)]
    return [(f'{ORD[k%12]} {word}',SIGN_GLYPH[(s0+k)%12]) for k in range(n)]
ORD=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th']

def exalt_box(code):
    """box in month 1 holding the whole day in which the event falls, on average
    (the year starts, on average, half-way through box 1)."""
    bs=bodies(code); m=months(code); u=float(unit(code))
    if len(bs)==1:
        b=bs[0]; deg=EXALT[b]; s0=(deg//30)*30
        if b in ORBIT: t=time_to(b,s0,deg,float(period_days(code)))/u
        elif b=='G': t=(deg-s0)/30*m[0]
        else: t=(s0+30-deg)/30*m[0]      # Nodes: backwards from 30° of the sign
        label=f'{deg-s0}° {SIGNS[deg//30]}'
    else:
        mid=midpoint(code); t=(mid%30)/30*m[0]
        dd=mid%30; half=abs(dd-int(dd)-0.5)<1e-9
        deg_txt=(f'{int(dd) or ""}½°' if half else f'{int(dd)}°')
        label=f'{deg_txt} {SIGNS[int(mid//30)]}'
    box=min(m[0],math.floor(t+0.5)+1)
    return box,label,t

# ---------------- orb
def eoc_amp(b):
    if b=='H': return 1.65
    if b=='G': e=0.0549
    else: e0,e1,_,_=ORBIT[b]; e=e0+e1*T(EPOCH_JD)
    M=np.linspace(0,2*np.pi,7201); E=M.copy()
    for _ in range(30): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    nu=2*np.arctan2(np.sqrt(1+e)*np.sin(E/2),np.sqrt(1-e)*np.cos(E/2))
    return float(np.degrees(np.abs(np.unwrap(nu)-M)).max())
MAX_ELONG={'F':28.0,'E':47.0}
MAX_SHIFT={'C':41.0,'B':11.1,'A':6.0}
def orb_days(code):
    bs=bodies(code)
    if code in ('GF','GE'): return (MAX_ELONG[bs[1]]+eoc_amp('G'))/(rate('G')-rate('D'))
    if code in ('GC','GB','GA'): return (MAX_SHIFT[bs[1]]+eoc_amp('G')+eoc_amp(bs[1]))/(rate('G')-rate(bs[1]))
    A=sum(eoc_amp(b) for b in bs)
    r=abs(rate(bs[0])) if len(bs)==1 else abs(rate(bs[0])-rate(bs[1]))
    return A/r

# ---------------- everything for one sheet
def sheet(code):
    no=sheets().index(code)+1; des=design(code); m=months(code)
    assert sum(m)==des['d'],(code,sum(m),des['d'])
    box,label,t=exalt_box(code)
    return dict(no=no,code=code,title=title(code),glyphs=glyphs(code),des=des,months=m,names=month_names(code),
                slow=is_slow(code),start=start_of(code),exbox=box,exlabel=label,orb=orb_days(code),
                period=float(period_days(code)),cycles=cycles_per_year(code))
ALL=None
def all_sheets():
    global ALL
    if ALL is None: ALL=[sheet(c) for c in sheets()]
    return ALL

if __name__=='__main__':
    import csv,sys
    rows=all_sheets()
    w=csv.writer(open(sys.argv[1] if len(sys.argv)>1 else 'calendars.csv','w',newline=''))
    if EMP:
        w.writerow(['no','code','mean_period_days','box','short_year','long_year','factor_h','step_h','tier1','tier2','tier3','worst_error_hours','year1_start','year1_hour','reference_point','reference_box','month_letters','month_lengths'])
        for r in rows:
            d=r['des']; ts=[f"every {N} yr: {c:+d} h" for N,c in d['tiers']]+['']*3
            w.writerow([r['no'],r['code'],f"{r['period']:.4f}",'GG month' if r['slow'] else 'day',d['d'],d['d']+1,d['factor'],d['s'],*ts[:3],f"{d['err_h']:.1f}",
                        ('GG month of ' if r['start']['new_moon'] else '')+r['start']['date'].isoformat(),r['start']['hour'],r['exlabel'],r['exbox'],
                        ' '.join(g for _,g in r['names']),' '.join(str(x) for x in r['months'])])
        sys.exit()
    w.writerow(['no','code','bodies','mean_period_days','box','short_year','long_year','factor_h','step_h','tier1','tier2','tier3','worst_error_hours','orb_days','year1_start','year1_hour','exaltation','exaltation_box','year_marker','month_lengths','seen_from_earth'])
    no_={r['code']:r['no'] for r in rows}
    def marker(r):
        c=r['code']; b=bodies(c)
        if c=='GG': return 'New Moon with the Sun in Taurus'
        if c=='DD': return 'March equinox (true)'
        if c=='HH': return 'mean North Node enters Gemini'
        if len(b)==1: return f"{NAMES[b[0]]} enters {SIGNS[EXALT[b[0]]//30]} (true, heliocentric)"
        sg=SIGNS[int(midpoint(c)//30)]
        if c in ('GF','GE'): return f"lunation in which the Moon meets {NAMES[b[1]]} in {sg} (seen from Earth)"
        return f"conjunction in {sg} (mean)"
    def sky(r):
        c=r['code']; b=bodies(c)
        if c=='DD': return 'month = Sun sign; day - 1 = degree'
        if c=='GD': return '1st = New Moon; Moon 12 deg east of the Sun per day'
        if c=='HH': return 'month = sign of the North Node'
        if c in SUNPAIR.values(): return 'every box: distance from the Sun (E/W)'+('' if c=='DA' else ' and Moon days')
        if c=='DH': return 'eclipse seasons marked'
        if c[0]=='G' and len(b)==2 and b[1] in SUNPAIR:
            return 'Moon meets planet on the 1st' + ('' if b[1]=='A' else f" + Moon days from sheet {no_[SUNPAIR[b[1]]]}")
        if len(b)==1 and b[0] in SUNPAIR: return f"planet = Sun +/- distance on sheet {no_[SUNPAIR[b[0]]]}"
        return ''
    for r in rows:
        d=r['des']; ts=[f"every {N} yr: {c:+d} h" for N,c in d['tiers']]+['']*3
        w.writerow([r['no'],r['code'],r['title'],f"{r['period']:.4f}",'lunation' if r['slow'] else 'day',d['d'],d['d']+1,d['factor'],d['s'],*ts[:3],
                    f"{d['err_h']:.1f}",f"{r['orb']:.2f}",('New Moon of ' if r['start']['new_moon'] else '')+r['start']['date'].isoformat(),r['start']['hour'],r['exlabel'],r['exbox'],
                    marker(r),' '.join(str(x) for x in r['months']),sky(r)])
        print(r['no'],r['code'],r['title'],round(r['period'],4),d['d'],'s',d['s'],'f',d['factor'],d['tiers'],round(d['err_h'],1),'orb',round(r['orb'],1),r['start']['date'],r['start']['hour'],'ex',r['exlabel'],r['exbox'],r['months'][:3])
