import sys; sys.path.insert(0,'.')
import datetime as dt, bisect, math
from almanac import *   # fonts etc, ordn, PACKS
import apse
NOW=dt.datetime.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else dt.datetime(2026,11,10,19,58,0)   # UTC; pass e.g. 2027-01-01T18:00:00
JD=(NOW-dt.datetime(2000,1,1,12)).total_seconds()/86400+2451545
sh=NOW+dt.timedelta(hours=6)
rows=[]
for no,code,_ in CAL:
    X=build(code); des=X['des']; c1=X['c1']; slow=X['slow']; t0=X['t0']
    ecc=code in SINGLE_ECC
    if ecc: f0,ev=apse.events(code,X)
    def pat(y):
        if not ecc: return X['months']
        p=f0
        for e in ev:
            if e[0]<=y: p=e[2]
        return p
    if slow:
        H=(JD-t0)*24/30; n=int(H//24); hour=H%24
    else:
        day0=X['grid'][0]['date']; n=(sh.date()-day0).days; hour=sh.hour+sh.minute/60
    # find own year y
    A=c1; y=1; Ns=[]
    while True:
        A2=A+hours_of_year(y,des)
        if (A//24)<=n<(A2//24): break
        A=A2; y+=1
        if y>100000: raise SystemExit('no year found for '+code)
    Ny=A//24; ln=A2//24-Ny; q=n-Ny+1; m=pat(y); cum=0; k=None
    for i,L in enumerate(m):
        if q<=cum+L: k=i; dd=q-cum; break
        cum+=L
    if k is None: k=11; dd=m[11]+1
    sign=SIGNS[(X['first']+k)%12]
    rows.append((no,code,y,k+1,sign,dd,q,ln,des['d'],hour,X['houses'],X.get('moonpair',False),slow,X['bs']))
    print(no,code,'yr',y,'month',k+1,sign,'day',dd,'(doy %d of %d)'%(q,ln),'hour %.1f'%hour)
import pickle; pickle.dump(rows,open('now36.pkl','wb'))
