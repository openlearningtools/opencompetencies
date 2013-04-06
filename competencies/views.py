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
    subject_areas = school.subjectarea_set.all()
    subject_area_subdiscipline_areas = get_subjectarea_subdisciplinearea_dict(school_id)
    return render_to_response('competencies/school.html',{'school': school, 'subject_areas': subject_areas, 'subject_area_subdiscipline_areas': subject_area_subdiscipline_areas})

def subject_area(request, subject_area_id):
    """Shows a subject area's subdiscipline areas, and competency areas."""
    # Build subject_area-
    pass

def entire_system(request):
    subject_areas = SubjectArea.objects.all()
    return render_to_response('competencies/entire_system.html', {'subject_areas': subject_areas})

# --- Helper functions ---
def get_subjectarea_subdisciplinearea_dict(school_id):
    """Builds a dictionary of all subject_areas as keys, 
    with subdiscipline_areas as values."""
    school = School.objects.get(id=school_id)
    subject_areas = school.subjectarea_set.all()
    # Build a dictionary for use in template:
    subject_area_subdiscipline_areas = {}
    for subject_area in subject_areas:
        subject_area_subdiscipline_areas[subject_area] = subject_area.subdisciplinearea_set.all()
    return subject_area_subdiscipline_areas
