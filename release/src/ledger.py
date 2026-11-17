"""The year ledger of every sheet, and everything cut from it: date -> box, year starts, month starts."""
import math, datetime as dt, bisect
import engine2 as E

def nm_date(k): return dt.date.fromordinal(E.moon_month_starts()[k])
def lun_index(date): return E.moon_box(date.toordinal())

class Ledger:
    def __init__(self,s,until=dt.date(2140,1,1)):
        self.s=s; d=s['des']; self.d=d['d']; self.slow=s['slow']
        self.months=s['months']; self.cum=[0]
        for m in self.months: self.cum.append(self.cum[-1]+m)
        st=s['start']; A=st['hour']-1
        if self.slow:
            base=st['k']
        else:
            base=st['date'].toordinal()
        self.starts=[]; self.hours=[]; y=1
        while True:
            u=base+A//24
            self.starts.append(u); self.hours.append(A%24+1)
            date=nm_date(u) if self.slow else dt.date.fromordinal(u)
            if date>until: break
            A+=E.year_hours(d,y); y+=1
    def start_date(self,y):
        u=self.starts[y-1]; return nm_date(u) if self.slow else dt.date.fromordinal(u)
    def unit_of(self,date): return lun_index(date) if self.slow else date.toordinal()
    def locate(self,date):
        """-> (own year, box in year, month, day-in-month, intercalary?)"""
        u=self.unit_of(date); i=bisect.bisect_right(self.starts,u)-1
        y=i+1; box=u-self.starts[i]+1; L=self.starts[i+1]-self.starts[i]
        assert 1<=box<=L and L in (self.d,self.d+1),(self.s['code'],date,box,L)
        if box==self.d+1:
            return y,box,len(self.months),self.months[-1]+1,True
        m=bisect.bisect_left(self.cum,box)   # month index 1-based
        return y,box,m,box-self.cum[m-1],False
    def is_tier_year(self,y): return any(y%N==0 for N,c in self.s['des']['tiers'])
    def month_start_dates(self,y):
        """real date on which each month of own year y begins"""
        out=[]
        for m in range(len(self.months)):
            u=self.starts[y-1]+self.cum[m]
            out.append(nm_date(u) if self.slow else dt.date.fromordinal(u))
        return out
    def year_of(self,date): return self.locate(date)[0]
    def box_starts_in_year(self,Y):
        """slow sheets: (date, new-year?) for every box start in Gregorian year Y"""
        k=lun_index(dt.date(Y,1,1)); out=[]
        while True:
            k+=1; d=nm_date(k)
            if d.year>Y: break
            out.append((d,k in self.starts))
        return out
    def year_starts_in(self,Y):
        out=[]
        for i,u in enumerate(self.starts):
            d=self.start_date(i+1)
            if d.year==Y: out.append((d,self.hours[i],i+1))
            if d.year>Y: break
        return out

# Folvasin year: the Solar sheet's own year count; year 1 of the Sun sheet (true equinox 2025) is 6912
_SUN=None
def sun_ledger():
    global _SUN
    if _SUN is None: _SUN=Ledger([s for s in E.all_sheets() if s['code']=='DD'][0])
    return _SUN
def folvasin(date):
    L=sun_ledger()
    if date>=L.start_date(1): return 6911+L.year_of(date)
    s=L.s; d=s['des']; A=s['start']['hour']-1; base=s['start']['date'].toordinal(); y=0
    while True:                                # run the Solar ledger backwards (years 0, -1, ...)
        A-=E.year_hours(d,y)
        if base+A//24<=date.toordinal(): return 6911+y
        y-=1

def months_hold_until(s,maxy=20000):
    """first own year in which the apsidal month lengths would change (single planets only)"""
    code=s['code']; b=code[0]
    if code[0]!=code[1] or b not in E.ORBIT: return None
    base=s['months']; P=s['period']; t0=s['start']['jd']; d=s['des']['d']
    import numpy as np
    lo=1; step=1
    def months_at(y):
        jd=t0+(y-1)*P; tt=E.T(jd)
        e0,e1,w0,w1=E.ORBIT[b]; e=e0+e1*tt; w=(w0+w1*tt)%360
        start=(E.EXALT[b]//30)*30
        th=np.radians(start+30*np.arange(13)); nu=th-np.radians(w)
        Ea=np.arctan2(np.sqrt(1-e*e)*np.sin(nu),e+np.cos(nu)); M=Ea-e*np.sin(Ea)
        dM=np.diff(np.unwrap(M)); dM=np.where(dM<0,dM+2*np.pi,dM)
        return E.cumround(dM/(2*np.pi)*d)
    # reference: the months are computed for the epoch; find the first own year after it in which they change
    y0=sun_ledger().year_of(dt.date(2025,12,8)) if code=='DD' else Ledger(s).year_of(dt.date(2025,12,8))
    def at(n):
        jd=E.EPOCH_JD+n*P; tt=E.T(jd)
        e0,e1,w0,w1=E.ORBIT[b]; e=e0+e1*tt; w=(w0+w1*tt)%360
        start=(E.EXALT[b]//30)*30
        th=np.radians(start+30*np.arange(13)); nu=th-np.radians(w)
        Ea=np.arctan2(np.sqrt(1-e*e)*np.sin(nu),e+np.cos(nu)); M=Ea-e*np.sin(Ea)
        dM=np.diff(np.unwrap(M)); dM=np.where(dM<0,dM+2*np.pi,dM)
        return E.cumround(dM/(2*np.pi)*d)
    n=0
    while n<maxy:
        if at(n)!=base: return y0+n
        n+=1 if n<300 else 5
    return None
