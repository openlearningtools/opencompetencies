from django.shortcuts import render_to_response
from django.template import RequestContext

from copy import copy

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

def fork(request, school_id):
    empty_school = School.objects.get(id=school_id)
    # Only get schools that have at least one subject area:
    forkable_schools = [school for school in School.objects.all() if school.subjectarea_set.all()]
    return render_to_response('competencies/fork.html',{'empty_school': empty_school, 'forkable_schools': forkable_schools})

def confirm_fork(request, forking_school_id, forked_school_id):
    """Forks the requested school, and confirms success."""
    forking_school = School.objects.get(id=forking_school_id)
    forked_school = School.objects.get(id=forked_school_id)
    fork_school(forking_school, forked_school)
    return render_to_response('competencies/confirm_fork.html',{'forking_school': forking_school, 'forked_school': forked_school})

def subject_area(request, school_id, subject_area_id):
    """Shows a subject area's subdiscipline areas, and competency areas."""
    school = School.objects.get(id=school_id)
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    # Get a list of general subject competencies, and a dict of competencies by sda
    sa_competencies, sda_competencies = get_sa_competencies(subject_area)
    return render_to_response('competencies/subject_area.html',{'school': school, 'subject_area':subject_area, 'sa_competencies': sa_competencies, 'sda_competencies': sda_competencies})

def competency_area(request, school_id, subject_area_id, competency_area_id):
    """Shows all of the essential understandings and learning targets for a given comptency area."""
    school = School.objects.get(id=school_id)
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    competency_area = CompetencyArea.objects.get(id=competency_area_id)
    # Get a dict of essential understandings, and associated learning targets.
    eus_lts = get_eus_lts(competency_area)
    return render_to_response('competencies/competency_area.html',
                              {'school': school, 'subject_area': subject_area, 'competency_area': competency_area,
                               'eus_lts': eus_lts})

def entire_system(request):
    subject_areas = SubjectArea.objects.all()
    return render_to_response('competencies/entire_system.html', {'subject_areas': subject_areas})


# --- Helper functions ---
def get_subjectarea_subdisciplinearea_dict(school_id):
    """Builds a dictionary with all subject_areas as keys, 
    with subdiscipline_areas as values."""
    school = School.objects.get(id=school_id)
    subject_areas = school.subjectarea_set.all()
    sa_sdas = {sa: sa.subdisciplinearea_set.all() for sa in subject_areas}
    return sa_sdas

def get_sa_competencies(subject_area):
    """Returns a tuple:
    first item: list of comps in general subject area
    second item: dictionary of comps by sda"""

    # Loop through competencies, placing by sda first;
    #  If no sda, place in general subject area.
    sa_competencies = []
    sda_competencies = {sda: [] for sda in subject_area.subdisciplinearea_set.all()}
    for competency in subject_area.competencyarea_set.all():
        if competency.subdiscipline_area:
            sda_competencies[competency.subdiscipline_area].append(competency)
        else:
            sa_competencies.append(competency)

    return (sa_competencies, sda_competencies)

def get_eus_lts(competency_area):
    """Returns a dict of essential understandings, with associated learning targets."""
    eus = competency_area.essentialunderstanding_set.all()
    eus_lts = {}
    for eu in eus:
        eus_lts[eu] = eu.learningtarget_set.all()
    return eus_lts

def fork_school(forking_school, forked_school):
    """Forks a given school's competency system.  Copies all aspects of
    forked_school's competency system over to forking_school's system.
    Resets all keys to new school's system, so that forking_school gets
    an independent, isolated copy of the forked_school's system.

    Test: Create a school, fork it, compare all hierarchical elements.
    """

    # Overall approach:
    #  Create new copy of each element;
    #  Set pk, id to None;
    #  Redefine appropriate parameters;
    #  Save new element;
    #  Use existing elements to access next level of hierarchy.

    # Copy all subject areas to new school:
    sas = forked_school.subjectarea_set.all()
    for sa in sas:
        new_sa = copy(sa)
        new_sa.pk, new_sa.id = None, None
        new_sa.school = forking_school
        new_sa.save()

        # Copy all competency areas that are only connected to an sa,
        #  not sda, here:
        comps = sa.competencyarea_set.all()
        for comp in comps:
            if not comp.subdiscipline_area:
                new_comp = copy(comp)
                new_comp.pk, new_comp.id = None, None
                new_comp.subject_area = new_sa
                new_comp.save()

        # Copy all sdas to new school:
        sdas = sa.subdisciplinearea_set.all()
        for sda in sdas:
            new_sda = copy(sda)
            new_sda.pk, new_sda.id = None, None
            new_sda.subject_area = new_sa
            new_sda.save()
            
            # Copy all competency areas connected to current sda here:
            for comp in comps:
                if comp.subdiscipline_area and comp.subdiscipline_area.subdiscipline_area == sda.subdiscipline_area:
                    new_comp = copy(comp)
                    new_comp.pk, new_comp.id = None, None
                    new_comp.subject_area = new_sa
                    new_comp.subdiscipline_area = new_sda
                    new_comp.save()
                    
