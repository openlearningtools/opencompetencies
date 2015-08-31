from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from competencies.models import SubjectArea

class PDFTest():
    def __init__(self, response):
        # response argument is used as the file object.
        self.response = response
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        self.styles = getSampleStyleSheet()

        self.title = ''
        self.subtitle = ''

    def myFirstPage(self, canvas, doc):
        canvas.saveState()

        canvas.setFont('Times-Bold',16)
        canvas.drawString(inch, self.PAGE_HEIGHT-inch, self.Title)
        canvas.setFont('Times-Bold',14)
        canvas.drawString(inch, self.PAGE_HEIGHT-1.25*inch, self.subtitle+'blah')

        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.restoreState()

    def makeSummary(self, org, sa, sdas, cas, eus):
        """Generates a pdf of the sa_summary page."""
        print('building doc...')

        # Prep document.
        self.Title = org.name
        self.subtitle = sa.subject_area

        doc = SimpleDocTemplate("competencies/sa_summary.pdf")
        doc = SimpleDocTemplate(self.response)
        Story = [Spacer(1,0.5*inch)]
        style = self.styles["Normal"]

        self.first_col_x = inch
        self.second_col_x = self.PAGE_WIDTH / 3

        from reportlab.platypus.tables import Table
        data = [(org.alias_ca.title(), org.alias_eu.title())]

        # Add subject area competency areas.
        for ca in cas:
            if not ca.subdiscipline_area:
                p = Paragraph(ca.competency_area, style)
                data.append((p, ''))
                for eu in eus:
                    if eu.competency_area == ca:
                        p = Paragraph(eu.essential_understanding, style)
                        data.append(('', p))

        # Add sda competency areas.
        for sda in sdas:
            data.append((sda.subdiscipline_area, ''))
            for ca in cas:
                if (ca.subdiscipline_area
                    and ca.subdiscipline_area.subdiscipline_area == sda.subdiscipline_area):
                    data.append((ca.competency_area, ''))

            
        table = Table(data)
        elements = []
        elements.append(table)
        doc.build(elements)

        return self.response
        # # Add competency areas and essential understandings.
        # for sda in sa.subdisciplinearea_set.all():
        #     p = Paragraph(sda.subdiscipline_area, style)
        #     Story.append(p)
        #     Story.append(Spacer(1, 0.2*inch))

        #doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
