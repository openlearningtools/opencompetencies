from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import modelformset_factory, inlineformset_factory

from copy import copy

from competencies.models import School, SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget


def index(request):
    return render_to_response('competencies/index.html')

# --- Simple views, for exploring system without changing it: ---
def schools(request):
    schools = School.objects.all()
    return render_to_response('competencies/schools.html', {'schools': schools}, context_instance=RequestContext(request))

def school(request, school_id):
    school = School.objects.get(id=school_id)
    return render_to_response('competencies/school.html', {'school': school})

def subject_area(request, subject_area_id):
    """Shows a subject area's subdiscipline areas, and competency areas."""
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    school = subject_area.school
    return render_to_response('competencies/subject_area.html',
                              {'subject_area': subject_area, 'school': school})

def subdiscipline_area(request, subdiscipline_area_id):
    """Shows all of the competency areas for a given subdiscipline area."""
    subdiscipline_area = SubdisciplineArea.objects.get(id=subdiscipline_area_id)
    subject_area = subdiscipline_area.subject_area
    school = subject_area.school
    competency_areas = subdiscipline_area.competencyarea_set.all()
    return render_to_response('competencies/subdiscipline_area.html',
                              {'subdiscipline_area': subdiscipline_area, 'subject_area': subject_area,
                               'school': school, 'competency_areas': competency_areas})

def competency_area(request, competency_area_id):
    """Shows all of the essential understandings for a given competency area."""
    competency_area = CompetencyArea.objects.get(id=competency_area_id)
    subject_area = competency_area.subject_area
    school = subject_area.school
    essential_understandings = competency_area.essentialunderstanding_set.all()
    return render_to_response('competencies/competency_area.html',
                              {'school': school, 'subject_area': subject_area, 'competency_area': competency_area,
                               'essential_understandings': essential_understandings})

def essential_understanding(request, essential_understanding_id):
    """Shows all learning targets for a given essential understanding."""
    essential_understanding = EssentialUnderstanding.objects.get(id=essential_understanding_id)
    competency_area = essential_understanding.competency_area
    subject_area = competency_area.subject_area
    school = subject_area.school
    learning_targets = essential_understanding.learningtarget_set.all()
    return render_to_response('competencies/essential_understanding.html',
                              {'school': school, 'subject_area': subject_area, 'competency_area': competency_area,
                               'essential_understanding': essential_understanding, 'learning_targets': learning_targets})


# --- Edit views, for editing parts of the system ---
def edit_school(request, school_id):
    """Allows user to edit a school's subject areas.
    """
    school = School.objects.get(id=school_id)
    # fields arg not working, but exclude works???
    SubjectAreaFormSet = modelformset_factory(SubjectArea, exclude=('school'))

    if request.method == 'POST':
        sa_formset = SubjectAreaFormSet(request.POST)
        if sa_formset.is_valid():
            instances = sa_formset.save(commit=False)
            for instance in instances:
                instance.school = school
                instance.save()
    # Create formset for unbound and bound forms
    #  This allows continuing to add more items after saving.
    sa_formset = SubjectAreaFormSet(queryset=SubjectArea.objects.all().filter(school_id=school_id))

    return render_to_response('competencies/edit_school.html', {'school': school, 'sa_formset': sa_formset},
                              context_instance = RequestContext(request))

def edit_subject_area(request, subject_area_id):
    """Allows user to edit a subject_area's subdiscipline areas.
    """
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    school = subject_area.school
    # fields arg not working, but exclude works???
    SubdisciplineAreaFormSet = modelformset_factory(SubdisciplineArea, exclude=('subject_area'))

    if request.method == 'POST':
        sda_formset = SubdisciplineAreaFormSet(request.POST)
        if sda_formset.is_valid():
            instances = sda_formset.save(commit=False)
            for instance in instances:
                instance.subject_area = subject_area
                instance.save()
    # Create formset for unbound and bound forms
    #  This allows continuing to add more items after saving.
    sda_formset = SubdisciplineAreaFormSet(queryset=SubdisciplineArea.objects.all().filter(subject_area_id=subject_area_id))

    return render_to_response('competencies/edit_subject_area.html',
                              {'school': school, 'subject_area': subject_area, 'sda_formset': sda_formset},
                              context_instance = RequestContext(request))


# --- Forking pages: pages related to forking an existing school ---
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

def new_school(request):
    """Creates a new school, then offers link to fork an existing
    school's competency system.
    """
    # Will need validation.
    new_school_name = request.POST['new_school_name']
    new_school_created = False
    new_school = None
    if new_school_name:
        # Create new school
        new_school = School(name=new_school_name)
        new_school.save()
        new_school_created = True
    return render_to_response('competencies/new_school.html',
                              {'new_school_name': new_school_name, 'new_school_created': new_school_created,
                               'new_school': new_school }, context_instance=RequestContext(request))
        

# --- Helper functions ---
def fork_school(forking_school, forked_school):
    """Forks a given school's competency system.  Copies all aspects of
    forked_school's competency system over to forking_school's system.
    Resets all keys to new school's system, so that forking_school gets
    an independent, isolated copy of the forked_school's system.

    Clearly, this is a long function that could be refactored.

    Test: Create a school, fork it, compare all hierarchical elements.
    """

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

                # Copy all essential understandings associated with this competency area
                eus = comp.essentialunderstanding_set.all()
                for eu in eus:
                    new_eu = copy(eu)
                    new_eu.pk, new_eu.id = None, None
                    new_eu.competency_area = new_comp
                    new_eu.save()
                
                    # Copy all learning targets associated with
                    #  this essential understanding:
                    copy_eu_lts(eu, new_eu)

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

                    # Copy all essential understandings associated with this competency area
                    eus = comp.essentialunderstanding_set.all()
                    for eu in eus:
                        new_eu = copy(eu)
                        new_eu.pk, new_eu.id = None, None
                        new_eu.competency_area = new_comp
                        new_eu.save()
                    
                        # Copy all learning targets associated with
                        #  this essential understanding:
                        copy_eu_lts(eu, new_eu)

def copy_eu_lts(eu, new_eu):
    """Copies all learning targets associated with existing essential understanding
    to a new essential understanding.
    """
    lts = eu.learningtarget_set.all()
    for lt in lts:
        new_lt = copy(lt)
        new_lt.pk, new_lt.id = None, None
        new_lt.essential_understanding = new_eu
        new_lt.save()
