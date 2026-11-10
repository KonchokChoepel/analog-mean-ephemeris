import numpy as np
# Standish JPL approx elements, 1800-2050: a,e,I,L,varpi,Omega  + rates per Julian century
EL={
'Mercury':[0.38709927,0.20563593,7.00497902,252.25032350,77.45779628,48.33076593, 0.00000037,0.00001906,-0.00594749,149472.67411175,0.16047689,-0.12534081],
'Venus':[0.72333566,0.00677672,3.39467605,181.97909950,131.60246718,76.67984255, 0.00000390,-0.00004107,-0.00078890,58517.81538729,0.00268329,-0.27769418],
'Earth':[1.00000261,0.01671123,-0.00001531,100.46457166,102.93768193,0.0, 0.00000562,-0.00004392,-0.01294668,35999.37244981,0.32327364,0.0],
'Mars':[1.52371034,0.09339410,1.84969142,-4.55343205,-23.94362959,49.55953891, 0.00001847,0.00007882,-0.00813131,19140.30268499,0.44441088,-0.29257343],
'Jupiter':[5.20288700,0.04838624,1.30439695,34.39644051,14.72847983,100.47390909, -0.00011607,-0.00013253,-0.00183714,3034.74612775,0.21252668,0.20469106],
'Saturn':[9.53667594,0.05386179,2.48599187,49.95424423,92.59887831,113.66242448, -0.00125060,-0.00050991,0.00193609,1222.49362201,-0.41897216,-0.28867794],
'Uranus':[19.18916464,0.04725744,0.77263783,313.23810451,170.95427630,74.01692503, -0.00196176,-0.00004397,-0.00242939,428.48202785,0.40805281,0.04240589],
'Neptune':[30.06992276,0.00859048,1.77004347,-55.12002969,44.96476227,131.78422574, 0.00026291,0.00005105,0.00035372,218.45945325,-0.32241464,-0.00508664],
}
MASS={'Mercury':1/6023600,'Venus':1/408523.71,'Earth':1/332946.05,'Mars':1/3098708,'Jupiter':1/1047.3486,'Saturn':1/3497.898,'Uranus':1/22902.98,'Neptune':1/19412.24}
PREC=1.3969713  # deg/century general precession in longitude
def kep(M,e):
    E=M.copy()
    for _ in range(30): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E
def helio_xyz(name,T):
    a0,e0,I0,L0,w0,O0,da,de,dI,dL,dw,dO=EL[name]
    a=a0+da*T; e=e0+de*T; I=np.radians(I0+dI*T); L=L0+dL*T; w=w0+dw*T; O=O0+dO*T
    M=np.radians(((L-w)+180)%360-180)
    E=kep(M,e)
    x=a*(np.cos(E)-e); y=a*np.sqrt(1-e*e)*np.sin(E)
    om=np.radians(w-O); Or=np.radians(O)
    xp=x*np.cos(om)-y*np.sin(om); yp=x*np.sin(om)+y*np.cos(om)
    X=xp*np.cos(Or)-yp*np.cos(I)*np.sin(Or)*0 
    # full rotation
    cO,sO,cI,sI=np.cos(Or),np.sin(Or),np.cos(I),np.sin(I)
    co,so=np.cos(om),np.sin(om)
    X=(cO*co-sO*so*cI)*x+(-cO*so-sO*co*cI)*y
    Y=(sO*co+cO*so*cI)*x+(-sO*so+cO*co*cI)*y
    Z=(so*sI)*x+(co*sI)*y
    return np.array([X,Y,Z])
def lon(v,T): return (np.degrees(np.arctan2(v[1],v[0]))+PREC*T)%360
def sun_bary(T):
    # Sun's position relative to SSB from astrocentric planet positions (approximation)
    tot=1+sum(MASS.values()); s=np.zeros_like(helio_xyz('Earth',T))
    for n,m in MASS.items(): s=s+m*helio_xyz(n,T)
    return -s/tot   # SSB->Sun vector is -(sum m r)/tot  (r heliocentric)  => SSB = sum m r/tot, Sun=-SSB
def bary_xyz(name,T): return helio_xyz(name,T)+sun_bary(T)
def jd2T(jd): return (jd-2451545.0)/36525
