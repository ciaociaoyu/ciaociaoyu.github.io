#!/usr/bin/env python3
"""Build the academic CV from cv-data.json with ReportLab (4.x)."""
from pathlib import Path
from html import escape
import argparse,json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Table,TableStyle

ROOT=Path(__file__).resolve().parent
# Embed real font files so the downloaded CV renders consistently across viewers.
mac_fonts=Path('/System/Library/Fonts/Supplemental')
if (mac_fonts/'Times New Roman.ttf').is_file():
    font_paths=[mac_fonts/x for x in ['Times New Roman.ttf','Times New Roman Bold.ttf','Times New Roman Italic.ttf','Times New Roman Bold Italic.ttf']]
else:
    font_dir=Path(reportlab.__file__).resolve().parent/'fonts'
    font_paths=[font_dir/x for x in ['Vera.ttf','VeraBd.ttf','VeraIt.ttf','VeraBI.ttf']]
for name,path in zip(['CVSerif','CVSerif-Bold','CVSerif-Italic','CVSerif-BoldItalic'],font_paths):
    pdfmetrics.registerFont(TTFont(name,str(path)))
pdfmetrics.registerFontFamily('CVSerif',normal='CVSerif',bold='CVSerif-Bold',italic='CVSerif-Italic',boldItalic='CVSerif-BoldItalic')
INK=colors.HexColor('#161b2b')
MUTED=colors.HexColor('#50596c')
BLUE=colors.HexColor('#304d77')
styles={
 'name':ParagraphStyle('Name',fontName='CVSerif-Bold',fontSize=24,leading=28,textColor=INK,alignment=TA_CENTER,spaceAfter=4),
 'role':ParagraphStyle('Role',fontName='CVSerif',fontSize=10.7,leading=14,alignment=TA_CENTER,spaceAfter=3),
 'contact':ParagraphStyle('Contact',fontName='CVSerif',fontSize=9.4,leading=12.5,alignment=TA_CENTER),
 'section':ParagraphStyle('Section',fontName='CVSerif-Bold',fontSize=11.5,leading=15,textColor=INK,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'entry':ParagraphStyle('Entry',fontName='CVSerif-Bold',fontSize=10.5,leading=13.5,spaceAfter=2,keepWithNext=True),
 'body':ParagraphStyle('Body',fontName='CVSerif',fontSize=10.4,leading=13.7,textColor=INK),
 'small':ParagraphStyle('Small',fontName='CVSerif',fontSize=9.5,leading=12.5,textColor=MUTED),
 'date':ParagraphStyle('Date',fontName='CVSerif',fontSize=9.8,leading=13.5,alignment=2,textColor=MUTED),
 'citation':ParagraphStyle('Citation',fontName='CVSerif',fontSize=10.3,leading=14,textColor=INK,leftIndent=21,firstLineIndent=-21,spaceAfter=10),
 'bullet':ParagraphStyle('Bullet',fontName='CVSerif',fontSize=10.2,leading=13.6,textColor=INK,leftIndent=11,firstLineIndent=-9,spaceBefore=2),
}
def p(text,kind='body'):return Paragraph(text,styles[kind])
def a(url,label):return '<a href="'+escape(url,quote=True)+'" color="#304d77">'+escape(label)+'</a>'
def authors_text(entry):
 names=entry.get('display_authors',entry.get('authors',[]));stars=entry.get('equal_contribution',[])
 out=[]
 for name in names:
  s=escape(name)
  if name in stars:s+='<super>*</super>'
  if name=='Jichao Yu':s='<b>'+s+'</b>'
  out.append(s)
 return ', '.join(out)
def citation(entry,index):
 parts=[f'[{index}] ']
 if entry.get('authors'):parts.append(authors_text(entry)+'. ')
 parts.append('<b>'+escape(entry['title'])+'</b>. ')
 parts.append(escape(entry['venue'])+'. ')
 if entry.get('role'):parts.append(escape(entry['role']).replace('Jichao Yu','<b>Jichao Yu</b>')+'. ')
 if entry.get('url'):parts.append(a(entry['url'],entry['link_label'])+'.')
 if entry.get('equal_contribution'):parts.append('<br/><font size="9.5"><i>* Equal contribution (co-first authors).</i></font>')
 return p(''.join(parts),'citation')
def header_row(left,right):
 t=Table([[p(left,'entry'),p(right,'date')]],colWidths=[383,121],hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
 return t
def footer(canvas,doc):
 canvas.saveState();canvas.setFont('CVSerif',9);canvas.setFillColor(MUTED)
 canvas.drawString(54,27,'Jichao (Ciao) Yu | Updated October 24, 2026')
 canvas.drawRightString(558,27,str(doc.page));canvas.restoreState()
def build(data,output):
 doc=SimpleDocTemplate(str(output),pagesize=letter,rightMargin=54,leftMargin=54,topMargin=42,bottomMargin=45,title='Jichao (Ciao) Yu - Curriculum Vitae',author='Jichao Yu',subject='Academic CV updated October 24, 2026')
 story=[p('Jichao (Ciao) Yu','name'),p('Ph.D. Student in Computer Science | University of Georgia','role'),p(a('mailto:jy03364@uga.edu','jy03364@uga.edu')+' | '+a('mailto:ciao_yu@outlook.com','ciao_yu@outlook.com')+' | 614-264-2313','contact'),p(a('https://ciaociaoyu.github.io/','ciaociaoyu.github.io')+' | '+a('https://github.com/ciaociaoyu','github.com/ciaociaoyu'),'contact')]
 story.append(p('EDUCATION','section'))
 for item in data['education']:
  group=[header_row(escape(item['institution']),escape(item['date'])),p(escape(item['degree']))]
  for line in item['details']:group.append(p(escape(line),'small'))
  group.append(Spacer(1,8));story.append(KeepTogether(group))
 story.extend([p('RESEARCH INTERESTS','section'),p('Machine learning systems, federated and distributed learning, optimization, and AI for education.'),p('RECENT PUBLICATIONS AND PREPRINTS','section')])
 for i,item in enumerate(data['publications'][:4],1):story.append(KeepTogether([citation(item,i)]))
 story.extend([PageBreak(),p('EARLIER PUBLICATIONS','section')])
 for i,item in enumerate(data['publications'][4:],5):story.append(KeepTogether([citation(item,i)]))
 story.append(p('RESEARCH EXPERIENCE','section'))
 for item in data['research']:
  group=[header_row(escape(item['title']),escape(item['date'])),p(escape(item['institution']),'small'),p(escape(item['advisors']),'small')]
  group.extend(p('- '+escape(line),'bullet') for line in item['bullets'])
  group.append(Spacer(1,9));story.append(KeepTogether(group))
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT.parent/'CV.pdf');ap.add_argument('--data',type=Path,default=ROOT/'cv-data.json');args=ap.parse_args()
 args.output.parent.mkdir(parents=True,exist_ok=True);build(json.loads(args.data.read_text()),args.output);print(args.output)
