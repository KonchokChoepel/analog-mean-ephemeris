import numpy as np, datetime as dt, math
from fractions import Fraction as Fr
from eph import EL, PREC, helio_xyz, lon, jd2T, kep
EPOCH_JD=2461018.19      # heliocentric Saturn-Neptune conjunction (8 Dec 2025)
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
NAMES={'A':'Saturn','B':'Jupiter','C':'Mars','D':'Sun','E':'Venus','F':'Mercury','G':'Moon','H':'Nodes'}
GLYPH={'A':'♄','B':'♃','C':'♂','D':'☉','E':'♀','F':'☿','G':'☽','H':'☊'}
EXALT={'D':19,'G':33,'C':298,'F':165,'B':105,'E':357,'A':201,'H':63}
SLOW_DAYS=1000
# ---- the 36 calendars: (no, code, period seconds)
CAL=[(1,'DD',31556925),(2,'GG',28327016),(3,'FF',7600530),(4,'EE',19414149),(5,'CC',59355037),(6,'BB',374163408),(7,'AA',928529568),(8,'HI',586956370),
(9,'GD',30617314),(10,'GF',41088279),(11,'GE',32248092),(12,'GC',29500259),(13,'GB',28506865),(14,'GA',28399215),(15,'HGI',28213549),
(16,'DF',10011914),(17,'DE',50453936),(18,'DC',67380924),(19,'DB',34463582),(20,'DA',32667148),(21,'HDI',29946872),
(22,'FE',12490485),(23,'FC',8716724),(24,'FB',7758124),(25,'FA',7663258),(26,'HFI',7503369),
(27,'EC',28850824),(28,'EB',20476616),(29,'EA',19828738),(30,'HEI',18792567),
(31,'CB',70546037),(32,'CA',63408332),(33,'HCI',53904073),(34,'HBI',228501796),(35,'HAI',359624811),(36,'BA',626700929)]
LUT={0:1,1:1,2:2,3:3,4:4,5:6,6:6,7:8,8:8,9:8,10:12,11:12,12:12,13:12,14:-8,15:-8,16:-8,17:-6,18:-6,19:-4,20:-4,21:-3,22:-2,23:-1}
def bodies(code):
    if code in('DD','GG','FF','EE','CC','BB','AA'): return [code[0]]
    if code=='HI': return ['H']
    if code[0]=='H': return ['H',code[1]]
    return [code[0],code[1]]
# ---- mean longitudes (mean equinox of date), degrees
def mean_lon(b,jd):
    T=jd2T(jd)
    if b=='G': return (218.3164477+481267.88123421*T-0.0015786*T*T)%360
    if b=='H': return (125.0445479-1934.1362891*T+0.0020754*T*T)%360
    if b=='D': el=EL['Earth']; return (el[3]+el[9]*T+180+PREC*T)%360
    nm={'A':'Saturn','B':'Jupiter','C':'Mars','E':'Venus','F':'Mercury'}[b]; el=EL[nm]
    return (el[3]+el[9]*T+PREC*T)%360
def true_lon(b,jd):
    T=jd2T(jd)
    if b=='D': return (lon(helio_xyz('Earth',T),T)+180)%360
    nm={'A':'Saturn','B':'Jupiter','C':'Mars','E':'Venus','F':'Mercury'}[b]
    return lon(helio_xyz(nm,T),T)
def wrap(x): return ((x+180)%360)-180
def find_last(fun,jd_end,span,step=None):
    """latest jd<=jd_end where fun crosses 0 (|fun|<90 on both sides)"""
    n=6000; jds=np.linspace(jd_end-span,jd_end,n)
    v=np.array([fun(j) for j in jds])
    idx=[i for i in range(n-1) if v[i]*v[i+1]<=0 and abs(v[i])<90 and abs(v[i+1])<90]
    i=idx[-1]; a,b=jds[i],jds[i+1]; fa=v[i]
    for _ in range(60):
        m=(a+b)/2; fm=fun(m)
        if fa*fm<=0: b=m
        else: a=m; fa=fm
    return (a+b)/2
def anchor(code,P_days):
    bs=bodies(code)
    if code=='GG':
        f=lambda j: wrap(mean_lon('G',j)-mean_lon('D',j)); jd_end=EPOCH_JD
        for _ in range(40):
            t=find_last(f,jd_end,36)
            if 30<=mean_lon('D',t)<60: return t
            jd_end=t-1
        raise RuntimeError('no new moon in Taurus found')
    if len(bs)==1:
        b=bs[0]
        tgt=0.0 if b=='D' else float(EXALT[b])
        f=(lambda j: wrap(true_lon(b,j)-tgt)) if b not in 'GH' else (lambda j: wrap(mean_lon(b,j)-tgt))
        return find_last(f,EPOCH_JD,P_days*1.05)
    x,y=bs
    f=lambda j: wrap(mean_lon(x,j)-mean_lon(y,j))
    return find_last(f,EPOCH_JD,P_days*1.1+5)
# ---- design of whole-number scheme
def _tiers(p,hrs,L,s,modes,scale):
    drift=hrs-s; tiers=[]
    for m in modes:
        if drift==0: tiers.append(None); continue
        x=Fr(abs(L))/abs(drift); N=max(1,int(x//1) if m=='f' else (-int(-x//1)) if m=='c' else int(x+Fr(1,2)))
        corr=abs(L) if drift>0 else -abs(L)
        tiers.append((N,corr,float(abs(drift))*3600*scale)); drift=drift-Fr(corr,N)
    return tiers
def design(P_s,scale):
    import itertools
    p=Fr(P_s,86400*scale); d=p.numerator//p.denominator; f=p-d; hrs=f*24; h=int(hrs)  # floor
    L=LUT[h]; s=L if L>0 else 24+L
    def mk(t): return dict(p=p,d=d,hrs=hrs,h=h,L=L,s=s,K=24//abs(L),tiers=t)
    base=mk(_tiers(p,hrs,L,s,'rrr',scale))
    n1=base['tiers'][0][0] if base['tiers'][0] else 99
    best=None
    for modes in itertools.product('fc',repeat=3):
        t=_tiers(p,hrs,L,s,modes,scale); ns=[x[0] for x in t if x]
        if ns and ns[0]<2 and n1>=2: continue
        if any(b<4*a for a,b in zip(ns,ns[1:])): continue
        e=max_error(mk(t))
        if best is None or e<best[0]-1e-9: best=(e,t)
    if best is None or n1<2: return base
    return mk(best[1])
def hours_of_year(y,des):
    # length of year y (1-indexed) in hours
    tot=24*des['d']+des['s']
    for t in des['tiers']:
        if t and y%t[0]==0: tot+=t[1]
    return tot
def simulate(des,c1,Y):
    A=c1; out=[]
    for y in range(1,Y+1):
        A2=A+hours_of_year(y,des); out.append((A,A2)); A=A2
    return out
def max_error(des,Y=40000):
    ys=np.arange(1,Y+1,dtype=np.int64)
    inc=np.full(Y,24*des['d']+des['s'],dtype=np.float64)
    for t in des['tiers']:
        if t: inc+= (ys%t[0]==0)*t[1]
    A=np.concatenate([[0],np.cumsum(inc)])
    true=np.arange(Y+1)*float(des['p'])*24
    e=A-true
    return float(np.abs(e).max())
# ---- months
def bresenham(total,parts=12):
    base,ex=divmod(total,parts); return [base+(1 if ((k+1)*ex)//parts-(k*ex)//parts else 0) for k in range(parts)]
def largest_remainder(vals,total):
    s=sum(vals); sc=[v*total/s for v in vals]; fl=[int(math.floor(x)) for x in sc]
    rem=total-sum(fl); order=sorted(range(len(sc)),key=lambda i:-(sc[i]-fl[i]))
    for i in order[:rem]: fl[i]+=1
    return fl
def cumround(raw):
    cum=np.cumsum(np.asarray(raw,dtype=float)); b=np.rint(cum).astype(int)
    return [int(x) for x in np.diff(np.concatenate([[0],b]))]
def ecc_arcs(code,start):
    b=code[0]; T=jd2T(EPOCH_JD)
    nm={'A':'Saturn','B':'Jupiter','C':'Mars','D':'Earth','E':'Venus','F':'Mercury'}[b]; el=EL[nm]
    e=el[1]+el[7]*T; w=(el[4]+(el[10]+PREC)*T+(180 if b=='D' else 0))%360
    th=np.radians(start+30*np.arange(13)); nu=th-np.radians(w)
    E=np.arctan2(np.sqrt(1-e*e)*np.sin(nu),e+np.cos(nu)); M=E-e*np.sin(E)
    dM=np.diff(np.unwrap(M)); dM=np.where(dM<0,dM+2*np.pi,dM)
    return list(dM/(2*np.pi)),e
def midpoint_sign(code):
    bs=bodies(code)
    if len(bs)==1: return None
    a,b=EXALT[bs[0]],EXALT[bs[1]]; d=wrap(b-a); mid=(a+d/2)%360
    return int(mid//30), mid
# ---- orb
def eoc_amp(b):
    if b=='H': return 1.65
    if b=='G': e=0.0549
    else:
        nm={'A':'Saturn','B':'Jupiter','C':'Mars','D':'Earth','E':'Venus','F':'Mercury'}[b]; T=jd2T(EPOCH_JD); el=EL[nm]; e=el[1]+el[7]*T
    M=np.linspace(0,2*np.pi,7201); E=kep(M,e); nu=2*np.arctan2(np.sqrt(1+e)*np.sin(E/2),np.sqrt(1-e)*np.cos(E/2))
    return float(np.degrees(np.abs(np.unwrap(nu)-M)).max())
def motion(b):
    if b=='G': return 13.176358
    if b=='H': return -0.0529539
    if b=='D': el=EL['Earth']
    else: el=EL[{'A':'Saturn','B':'Jupiter','C':'Mars','E':'Venus','F':'Mercury'}[b]]
    return (el[9]+PREC)/36525
def orb_days(code):
    bs=bodies(code); A=sum(eoc_amp(b) for b in bs)
    rel=abs(motion(bs[0])) if len(bs)==1 else abs(motion(bs[0])-motion(bs[1]))
    return A/rel,A,rel
