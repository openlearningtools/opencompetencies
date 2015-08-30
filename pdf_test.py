from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'opencompetencies.settings'

from competencies.models import SubjectArea


class PDFTest():
    def __init__(self):
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.Title = ''
        self.subtitle = ''
        self.pageinfo = "platypus example"

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(inch, self.PAGE_HEIGHT-108, self.Title)
        canvas.drawString(inch, self.PAGE_HEIGHT-216, self.subtitle)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch,"First Page / %s" % self.pageinfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def go(self, sa_id):
        sa = SubjectArea.objects.get(id=sa_id)
        org = sa.organization
        self.Title = org.name
        self.subtitle = sa.subject_area

        doc = SimpleDocTemplate("phello.pdf")
        Story = [Spacer(1,2*inch)]
        style = self.styles["Normal"]



        for i in range(100):
            bogustext = ("Paragraph number %s. " % i) *20
            p = Paragraph(bogustext, style)
            Story.append(p)
            Story.append(Spacer(1,0.2*inch))
        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)


pdftest = PDFTest()
pdftest.go(24)
