"""Rebuild everything into ../output  (python3 src/build_all.py [ISO UTC time for the Year-End Cards])"""
import subprocess,sys,os
here=os.path.dirname(os.path.abspath(__file__)); out=os.path.join(here,'..','output'); os.makedirs(os.path.join(out,'almanacs'),exist_ok=True)
now=sys.argv[1:]
steps=[['run_all.py'],['build_pdf.py',out+'/36_Calendars_Hand_Pack.pdf'],['almanac.py',out+'/almanacs'],['sep_table.py',out+'/Separation_Table.pdf'],['now36.py']+now,['yearend.py',out+'/Year_End_Cards.pdf']]
for s in steps:
    print('>>',*s); subprocess.run([sys.executable]+s,cwd=here,check=True)
