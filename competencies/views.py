from django.shortcuts import render_to_response
from django.template import RequestContext

from competencies.models import School, SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget


def index(request):
    return render_to_response('competencies/index.html')

def schools(request):
    schools = School.objects.all()
    return render_to_response('competencies/schools.html',{'schools': schools})

def school(request, school_id):
    # Build out school-subject-subdiscipline dict or series of lists
    school = School.objects.get(id=school_id)
    subject_areas = school.subjectarea_set.all()
    return render_to_response('competencies/school.html',{'school': school, 'subject_areas': subject_areas})

def entire_system(request):
    subject_areas = SubjectArea.objects.all()
    return render_to_response('competencies/entire_system.html', {'subject_areas': subject_areas})
