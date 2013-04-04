from django.shortcuts import render_to_response
from django.template import RequestContext

from competencies.models import SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget


def index(request):
    return render_to_response('competencies/index.html')

def entire_system(request):
    subject_areas = SubjectArea.objects.all()
    return render_to_response('competencies/entire_system.html', {'subject_areas': subject_areas})
