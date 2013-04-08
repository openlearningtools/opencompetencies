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
    school = School.objects.get(id=school_id)
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    # Get a list of general subject competencies, and a dict of competencies by sda
    sa_competencies, sda_competencies = get_sa_competencies(subject_area)
    return render_to_response('competencies/subject_area.html',{'school': school, 'subject_area':subject_area, 'sa_competencies': sa_competencies, 'sda_competencies': sda_competencies})

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

def get_sa_competencies(subject_area):
    """Builds a dictionary of all competency areas for a given
    subject area, including its subdiscipline areas."""

    """Returns a tuple:
    first item: list of comps in general subject area
    second item: dictionary of comps by sda"""

    # Initialize dictionary value lists
    sa_competencies = []
    sda_competencies = {}
    sdas = subject_area.subdisciplinearea_set.all()
    for sda in sdas:
        sda_competencies[sda] = []

    # Loop through competencies, placing by sda first;
    #  If no sda, place in general subject area.
    competencies = subject_area.competencyarea_set.all()
    for competency in competencies:
        if competency.subdiscipline_area:
            sda_competencies[competency.subdiscipline_area].append(competency)
        else:
            sa_competencies.append(competency)

    return (sa_competencies, sda_competencies)
