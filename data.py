import sys,pickle; sys.path.insert(0,'.')
from engine import *
import os
R=pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'R.pkl'),'rb'))   # made by run_all.py
MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def jd2dt(jd): return dt.datetime(2000,1,1,12)+dt.timedelta(days=jd-2451545)
def fmt(d): return f"{d.day} {MON[d.month-1]} {d.year}"
SINGLE_ECC=('DD','FF','EE','CC','BB','AA')
TITLES={'DD':'Solar year','GG':'12 lunations','FF':'Mercurial year','EE':'Venusian year','CC':'Martian year','BB':'Jovian year','AA':'Saturnine year','HI':'Nodal cycle'}
def build(code):
    r=R[code]; des=r['des']; slow=r['slow']; d=des['d']; t0=r['t0']; bs=bodies(code)
    out=dict(r); out['bs']=bs
    if code in SINGLE_ECC:
        start=0 if code=='DD' else EXALT[code[0]]
        arcs,e=ecc_arcs(code,start); months=cumround([a*d/sum(arcs) for a in arcs]); first=int(start//30); kind='ecc'
        out['raw_arcs']=[a*float(des['p']) for a in arcs]
    elif code in('GG','HI'):
        months=bresenham(d); first=int(EXALT[code[0]]//30); kind='equal'
    else:
        months=bresenham(d); first=midpoint_sign(code)[0]; kind='equal'
    out['months']=months; out['first']=first; out['kind']=kind
    out['moonpair']=code in ('GD','GF','GE','GC','GB','GA','HGI')
    out['houses']=(len(bs)==2 and not out['moonpair'])
    if len(bs)==2 and not out['moonpair']:
        fast,slow_=sorted(bs,key=lambda b:-abs(motion(b)))
        out['fast']=fast; out['slowb']=slow_; out['back']=(fast=='H')
    # clock origin
    if not slow:
        x=jd2dt(t0+0.25); h=x.hour+x.minute/60+x.second/3600; c1=int(round(h)); day0=x.date()
        if c1==24: c1=0; day0=day0+dt.timedelta(days=1)
        datef=lambda N: day0+dt.timedelta(days=int(N))
    else:
        c1=0; datef=lambda N: jd2dt(t0+30*N+0.25).date()
    out['c1']=c1
    cum=0; starts=[]; 
    for m in months: starts.append((cum+1,cum+m,datef(cum))); cum+=m
    out['mrows']=starts
    sim=simulate(des,c1,100); grid=[]
    for y,(A,A2) in enumerate(sim,1):
        N=A//24; c=A%24; L_=A2//24-N
        fired=[i+1 for i,t in enumerate(des['tiers']) if t and y%t[0]==0]
        grid.append(dict(y=y,len=L_,hr=c,fired=fired,date=datef(N) if not slow else jd2dt(t0+30*A/24+0.25).date()))
    out['grid']=grid
    od=r['orb']; out['orb_d']=math.ceil(od) if od>1 else 1
    out['acc']=max(1,math.ceil(r['err']/24-1e-9))
    return out
