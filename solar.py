import sys; sys.path.insert(0,'.')
import bisect
from data import *
import apse
_X=build('DD'); _des=_X['des']; _day0=_X['grid'][0]['date']; _c1=_X['c1']
_f,_ev=apse.events('DD',_X)
YMIN,YMAX=-200,4500
A={1:_c1}
for y in range(1,YMAX): A[y+1]=A[y]+hours_of_year(y,_des)
for y in range(0,YMIN-1,-1): A[y]=A[y+1]-hours_of_year(y,_des)
YS=list(range(YMIN,YMAX+1)); NS=[A[y]//24 for y in YS]
def pattern_at(y):
    p=_f
    for e in _ev:
        if e[0]<=y: p=e[2]
    return p
MONS=SIGNS
def solar_of(date):
    n=(date-_day0).days; i=bisect.bisect_right(NS,n)-1; y=YS[i]
    q=n-NS[i]+1; m=pattern_at(y); cum=0
    for k,L in enumerate(m):
        if q<=cum+L: return 6912+y-1,k,q-cum
        cum+=L
    return 6912+y-1,11,m[11]+1       # intercalary day (day after month 12's last)
def sol_str(date,short=True):
    yr,k,dd=solar_of(date); return f"{dd} {MONS[k][:3] if short else MONS[k]}"
def sol_year(date): return solar_of(date)[0]
if __name__=='__main__':
    for dd in (_day0,_day0+dt.timedelta(days=-1),_day0+dt.timedelta(days=365),dt.date(2025,12,8),dt.date(2024,3,8),dt.date(2011,11,10)):
        print(dd,solar_of(dd),sol_str(dd))
