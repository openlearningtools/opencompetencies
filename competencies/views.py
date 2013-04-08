from django.shortcuts import render_to_response
from django.template import RequestContext

from competencies.models import School, SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget


def index(request):
    return render_to_response('competencies/index.html')

def schools(request):
    schools = School.objects.all()
    return render_to_response('competencies/schools.html',{'schools': schools})

def school(request, school_id):
    school = School.objects.get(id=school_id)
    sa_sdas = get_subjectarea_subdisciplinearea_dict(school_id)
    return render_to_response('competencies/school.html',{'school': school, 'subject_area_subdiscipline_areas': sa_sdas})

def subject_area(request, school_id, subject_area_id):
    """Shows a subject area's subdiscipline areas, and competency areas."""
    sa_competencies = get_sa_competencies_dict(SubjectArea.objects.get(id=subject_area_id))
    school = School.objects.get(id=school_id)
    return render_to_response('competencies/subject_area.html',{'school': school, 'sa_competencies': sa_competencies})

def entire_system(request):
    subject_areas = SubjectArea.objects.all()
    return render_to_response('competencies/entire_system.html', {'subject_areas': subject_areas})


# --- Helper functions ---
def get_subjectarea_subdisciplinearea_dict(school_id):
    """Builds a dictionary with all subject_areas as keys, 
    with subdiscipline_areas as values."""
    school = School.objects.get(id=school_id)
    subject_areas = school.subjectarea_set.all()
    sa_sdas = {}
    for sa in subject_areas:
        sa_sdas[sa] = sa.subdisciplinearea_set.all()
    return sa_sdas

def get_sa_competencies_dict(subject_area):
    """Builds a dictionary of all competency areas for a given
    subject area, including its subdiscipline areas."""
    sa_competencies = {}
    # Competencies have fk to sa and sda; if sda, don't include in sa list
    competencies = []
    
    return sa_competencies
