import sys; sys.path.insert(0,'.')
from almanac import *
HORIZON_YR=5000      # Earth years after the epoch
HYST=0.62
HB=0.12
def elems(b,T):
    nm={'A':'Saturn','B':'Jupiter','C':'Mars','D':'Earth','E':'Venus','F':'Mercury'}[b]; el=EL[nm]
    return el[1]+el[7]*T, (el[4]+(el[10]+PREC)*T+(180 if b=='D' else 0))%360
def raw_lengths(b,T,d):
    e,w=elems(b,T); start=0 if b=='D' else EXALT[b]
    th=np.radians(start+30*np.arange(13)); nu=th-np.radians(w)
    E=np.arctan2(np.sqrt(1-e*e)*np.sin(nu),e+np.cos(nu)); M=np.unwrap(E-e*np.sin(E))
    dM=np.diff(M); dM=np.where(dM<0,dM+2*np.pi,dM)
    return dM/(2*np.pi)*d
def apse_month(b,T):
    e,w=elems(b,T); start=0 if b=='D' else EXALT[b]
    p=int(((w-start)%360)//30)+1; return p,(p+5)%12+1     # perigee month, apogee month
def events(code,X):
    b=code[0]; d=X['des']['d']; Pd=float(X['Pdays']) if 'Pdays' in X else None
    Pd=X['Pdays']; Te=jd2T(EPOCH_JD); ymax=int(HORIZON_YR*365.25/Pd)
    cur=cumround(list(raw_lengths(b,Te,d))); first=list(cur); ev=[]
    for y in range(2,ymax+1):
        T=Te+(y-1)*Pd/36525; r=raw_lengths(b,T,d)
        if max(abs(np.cumsum(r)[i]-np.cumsum(cur)[i]) for i in range(12))>0.5+HB:
            new=cumround(list(r))
            if new!=cur:
                earth=2025.93+(y-1)*Pd/365.25
                ev.append((y,int(earth)+4887,list(new),[new[i]-cur[i] for i in range(12)])); cur=new
    return first,ev
if __name__=='__main__':
    for code in SINGLE_ECC:
        X=build(code); f,ev=events(code,X); T0=jd2T(EPOCH_JD)
        print(code,X['des']['d'],f,'apse months(peri,apo)',apse_month(code[0],T0),'events',len(ev))
        for e in ev[:3]: print('   ',e[0],e[1],e[3])
