"""A4 journal: one landscape sheet per weekday (left: the 24 hours; right: the day's tally and notes)."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping
import engine2 as E
FD='/usr/share/fonts/truetype/dejavu/'
for n in ['DejaVuSans','DejaVuSans-Bold','DejaVuSansCondensed','DejaVuSansCondensed-Bold']:
    pdfmetrics.registerFont(TTFont(n,FD+n+'.ttf'))
addMapping('DejaVuSans',0,0,'DejaVuSans'); addMapping('DejaVuSans',1,0,'DejaVuSans-Bold')
W,H=landscape(A4); M=22; GUT=26; PW=(W-2*M-GUT)/2
LIC='© 2026 Aidan John Walsh · CC BY-SA 4.0: use, share and modify freely, commercially too, with credit; share changes under the same licence · github.com/KonchokChoepel/analog-mean-ephemeris'
CHALD=['A','B','C','D','E','F','G']          # the hour sequence: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon
DAYS=[('SUNDAY','D'),('MONDAY','G'),('TUESDAY','C'),('WEDNESDAY','F'),('THURSDAY','B'),('FRIDAY','E'),('SATURDAY','A')]
KEY={'G':('nurses, midwives, caterers, sailors, drivers, childcare','silver, milk, eggs, seafood, salt, bottled water','home, family, mothers, mood and sleep, public opinion'),
 'F':('writers, journalists, teachers, programmers, couriers','phones, computers, paper, books, software','email, contracts, exams, deals, short trips, paperwork'),
 'E':('musicians, designers, beauticians, florists, chefs','cosmetics, perfume, clothing, flowers, sweets, wine','dating, marriage, parties, gifts, friendships'),
 'D':('executives, politicians, officials, jewellers, actors','gold, jewellery, citrus, saffron, honey','leadership, status, fame, fathers, the heart'),
 'C':('soldiers, police, surgeons, mechanics, builders, athletes','steel, tools, fuel, firearms, spicy food','fights, fevers, injuries, accidents, workouts, surgery'),
 'B':('judges, lawyers, clergy, bankers, professors, publishers','grain, sugar, fruit, tin, shares','courts, studies, travel abroad, windfalls, investments'),
 'A':('farmers, miners, surveyors, civil engineers, undertakers','lead, coal, concrete, timber, land','property, debts, deadlines, old age, bones and teeth')}
TIMES=['6 PM','7 PM','8 PM','9 PM','10 PM','11 PM','12 AM','1 AM','2 AM','3 AM','4 AM','5 AM','6 AM','7 AM','8 AM','9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM','5 PM']
KS=ParagraphStyle('k',fontName='DejaVuSans',fontSize=7,leading=8.6)

def hour_ruler(day,k):
    """k = 1..24 counted from 18:00; hours 13-24 are the day's own (13 = 6 AM = the day ruler);
    hours 1-12 are the night of the previous planetary day."""
    i=CHALD.index(day)
    return CHALD[(i+(k-13))%7]

def page(c,name,day,shade_day=False):
    # ---------- left: the hours
    x0=M; top=H-M
    c.setFont('DejaVuSans-Bold',7); c.drawString(x0,top-11,'SUBJECT'); c.setLineWidth(0.6); c.rect(x0+36,top-17,150,16)
    c.drawString(x0+198,top-11,'TODAY')
    cw=(PW-228)/3
    for j,(b,lab) in enumerate([('B','year'),('D','month'),('G','day')]):
        bx=x0+228+j*cw; c.rect(bx,top-17,cw,16)
        c.setFont('DejaVuSans',8); c.drawString(bx+3,top-12,E.GLYPH[b])
        c.setFont('DejaVuSans',5); c.drawRightString(bx+cw-2,top-15,lab)
    by=top-40; c.setFillGray(0.15); c.rect(x0,by,PW,18,stroke=0,fill=1); c.setFillGray(1)
    c.setFont('DejaVuSans-Bold',13); c.drawString(x0+8,by+4.5,name)
    c.setFont('DejaVuSans',6.5); c.drawString(x0+8+pdfmetrics.stringWidth(name,'DejaVuSans-Bold',13)+12,by+6,f'day of {E.NAMES[day]} · the day begins at 18:00 (6 PM)')
    c.setFont('DejaVuSans',10); c.drawRightString(x0+PW-8,by+4.5,E.GLYPH[day]); c.setFillGray(0)
    rh=(by-4-(M+22))/24; y=by-4
    for k in range(1,25):
        yy=y-k*rh
        if k in (1,13): c.setLineWidth(1.0)
        else: c.setLineWidth(0.4)
        c.line(x0,yy+rh,x0+PW,yy+rh)
        if k<=12 or shade_day:
            c.setFillGray(0.9); c.rect(x0,yy,40,rh,stroke=0,fill=1); c.rect(x0+40,yy,18,rh,stroke=0,fill=1); c.setFillGray(0)
        c.setFont('DejaVuSans',8.5); c.drawCentredString(x0+9,yy+rh/2-3,E.GLYPH[hour_ruler(day,k)])
        c.setFont('DejaVuSans',6); c.drawString(x0+17,yy+rh/2-2,TIMES[k-1])
        c.setFont('DejaVuSans-Bold',6.5); c.drawCentredString(x0+49,yy+rh/2-2.2,str(k))
        c.setDash(0.6,1.4); c.setLineWidth(0.35); c.line(x0+62,yy+rh/2,x0+PW-4,yy+rh/2); c.setDash()
    c.setLineWidth(1.0); c.line(x0,y-24*rh,x0+PW,y-24*rh); c.rect(x0,y-24*rh,PW,24*rh)
    for xx in (x0+40,x0+58): c.setLineWidth(0.4); c.line(xx,y,xx,y-24*rh)
    c.setFont('DejaVuSans',5.6)
    c.drawString(x0,M+12,'Hours are numbered 1 to 24 from 18:00 (6 PM). Planetary hour: the ruler of each hour.')
    # ---------- right: tally, key, notes
    x1=M+PW+GUT
    c.setFillGray(0.15); c.rect(x1,top-22,PW,20,stroke=0,fill=1); c.setFillGray(1)
    c.setFont('DejaVuSans-Bold',12); c.drawString(x1+8,top-16.5,f'{name} · notes')
    c.setFont('DejaVuSans',6.3); c.drawRightString(x1+PW-8,top-15.5,"MONTH AND DAY IN EACH BODY'S CALENDAR TODAY"); c.setFillGray(0)
    lw=46; colw=(PW-lw)/8; ty=top-28
    c.setLineWidth(0.6)
    for j,b in enumerate(E.ORDER):
        bx=x1+lw+j*colw; c.rect(bx,ty-24,colw,24)
        c.setFont('DejaVuSans',10); c.drawCentredString(bx+colw/2,ty-13,E.GLYPH[b])
        c.setFont('DejaVuSans-Bold',4.8); c.drawCentredString(bx+colw/2,ty-21,E.NAMES[b].upper())
    c.rect(x1,ty-24,lw,24)
    for r,lab in enumerate(['MONTH','DAY','IN THE SKY']):
        yy=ty-24-(r+1)*18; c.rect(x1,yy,lw,18); c.setFont('DejaVuSans-Bold',6 if r<2 else 5.2); c.drawString(x1+4,yy+6.5,lab)
        for j in range(8): c.rect(x1+lw+j*colw,yy,colw,18)
    yk=ty-24-54-9
    sky=('<b>In the sky</b> (sign and degree): ☉ the Sun sheet’s month, day − 1 ≈ degree · ☽ the Sun + 12° a day since the 1st of Moon–Sun · '
         '☿ ♀ ♂ ♃ ♄ the Sun ± the distance on each Sun–planet sheet (E evening sky, W morning, under 12 not visible) · ☊ the Nodes sheet’s month.')
    p=Paragraph(sky,ParagraphStyle('sk',fontName='DejaVuSans',fontSize=5.8,leading=7)); _,ph=p.wrap(PW,40); p.drawOn(c,x1,yk-ph+6)
    ky=yk-ph-2
    t,g,mtr=KEY[day]
    c.setFont('DejaVuSans-Bold',6.5); c.drawString(x1,ky-7,f'{E.GLYPH[day]}  {E.NAMES[day].upper()} · what the day ruler governs, to note')
    c.setLineWidth(0.8); c.line(x1,ky-10,x1+PW,ky-10)
    cy=ky-12; tw=(PW-6)/3; hh=0
    for j,(lab,txt) in enumerate([('Trades',t),('Goods',g),('Matters',mtr)]):
        p=Paragraph(f'<font name="DejaVuSans-Bold">{lab}</font>  {txt}',KS); _,h=p.wrap(tw,60); p.drawOn(c,x1+j*(tw+3),cy-h); hh=max(hh,h)
    ny=cy-hh-12
    c.setFont('DejaVuSans-Bold',6.5); c.drawString(x1,ny,'NOTES'); c.setLineWidth(0.8); c.line(x1,ny-3,x1+PW,ny-3)
    foot=M+42; nlines=int((ny-8-foot)/17.6); step=(ny-8-foot)/nlines
    for i in range(1,nlines+1):
        yy=ny-3-i*step; c.setDash(0.6,1.4); c.setLineWidth(0.35); c.line(x1,yy,x1+PW-12,yy); c.setDash()
        c.setFont('DejaVuSans',5); c.setFillGray(0.45); c.drawRightString(x1+PW,yy+1,str(i)); c.setFillGray(0)
    p=Paragraph('Planetary hours: hour 13 (6 AM) belongs to the day’s planet; the hours after it follow the order Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, and repeat. '
                'Use them to mark a chosen time. Hours 1–12, the night at the head of the left page, belong to the previous planetary day. '
                '<b>Journal first, sheets second:</b> write what happened before you look at the sheets, then fill in each body’s month and day. Count the entries under each body at the turn of each month and year.',
                ParagraphStyle('f',fontName='DejaVuSans',fontSize=5.6,leading=7))
    _,h=p.wrap(PW,40); p.drawOn(c,x1,M+12)
    c.setFont('DejaVuSans',5); c.drawString(M,M,LIC)

# ---------------- empirical (blind) edition: one page for every day, no rulers, no meanings
RECORD=[('Events','something that happened, with the hour it happened (1–24). One line, plain words: who or what, and what changed.'),
        ('Counts','how many of something: the same thing counted the same way every day, so days can be compared.'),
        ('Measures','a reading with a unit, taken the same way each time: an amount, a duration, a weight, a price, a temperature.'),
        ('Ratings','a state scored on a scale you fix once and never change (for example 1 to 5), at the same hour each day.'),
        ('Absences','something regular that did not happen. A day with nothing to report is still a day: write “nothing”.')]
RULES=('Write the plain fact, not what it means. Use the same words for the same kind of thing. Record before you look at any calendar. '
       'Never change an old entry: add a dated correction. Keep every day, ordinary ones included: patterns can only be counted against them.')
def page_emp(c):
    x0=M; top=H-M
    c.setFont('DejaVuSans-Bold',7); c.drawString(x0,top-11,'SUBJECT'); c.setLineWidth(0.6); c.rect(x0+36,top-17,150,16)
    c.drawString(x0+198,top-11,'DATE'); c.rect(x0+222,top-17,PW-222,16)
    by=top-40; c.setFillGray(0.15); c.rect(x0,by,PW,18,stroke=0,fill=1); c.setFillGray(1)
    c.setFont('DejaVuSans-Bold',13); c.drawString(x0+8,by+4.5,'DAY'); c.setFont('DejaVuSans',6.5)
    c.drawString(x0+46,by+6,'weekday ______________'); c.setFillGray(0)
    rh=(by-4-(M+10))/24; y=by-4
    for k in range(1,25):
        yy=y-k*rh
        c.setLineWidth(1.0 if k in (1,13) else 0.4); c.line(x0,yy+rh,x0+PW,yy+rh)
        c.setFont('DejaVuSans',6); c.drawString(x0+17,yy+rh/2-2,TIMES[k-1])
        c.setFont('DejaVuSans-Bold',6.5); c.drawCentredString(x0+49,yy+rh/2-2.2,str(k))
        c.setDash(0.6,1.4); c.setLineWidth(0.35); c.line(x0+62,yy+rh/2,x0+PW-4,yy+rh/2); c.setDash()
    c.setLineWidth(1.0); c.rect(x0,y-24*rh,PW,24*rh)
    for xx in (x0+15,x0+40,x0+58): c.setLineWidth(0.4); c.line(xx,y,xx,y-24*rh)
    c.setFont('DejaVuSans',5.6)
    x1=M+PW+GUT
    c.setFillGray(0.15); c.rect(x1,top-22,PW,20,stroke=0,fill=1); c.setFillGray(1)
    c.setFont('DejaVuSans-Bold',12); c.drawString(x1+8,top-16.5,'CYCLES'); c.setFillGray(0)
    kw='events · counts · measures · durations · ratings · absences'
    fs=6.6
    while pdfmetrics.stringWidth(kw,'DejaVuSans',fs)>PW and fs>5: fs-=0.1
    # the triangle: own cycles on the diagonal, the 28 pairs below it (code = column letter + row letter)
    O=E.ORDER; lw=11; cw=(PW-lw)/8; ch=17.5; tt=top-30
    slow={s['code'] for s in E.all_sheets() if s['slow']}
    for i,ri in enumerate(O):
        yy=tt-(i+1)*ch
        c.setFont('DejaVuSans-Bold',7); c.drawCentredString(x1+lw/2-1,yy+ch/2-2.5,ri)
        for j in range(i+1):
            bx=x1+lw+j*cw; code=O[j]+ri
            if i==j: c.setFillGray(0.9); c.rect(bx,yy,cw,ch,stroke=0,fill=1); c.setFillGray(0)
            c.setLineWidth(0.6); c.rect(bx,yy,cw,ch)
            c.setLineWidth(0.3); c.setDash(0.8,1.2); c.line(bx+cw*0.42,yy+1.5,bx+cw*0.42,yy+ch-1.5); c.setDash()
            c.setFont('DejaVuSansCondensed-Bold',5.2); c.drawRightString(bx+cw-1.4,yy+ch-5.6,code)
    tb=tt-8*ch
    # notes, below the triangle
    ny=tb-14
    c.setFillGray(0.15); c.rect(x1,ny-18,PW,18,stroke=0,fill=1); c.setFillGray(1)
    c.setFont('DejaVuSans-Bold',12); c.drawString(x1+8,ny-13.5,'NOTES')
    c.setFont('DejaVuSans',fs); c.drawRightString(x1+PW-8,ny-12.5,kw); c.setFillGray(0)
    step=17.6; foot=M+10; y=ny-18-step; n=0
    while y>foot:
        n+=1; c.setDash(0.6,1.4); c.setLineWidth(0.35); c.line(x1,y,x1+PW-12,y); c.setDash()
        c.setFont('DejaVuSans',5); c.setFillGray(0.45); c.drawRightString(x1+PW,y+1,str(n)); c.setFillGray(0)
        y-=step
    c.setFont('DejaVuSans',5); c.drawString(M,M,LIC)

def build(out):
    c=canvas.Canvas(out,pagesize=landscape(A4)); c.setTitle('The 36 Calendar Analog Ephemeris · '+('Empirical Edition · A4 journal page' if E.EMP else 'A4 journal pages (black and white)')); c.setAuthor('Aidan John Walsh')
    if E.EMP: page_emp(c); c.showPage()
    else:
        for name,day in DAYS: page(c,name,day); c.showPage()
    c.save()
if __name__=='__main__': build(sys.argv[1])
