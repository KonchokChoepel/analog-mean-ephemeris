import sys,os,pickle,datetime as dt; sys.path.insert(0,'.')
from almanac import *
rows=pickle.load(open('now36.pkl','rb')); cur={r[1]:r[2] for r in rows}
OUT=sys.argv[1] if len(sys.argv)>1 else 'Year_End_Cards.pdf'
cards=[]
for pack in PACKS:
    for no,code in members(pack):
        X=build(code); G=X['grid']; y=cur[code]; slow=X['slow']; d=X['des']['d']
        rws=[]
        for i in range(y,y+10):
            g=G[i-1]; nxt=G[i]['date']; last=nxt-dt.timedelta(days=30 if slow else 1)
            rws.append((i,g['date'],g['hr'],g['len'],last,g['fired']))
        cards.append((no,code,X,rws))
c=canvas.Canvas(OUT,pagesize=landscape(A4)); c.setTitle('Year-End Cards')
# page 1
c.setFillColor(NAVY); c.rect(M,H-M-50,W-2*M,50,stroke=0,fill=1); c.setFillColor(white)
c.setFont('DVB',22); c.drawString(M+12,H-M-26,"YEAR-END CARDS"); c.setFont('DV',9.5); c.drawString(M+12,H-M-42,"Is the last box of this cycle the short day or the long day? Look it up by date. No counting needed.")
txt=("<b>What a card is.</b> One card per calendar, listing the ten cycles from the one in progress on <b>10 November 2026</b>: when each starts, how long it is, and its last day. "
 "Cards are in almanac order (Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn and Nodes); the number is the Master calendar number.<br/><br/>"
 "<b>How to use one.</b> Keep crossing off boxes as usual. When you reach the end of a cycle, find that cycle's row. If it says <b>S</b> (short), the cycle ends on the top-left number of the split box. If it says <b>L</b> (long), it ends on the bottom-right number, and the next cycle begins the following day. The last-day date is there as a check: if today's date is past it, the cycle has ended. "
 "Grey rows are long years. The hour is when the new year begins, counted from 18:00 UTC. ▲ marks a correction year.<br/><br/>"
 "<b>Dates</b> are Gregorian, and each day begins at 18:00 UTC and carries the date of the day it ends in. On the slow calendars (marked *) one box is 30 real days, so their last-day dates are approximate to within a month.<br/><br/>"
 "<b>When a card runs out,</b> reprint it from the Masters' 100-year grids (the rows are already there), or ask for a fresh set. Month-length changes on the single-planet pages are separate and are listed in the Month-Length Tables.")
para(c,txt,M,H-M-66,W-2*M,sty(10)); c.showPage()
cw=(W-2*M-2*8)/3; ch=(H-2*M-8-18)/2
def card(c,x,y,no,code,X,rws):
    slow=X['slow']; d=X['des']['d']
    c.setStrokeColor(RULE); c.setDash(2,2); c.setLineWidth(.6); c.rect(x,y,cw,ch,stroke=1,fill=0); c.setDash()
    c.setFillColor(NAVY); c.rect(x,y+ch-26,cw,26,stroke=0,fill=1); c.setFillColor(white)
    t1,_=title_of(X); c.setFont('DVB',10.5); c.drawString(x+6,y+ch-17,t1+("*" if slow else ""))
    c.setFont('DVC',8); c.drawRightString(x+cw-6,y+ch-17,f"No. {no} · {code}")
    c.setFillColor(black); c.setFont('DVC',8); c.drawString(x+6,y+ch-38,f"Short year {d} days (S) · long year {d+1} days (L)")
    cols=[("Yr",22),("Starts",64),("Hr",24),("Days",44),("Last day",76)]; tw=sum(w for _,w in cols); x0=x+(cw-tw)/2; yy=y+ch-46; rh=16.5
    c.setFillColor(LB); c.rect(x0,yy-12,tw,12,stroke=0,fill=1); c.setFillColor(black); c.setFont('DVB',7); xs=x0
    for lab,w in cols: c.drawCentredString(xs+w/2,yy-9,lab); xs+=w
    yy-=12
    for k,(i,sd,hr,ln,last,fired) in enumerate(rws):
        longy=ln>d; c.setFillColor(LG if longy else white); c.setStrokeColor(RULE); c.setLineWidth(.3); c.rect(x0,yy-rh,tw,rh,stroke=1,fill=1)
        vals=[str(i),fmt(sd),f"{hr:02d}",f"{ln} {'L' if longy else 'S'}",fmt(last)]
        xs=x0; c.setFillColor(black)
        for j,((lab,w),v) in enumerate(zip(cols,vals)):
            c.setFont('DVCB' if j==3 else 'DVC',7.6); c.drawCentredString(xs+w/2,yy-11,v); xs+=w
        if fired: c.setFont('DVC',6); c.drawString(x0+tw+2,yy-9,'▲')
        if k==0: c.setFont('DVC',6); c.setFillColor(GREY); c.drawRightString(x0-2,yy-9,'now')
        yy-=rh
    c.setFillColor(GREY); c.setFont('DVC',6.2); c.drawString(x+6,y+5,"Cycles listed from the one in progress on 10 Nov 2026" + ("; 1 box = 30 days" if slow else ""))
for pi in range(0,len(cards),6):
    for j,(no,code,X,rws) in enumerate(cards[pi:pi+6]):
        col=j%3; row=j//3; x=M+col*(cw+8); y=H-M-18-(row+1)*ch-row*8
        card(c,x,y,no,code,X,rws)
    c.setFillColor(GREY); c.setFont('DVC',7); c.drawString(M,M-10,"Year-End Cards · cut along the dotted lines · hour = hours from 18:00 UTC · S short / L long · ▲ correction year"); c.showPage()
c.save(); print(len(cards),'cards')
