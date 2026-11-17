import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from a3_draw import GOLD, fill, LIC
W,H=A4; M=46
TITLE='What the proof against Astrology might look like'
SUB='and its usefulness regardless'
paras=[
"Astrology makes a claim about time: that the stage of a cycle bears on the character of what happens within it. That is a claim about the world, and claims about the world can be counted. "
"What has always been missing is the frame: a fixed measure of every cycle, kept by hand, and a record of life written by someone who does not know which stage they are writing in.",
"The 36 Calendar Analog Ephemeris is that frame. Eight cycles, singly and in every pair, are counted in whole days, each from a fixed start, each corrected by a printed rule that holds for thousands of years. "
"Nothing on the sheets is estimated, and nothing is looked up after printing: every day of every cycle follows from one ledger, and anyone can rebuild it with a pencil.",
"The Empirical Edition makes the frame blind. The calendars are identical, day for day, to the standard edition, but the cycles carry codes, not names. The key is sealed before the first entry and held by someone else. "
"The keeper writes the day first, in plain facts — events, counts, measures — and copies the 36 cycle dates last. Before any of it begins, a plan is written and signed: what will be counted, against which stages, and what result would count.",
"The proof against Astrology would look like this. Year after year, by keeper after keeper, the entries fall across the months of every cycle exactly as the days recorded would predict. "
"The reference days are like any other day. The patterns that surface in the first half of a record fail to return in the second. The keys are opened, and they open onto nothing. "
"No argument, no ridicule: a stack of honest ledgers, each one null. That is what a disproof is.",
"The proof for Astrology would look the same, with a different tally. The instrument does not care which way it falls. That indifference is its authority.",
"Its usefulness does not wait on the verdict. The calendars teach the arithmetic of the sky as the ancients practised it: whole days against cycles that are not whole, intercalation, corrections in tiers — Meton’s problem, Khayyam’s, Gregory’s, solved on every sheet. "
"The journal trains attention: what happened, when, how much, how often. A household that keeps it for a decade owns a dataset of its own life, dated to every cycle there is, and a habit of seeing plainly. "
"The method is open, the pages are free, and the result, whichever way it falls, belongs to whoever does the counting.",
"The question has been argued for at least two thousand years. Here it can be reconciled with a page and pencil, a few minutes a day for regular record keeping, and some patience."]
def draw(c,fs):
    fill(c,GOLD); c.rect(M,H-M-78,W-2*M,78,stroke=0,fill=1); fill(c,(1,1,1))
    ts=19
    from reportlab.pdfbase.pdfmetrics import stringWidth as _sw
    while _sw(TITLE,'DejaVuSans-Bold',ts)>W-2*M-28: ts-=0.2
    c.setFont('DejaVuSans-Bold',ts); c.drawString(M+14,H-M-34,TITLE)
    c.setFont('DejaVuSans',12.5); c.drawString(M+14,H-M-56,SUB)
    c.setFont('DejaVuSans',8.5); c.drawRightString(W-M-14,H-M-70,'Aidan John Walsh · The 36 Calendar Analog Ephemeris'); fill(c,(0,0,0))
    st=ParagraphStyle('p',fontName='DejaVuSans',fontSize=fs,leading=fs*1.5,spaceAfter=fs*0.8,alignment=4)
    last=ParagraphStyle('l',parent=st,fontName='DejaVuSans-Bold')
    story=[Paragraph(t,st) for t in paras[:-1]]+[Paragraph(paras[-1],last)]
    f=Frame(M,M+14,W-2*M,H-2*M-100,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    f.addFromList(story,c); return not story
def build(out):
    lo,hi=8,14
    for _ in range(14):
        m=(lo+hi)/2; c=canvas.Canvas('/dev/null',pagesize=A4)
        if draw(c,m): lo=m
        else: hi=m
    c=canvas.Canvas(out,pagesize=A4); c.setTitle(TITLE+', '+SUB); c.setAuthor('Aidan John Walsh')
    draw(c,lo); c.setFont('DejaVuSans',5); c.drawCentredString(W/2,M-6,LIC); c.save(); print(round(lo,2))
build(sys.argv[1])
