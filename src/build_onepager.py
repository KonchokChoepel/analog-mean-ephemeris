"""One-page visual explainer (A4)."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from a3_draw import *
W,H=A4; M=34
IMG=sys.argv[2]
def img(c,path,x,y,w):
    ir=ImageReader(path); iw,ih=ir.getSize(); h=w*ih/iw
    c.drawImage(ir,x,y-h,w,h); c.setLineWidth(0.5); stroke(c,MIDGREY); c.rect(x,y-h,w,h); stroke(c,(0,0,0)); return h
c=canvas.Canvas(sys.argv[1],pagesize=A4); c.setTitle('The 36 Calendar Analog Ephemeris · one-page introduction'); c.setAuthor('Aidan John Walsh')
fill(c,GOLD); c.rect(M,H-M-74,W-2*M,74,stroke=0,fill=1); fill(c,(1,1,1))
c.setFont('DejaVuSans-Bold',20); c.drawString(M+14,H-M-32,'THE 36 CALENDAR ANALOG EPHEMERIS')
c.setFont('DejaVuSans',10.5); c.drawString(M+14,H-M-52,'Every planetary cycle on paper, in whole days. Look up the date, cross off the box.')
c.setFont('DejaVuSans',9); c.drawString(M+14,H-M-66,'Aidan John Walsh · free to download · prints available'); fill(c,(0,0,0))
y=H-M-90
y-=para(c,'<b>Thirty-six calendars</b>: the Sun, the Moon, Mercury, Venus, Mars, Jupiter, Saturn and the Nodes, and every pair of them, each counting its mean cycle in whole days, '
         'with an intercalary day and a self-correcting hour step that keep it true for a lifetime. Nothing needs electricity, software or arithmetic.',M,y,W-2*M,size=10.5,leading=14)+8
y-=para(c,'<b>A journal to date the world by the sky.</b> Write what happened, then the day of each cycle. Count, month by month and year by year, as the Babylonian astronomers did '
         'when they kept the sky and the price of barley in the same diary.',M,y,W-2*M,size=10.5,leading=14)+12
gw=(W-2*M-14)/2
h1=img(c,IMG+'/a3_front_sun.png',M,y,gw); img(c,IMG+'/a3_back_sun.png',M+gw+14,y,gw)
c.setFont('DejaVuSans',8); c.drawString(M,y-h1-11,'A3 calendar, front: one box a day'); c.drawString(M+gw+14,y-h1-11,'Its back: Date Finder and a hundred-year Lifetime Table')
y-=h1+26
h2=img(c,IMG+'/a3_front_mercury_sun.png',M,y,gw); img(c,IMG+'/journal.png',M+gw+14,y,gw)
c.setFont('DejaVuSans',8); c.drawString(M,y-h2-11,'Mercury–Sun: Mercury’s place in the sky, and the Moon’s days'); c.drawString(M+gw+14,y-h2-11,'The journal: hours, the day’s ruler, and the tally')
y-=h2+28
items=['<b>The A3 pack</b>: 36 calendars with their tables, the method, a history of the method, seven almanacs and the journal.',
       '<b>The A4 home set</b>: the 36 calendars in black and white, a two-page calibration guide and the journal.',
       '<b>Open</b>: CC BY-SA 4.0 for the pages, GPL-3.0 for the code that builds and checks every one of them.']
for t in items: y-=para(c,'· '+t,M,y,W-2*M,size=9.5,leading=12.5)+3
c.setFont('DejaVuSans-Bold',11); c.drawCentredString(W/2,M+16,'github.com/KonchokChoepel/analog-mean-ephemeris')
c.setFont('DejaVuSans',7); c.drawCentredString(W/2,M,'© 2026 Aidan John Walsh · pages CC BY-SA 4.0 · code GPL-3.0')
c.save()
