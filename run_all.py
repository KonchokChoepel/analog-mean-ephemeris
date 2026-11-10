import sys,pickle; sys.path.insert(0,'.')
from engine import *
MOONPAIRS=('GD','GF','GE','GC','GB','GA','HGI')
R={}
for no,code,Ps in CAL:
    if code in MOONPAIRS: Peff=Fr(Ps)          # 12 conjunctions per year (sheet period is already 12 cycles)
    elif code=='GG': Peff=Fr(30617314)          # 12 lunations (= 12 x Moon-Sun synodic month)
    else: Peff=Fr(Ps)
    pd=float(Peff)/86400; slow=pd>=SLOW_DAYS; sc=30 if slow else 1
    des=design(Peff,sc); t0=anchor(code,pd)
    od=orb_days('GD' if code=='GG' else code)[0]
    R[code]=dict(no=no,code=code,Ps=float(Peff),slow=slow,sc=sc,des=des,t0=t0,orb=od,err=max_error(des),Pdays=pd)
    d=(dt.datetime(2000,1,1,12)+dt.timedelta(days=t0-2451545)).strftime('%Y-%m-%d %H:%M')
    if code in MOONPAIRS+('GG',): print(no,code,'P=%.4f d'%pd,'d',des['d'],'h',des['h'],'L',des['L'],'tiers',[(t[0],t[1]) if t else None for t in des['tiers']],'start',d,'err %.1f'%R[code]['err'],'orb %.2f'%od)
pickle.dump(R,open('R.pkl','wb'))
