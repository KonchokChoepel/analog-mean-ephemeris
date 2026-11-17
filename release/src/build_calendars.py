"""A4 black-and-white home-print set: the 36 calendars, two to a page where the boxes stay generous."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import engine2 as E
from a3_draw import *
W,H=A4; M=30; HEAD=34; FOOT=22; GAP=22
MIN_HALF_BOX=14.0
def half_h(): return (H-2*M-FOOT-GAP)/2
def fits_half(s):
    bw,bh,_,_=calendar_fit(s,W-2*M,half_h()-HEAD,3,12,12,False,8); return bh>=MIN_HALF_BOX
def head(c,s,ytop):
    d=s['des']; slow=s['slow']; code=s['code']
    c.setFont('DejaVuSans-Bold',14); c.drawString(M,ytop-13,f"{s['glyphs']}  {s['title'].upper()}".strip())
    c.setFont('DejaVuSans-Bold',14); c.drawRightString(W-M,ytop-13,code)
    u=('GG months' if E.EMP else 'New Moons') if slow else 'days'
    sub=f"{s['no']} of 36  ·  short year {d['d']} {u}  ·  long year {d['d']+1}"
    if slow: sub+=('  ·  1 box = 1 GG month' if E.EMP else '  ·  1 box = 1 New Moon')
    if code=='HH': sub+='  ·  backwards: days count down'
    no_=lambda cd:[x for x in E.all_sheets() if x['code']==cd][0]['no']
    if code=='FD': sub+='  ·  one year = 3 cycles'
    if E.EMP: pass
    elif code in E.SUNPAIR.values(): sub+='  ·  bottom left: distance from the Sun'+('  ·  ☽: Moon days' if code!='DA' else '')
    if not E.EMP and code[0]=='G' and len(code)==2 and code[1] in E.SUNPAIR and code[1]!='A': sub+=f"  ·  meets on the 1st + ☽ (sheet {no_(E.SUNPAIR[code[1]])})"
    if code=='DH' and not E.EMP: sub+='  ·  ◐ = eclipse season'
    c.setFont('DejaVuSans',7); c.drawString(M,ytop-24,sub)
    lab=('reference day ' if E.EMP else 'exaltation ' if code[0]==code[1] else 'exaltation midpoint ')+s['exlabel']
    xr=W-M-sw(code,'DejaVuSans-Bold',14)-16; c.setFont('DejaVuSans',7)
    tw=sw(lab,'DejaVuSans',7); c.drawRightString(xr,ytop-12,lab)
    c.setLineWidth(1.8); c.rect(xr-tw-11,ytop-13.5,7.5,7.5); c.setLineWidth(0.4)
    c.setLineWidth(0.4); c.line(M,ytop-29,W-M,ytop-29)
def sheet(c,s,ytop,h):
    head(c,s,ytop)
    draw_calendar(c,s,M,ytop-HEAD,W-2*M,h-HEAD,3,small=True,starts=False,hb=12,colgap=12,mono=True,week=False,mingap=8)
def notes(c,s,ytop,h):
    c.setDash(3,3); c.setLineWidth(0.5); c.line(M,ytop+GAP/2,W-M,ytop+GAP/2); c.setDash()
    c.setFont('DejaVuSans-Bold',9); c.drawString(M,ytop-12,f"NOTES  ·  {s['glyphs']} {s['title']}".replace("·  ","· "))
    c.setLineWidth(0.8); c.line(M,ytop-16,W-M,ytop-16)
    n=int((h-30)/19); stp=(h-30)/n
    c.setLineWidth(0.35); c.setDash(0.6,1.6)
    for k in range(1,n+1): y=ytop-16-k*stp; c.line(M,y,W-M,y)
    c.setDash()
def build(out):
    c=canvas.Canvas(out,pagesize=A4); c.setTitle('The 36 Calendar Analog Ephemeris · '+('Empirical Edition · ' if E.EMP else '')+'A4 black and white'); c.setAuthor('Aidan John Walsh')
    S=E.all_sheets(); n=len(S); fit=[fits_half(x) for x in S]
    # pair neighbours so that as few half-size sheets as possible stand alone (order kept)
    best=[0]*(n+2); choice=[1]*(n+2)
    for i in range(n-1,-1,-1):
        a=best[i+1]-(1 if fit[i] else 0)
        b=best[i+2] if i+1<n and fit[i] and fit[i+1] else -99
        best[i],choice[i]=(b,2) if b>=a else (a,1)
    i=0
    while i<len(S):
        if choice[i]==2:
            hh=half_h(); sheet(c,S[i],H-M,hh)
            c.setDash(3,3); c.setLineWidth(0.5); y=H-M-hh-GAP/2; c.line(M,y,W-M,y); c.setDash()
            sheet(c,S[i+1],H-M-hh-GAP,hh); i+=2
        elif fit[i]:
            hh=half_h(); sheet(c,S[i],H-M,hh); notes(c,S[i],H-M-hh-GAP,hh); i+=1
        else:
            sheet(c,S[i],H-M,H-2*M-FOOT); i+=1
        c.setFont('DejaVuSans',5.8); c.drawCentredString(W/2,M-6,'Small number = day of the year. The last box is split: top left ends a short year, bottom right a long one. '+('The letter beside a month is a fixed label counted from the start point.' if E.EMP else 'A sign beside a house counts from the mutual exaltation; it is not where the pair stands.'))
        c.drawCentredString(W/2,M-13,'© 2026 Aidan John Walsh · CC BY-SA 4.0 · github.com/KonchokChoepel/analog-mean-ephemeris')
        c.showPage()
    c.save()
if __name__=='__main__': build(sys.argv[1])
