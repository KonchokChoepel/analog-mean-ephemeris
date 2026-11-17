"""Independent check: recount every Date Finder cell from the printed rules (no ledger code), and compare
with the text actually printed in the A3 pack."""
import datetime as dt, re, subprocess, sys
import engine2 as E
S=E.all_sheets(); BY={s['code']:s for s in S}

def rule_starts(s, n_back=0, n_fwd=400):
    """year starts as (unit, hour) by the printed rule: hours 1-24, add step (+tiers); over 24 -> long."""
    d=s['des']; st=s['start']
    u0=st['date'].toordinal() if not s['slow'] else None
    H=st['hour']; out={1:(0,H)}; off=0
    for y in range(1,n_fwd):
        tot=H+d['s']+sum(c for N,c in d['tiers'] if y%N==0); extra=0
        while tot>24: tot-=24; extra+=1
        off+=d['d']+extra; H=tot; out[y+1]=(off,H)
    off=0; H=st['hour']
    for y in range(0,-n_back,-1):          # backwards: find the H that steps to the known one
        corr=sum(c for N,c in d['tiers'] if y%N==0) if y!=0 else sum(c for N,c in d['tiers'])
        for Hp in range(1,25):
            tot=Hp+d['s']+corr; extra=0
            while tot>24: tot-=24; extra+=1
            if tot==H: break
        off-=d['d']+extra; H=Hp; out[y]=(off,H)
    return out

# Moon-sheet month starts, from the Moon sheet alone (forward and back)
moon=BY['GG']; mstarts=rule_starts(moon,n_back=450,n_fwd=200); m0=moon['start']['date'].toordinal(); cum=[0]
for m in moon['months'][:-1]: cum.append(cum[-1]+m)
MM=sorted(m0+o+c for y,(o,h) in mstarts.items() for c in cum)
def lun(o):
    import bisect; return bisect.bisect_right(MM,o)-1

def count(s,date):
    st=s['start']; ys=rule_starts(s,n_fwd=600)
    if s['slow']:
        k1=lun(st['date'].toordinal()); u=lun(date.toordinal())-k1
    else:
        u=date.toordinal()-st['date'].toordinal()
    best=None
    for y,(o,h) in ys.items():
        if o<=u: best=(y,o)
    y,o=best; box=u-o+1; nxt=ys[y+1][0]-o
    ms=s['months']; d=s['des']['d']
    if box==d+1: m=len(ms); dd=ms[-1]+1; ic=True
    else:
        m=1; acc=0
        while box>acc+ms[m-1]: acc+=ms[m-1]; m+=1
        dd=box-acc; ic=False
    if s['code']=='HH': dd=0 if ic else ms[m-1]-dd+1
    return f'{m}·{dd}'+('+' if ic else '')

# expected cells
MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
bad=0; checked=0
pdf=sys.argv[1]
for s in S:
    page=6+2*s['no']                     # back page number
    txt=subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-x','0','-y','0','-W','745','-H','842','-layout',pdf,'-'],capture_output=True,text=True).stdout
    lines=txt.splitlines()
    i0=[i for i,l in enumerate(lines) if re.match(r'^\s*1\s+\d+·',l)][0]
    for r in range(31):
        cells=re.findall(r'\d+·\d+\+?',lines[i0+r] if re.match(rf'^\s*{r+1}\s',lines[i0+r]) else '')
        # expected, skipping non-existent dates
        exp=[]
        yy,mm=2026,11
        for j in range(24):
            try: exp.append(count(s,dt.date(yy,mm,r+1)))
            except ValueError: pass
            mm+=1
            if mm>12: mm=1; yy+=1
        checked+=len(exp)
        if cells!=exp:
            bad+=1; print('MISMATCH',s['code'],'row',r+1,cells[:6],exp[:6]); break
print(f'Date Finder cells checked: {checked}, mismatched rows: {bad}')
