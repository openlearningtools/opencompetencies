from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.contrib.auth import logout
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required

from copy import copy
from collections import OrderedDict

from competencies.models import *


def index(request):
    sample_school = School.objects.get(name='Sample High School')
    pw_min_hs_grad = Pathway.objects.filter(school=sample_school).get(name='Minimum High School Graduation Requirements')
    pw_physicist = Pathway.objects.filter(school=sample_school).get(name='Physicist')

    return render_to_response('competencies/index.html',
                              {'sample_school': sample_school,
                               'pw_min_hs_grad': pw_min_hs_grad,
                               'pw_physicist': pw_physicist},
                              context_instance = RequestContext(request))

# Authentication views
def logout_view(request):
    logout(request)
    # Redirect to home page for now. Later, maybe stay on same page.
    return redirect('/')

def profile(request):
    return render_to_response('registration/profile.html',
                              {},
                              context_instance = RequestContext(request))

def password_change_form(request):
    if request.method == 'POST':
        return password_change(request, post_change_redirect='/password_change_successful')
    else:
        return render_to_response('registration/password_change_form.html',
                                  {},
                                  context_instance = RequestContext(request))

def password_change_successful(request):
    return render_to_response('registration/password_change_successful.html',
                              {},
                              context_instance = RequestContext(request))

# --- Simple views, for exploring system without changing it: ---
def schools(request):
    schools = School.objects.all()
    return render_to_response('competencies/schools.html', {'schools': schools}, context_instance=RequestContext(request))

def school(request, school_id):
    school = School.objects.get(id=school_id)
    return render_to_response('competencies/school.html', {'school': school},
                              context_instance = RequestContext(request))

def subject_area(request, subject_area_id):
    """Shows a subject area's subdiscipline areas, and competency areas."""
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    school = subject_area.school
    # Competencies for the general subject area (no associated sda):
    sa_competency_areas = subject_area.competencyarea_set.all().filter(subdiscipline_area=None)
    return render_to_response('competencies/subject_area.html',
                              {'subject_area': subject_area, 'school': school,
                               'sa_competency_areas': sa_competency_areas},
                              context_instance = RequestContext(request))

def subdiscipline_area(request, subdiscipline_area_id):
    """Shows all of the competency areas for a given subdiscipline area."""
    subdiscipline_area = SubdisciplineArea.objects.get(id=subdiscipline_area_id)
    subject_area = subdiscipline_area.subject_area
    school = subject_area.school
    competency_areas = subdiscipline_area.competencyarea_set.all()
    ca_levels = {}
    for ca in competency_areas:
        ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    return render_to_response('competencies/subdiscipline_area.html',
                              {'subdiscipline_area': subdiscipline_area, 'subject_area': subject_area,
                               'school': school, 'competency_areas': competency_areas,
                               'ca_levels': ca_levels},
                              context_instance = RequestContext(request))

def competency_area(request, competency_area_id):
    """Shows all of the essential understandings for a given competency area."""
    competency_area = CompetencyArea.objects.get(id=competency_area_id)
    subject_area = competency_area.subject_area
    school = subject_area.school
    essential_understandings = competency_area.essentialunderstanding_set.all()
    ca_levels = [Level.objects.get(pk=level_pk) for level_pk in competency_area.get_level_order()]
    return render_to_response('competencies/competency_area.html',
                              {'school': school, 'subject_area': subject_area, 'competency_area': competency_area,
                               'essential_understandings': essential_understandings,
                               'ca_levels': ca_levels},
                              context_instance = RequestContext(request))

def essential_understanding(request, essential_understanding_id):
    """Shows all learning targets for a given essential understanding."""
    essential_understanding = EssentialUnderstanding.objects.get(id=essential_understanding_id)
    competency_area = essential_understanding.competency_area
    ca_levels = [Level.objects.get(pk=level_pk) for level_pk in competency_area.get_level_order()]
    subject_area = competency_area.subject_area
    school = subject_area.school
    learning_targets = essential_understanding.learningtarget_set.all()
    return render_to_response('competencies/essential_understanding.html',
                              {'school': school, 'subject_area': subject_area, 'competency_area': competency_area,
                               'essential_understanding': essential_understanding, 'learning_targets': learning_targets,
                               'ca_levels': ca_levels},
                              context_instance = RequestContext(request))

def entire_system(request, school_id):
    """Shows the entire system for a given school."""
    school = School.objects.get(id=school_id)

    # Get filter for visibility, based on logged-in status.
    if request.user.is_authenticated():
        kwargs = {}
    else:
        kwargs = {'{0}'.format('public'): True}

    # all subject areas for a school
    sas = school.subjectarea_set.filter(**kwargs)
    # all subdiscipline areas for each subject area
    #  using OrderedDict to preserve order of subject areas
    sa_sdas = OrderedDict()
    for sa in sas:
        sa_sdas[sa] = sa.subdisciplinearea_set.filter(**kwargs)
    # all general competency areas for a subject
    #  need to preserve order for these as well
    sa_cas = OrderedDict()
    for sa in sas:
        sa_cas[sa] = sa.competencyarea_set.filter(subdiscipline_area=None).filter(**kwargs)
    # all competency areas for each subdiscipline area
    sda_cas = {}
    for sa in sas:
        for sda in sa_sdas[sa]:
            sda_cas[sda] = sda.competencyarea_set.filter(**kwargs)
    # all essential understandings for each competency area
    #  loop through all sa_cas, sda_cas
    # also grab level descriptions for each competency area
    ca_eus = {}
    ca_levels = {}
    for cas in sda_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.filter(**kwargs)
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    for cas in sa_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.filter(**kwargs)
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    # all learning targets for each essential understanding
    eu_lts = {}
    for eus in ca_eus.values():
        for eu in eus:
            eu_lts[eu] = eu.learningtarget_set.filter(**kwargs)

    return render_to_response('competencies/entire_system.html', 
                              {'school': school, 'subject_areas': sas,
                               'sa_sdas': sa_sdas, 'sa_cas': sa_cas,
                               'sda_cas': sda_cas, 'ca_eus': ca_eus,
                               'ca_levels': ca_levels, 'eu_lts': eu_lts},
                              context_instance = RequestContext(request))


# --- Edit views, for editing parts of the system ---
@login_required
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

@login_required
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

@login_required
def edit_sa_competency_areas(request, subject_area_id):
    """Allows user to edit the competencies for a general subject area."""
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    school = subject_area.school
    sa_comps = subject_area.competencyarea_set.all()

    # Build the sa_comp_area formset by using queryset to exclude all
    #  competency areas with a defined sda. Need general ca_formset to do this.
    CompetencyAreaFormSet = modelformset_factory(CompetencyArea, form=CompetencyAreaForm, exclude=('subject_area', 'subdiscipline_area'))

    if request.method == 'POST':
        # Process general sa competency areas:
        sa_ca_formset = CompetencyAreaFormSet(request.POST)
        if sa_ca_formset.is_valid():
            instances = sa_ca_formset.save(commit=False)
            for instance in instances:
                instance.subject_area = subject_area
                instance.save()

    # Create formsets for unbound and bound forms, to allow editing after saving.
    sa_ca_formset = CompetencyAreaFormSet(queryset=CompetencyArea.objects.all().filter(subject_area=subject_area).filter(subdiscipline_area=None))

    return render_to_response('competencies/edit_sa_competency_areas.html',
                              {'school': school, 'subject_area': subject_area, 'sa_ca_formset': sa_ca_formset},
                              context_instance = RequestContext(request))

@login_required
def edit_sda_competency_areas(request, subdiscipline_area_id):
    """Allows user to edit the competencies for a specific subdiscipline area."""
    subdiscipline_area = SubdisciplineArea.objects.get(id=subdiscipline_area_id)
    subject_area = subdiscipline_area.subject_area
    school = subject_area.school
    sda_comps = subdiscipline_area.competencyarea_set.all()

    # Build the sda_comp_area formset by using queryset 
    CompetencyAreaFormSet = modelformset_factory(CompetencyArea, form=CompetencyAreaForm, exclude=('subject_area', 'subdiscipline_area'))

    if request.method == 'POST':
        # Process sda competency areas:
        sda_ca_formset = CompetencyAreaFormSet(request.POST)
        if sda_ca_formset.is_valid():
            instances = sda_ca_formset.save(commit=False)
            for instance in instances:
                instance.subject_area = subject_area
                instance.subdiscipline_area = subdiscipline_area
                instance.save()

    # Create formsets for unbound and bound forms, to allow editing after saving.
    sda_ca_formset = CompetencyAreaFormSet(queryset=CompetencyArea.objects.all().filter(subdiscipline_area=subdiscipline_area))

    return render_to_response('competencies/edit_sda_competency_areas.html',
                              {'school': school, 'subject_area': subject_area,
                               'subdiscipline_area': subdiscipline_area, 'sda_ca_formset': sda_ca_formset},
                              context_instance = RequestContext(request))

@login_required
def edit_competency_area(request, competency_area_id):
    """Allows user to edit the essential understandings for a given competency area."""
    ca = CompetencyArea.objects.get(id=competency_area_id)
    sa = ca.subject_area
    sda = ca.subdiscipline_area
    school = sa.school

    EssentialUnderstandingFormSet = modelformset_factory(EssentialUnderstanding, form=EssentialUnderstandingForm)

    if request.method == 'POST':
        eu_formset = EssentialUnderstandingFormSet(request.POST)
        if eu_formset.is_valid():
            instances = eu_formset.save(commit=False)
            for instance in instances:
                instance.competency_area = ca
                instance.save()

    eu_formset = EssentialUnderstandingFormSet(queryset=ca.essentialunderstanding_set.all())

    return render_to_response('competencies/edit_competency_area.html',
                              {'school': school, 'subject_area': sa,
                               'subdiscipline_area': sda, 'competency_area': ca,
                               'eu_formset': eu_formset},
                              context_instance = RequestContext(request))

@login_required
def edit_levels(request, competency_area_id):
    """Allows user to edit levels for a given competency area."""
    ca = CompetencyArea.objects.get(id=competency_area_id)
    ca_levels = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    sa = ca.subject_area
    sda = ca.subdiscipline_area
    school = sa.school

    LevelFormSet = modelformset_factory(Level, form=LevelForm)
    #LevelFormSet = modelformset_factory(Level)

    if request.method == 'POST':
        level_formset = LevelFormSet(request.POST)
        if level_formset.is_valid():
            instances = level_formset.save(commit=False)
            for instance in instances:
                instance.competency_area = ca
                instance.save()
                # Ensure that ordering is correct
                #  (apprentice - technician - master - professional
                correct_order = []
                for type in [Level.APPRENTICE, Level.TECHNICIAN,
                             Level.MASTER, Level.PROFESSIONAL]:
                    try:
                        correct_order.append(Level.objects.get(competency_area=ca, level_type=type).pk)
                    except:
                        pass
                if ca.get_level_order() != correct_order:
                    ca.set_level_order(correct_order)

    level_formset = LevelFormSet(queryset=ca.level_set.all())

    return render_to_response('competencies/edit_levels.html',
                              {'school': school, 'subject_area': sa,
                               'subdiscipline_area': sda, 'competency_area': ca,
                               'level_formset': level_formset},
                              context_instance = RequestContext(request))


@login_required
def edit_essential_understanding(request, essential_understanding_id):
    """Allows user to edit the learning targets associated with an essential understanding."""
    eu = EssentialUnderstanding.objects.get(id=essential_understanding_id)
    ca = eu.competency_area
    sa = ca.subject_area
    sda = ca.subdiscipline_area
    school = sa.school

    LearningTargetFormSet = modelformset_factory(LearningTarget, form=LearningTargetForm, extra=3)

    if request.method == 'POST':
        lt_formset = LearningTargetFormSet(request.POST)
        if lt_formset.is_valid():
            instances = lt_formset.save(commit=False)
            for instance in instances:
                instance.essential_understanding = eu
                instance.save()

    lt_formset = LearningTargetFormSet(queryset=eu.learningtarget_set.all())

    return render_to_response('competencies/edit_essential_understanding.html',
                              {'school': school, 'subject_area': sa,
                               'subdiscipline_area': sda, 'competency_area': ca,
                               'essential_understanding': eu, 'lt_formset': lt_formset},
                              context_instance = RequestContext(request))

@login_required
def edit_order(request, school_id):
    """Shows the entire system for a given school,
    with links to change the order of any child element.
    """
    school = School.objects.get(id=school_id)
    # all subject areas for a school
    sas = school.subjectarea_set.all()
    # all subdiscipline areas for each subject area
    #  using OrderedDict to preserve order of subject areas
    sa_sdas = OrderedDict()
    for sa in sas:
        sa_sdas[sa] = sa.subdisciplinearea_set.all()
    # all general competency areas for a subject
    #  need to preserve order for these as well
    sa_cas = OrderedDict()
    for sa in sas:
        sa_cas[sa] = sa.competencyarea_set.all().filter(subdiscipline_area=None)
    # all competency areas for each subdiscipline area
    sda_cas = {}
    for sa in sas:
        for sda in sa_sdas[sa]:
            sda_cas[sda] = sda.competencyarea_set.all()
    # all essential understandings for each competency area
    #  loop through all sa_cas, sda_cas
    # also grab level descriptions for each competency area
    ca_eus = {}
    ca_levels = {}
    for cas in sda_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    for cas in sa_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    # all learning targets for each essential understanding
    eu_lts = {}
    for eus in ca_eus.values():
        for eu in eus:
            eu_lts[eu] = eu.learningtarget_set.all()

    return render_to_response('competencies/edit_order.html', 
                              {'school': school, 'subject_areas': sas,
                               'sa_sdas': sa_sdas, 'sa_cas': sa_cas,
                               'sda_cas': sda_cas, 'ca_eus': ca_eus,
                               'ca_levels': ca_levels, 'eu_lts': eu_lts},
                              context_instance = RequestContext(request))

@login_required
def change_order(request, school_id, parent_type, parent_id, child_type, child_id, direction):
    """Changes the order of the child element passed in, and redirects to edit_order.
    Requires parent_type to be a ModelName, and child_type to be a modelname.
    """
    school = School.objects.get(id=school_id)

    # Get parent object and order of children
    parent_object = get_model('competencies', parent_type).objects.get(id=parent_id)
    get_order_method = 'get_' + child_type + '_order'
    order = getattr(parent_object, get_order_method)()

    print 'old order', order

    # Set new order.
    child_index = order.index(int(child_id))
    set_order_method = 'set_' + child_type + '_order'
    if direction == 'up' and child_index != 0:
        if child_type == 'competencyarea':
            # Need to move before previous ca in given sda, or in general sa
            #  Get pks of all cas in this sda
            #  Get order, find prev element
            ca = CompetencyArea.objects.get(id=child_id)
            sda = ca.subdiscipline_area
            if sda:
                # pks for cas in this sda only
                ca_sda_pks = [ca.pk for ca in sda.competencyarea_set.all()]
            else:
                # sda None, this is a ca for a general sa
                # pks for cas in this general sa
                sa = ca.subject_area
                ca_sda_pks = [ca.pk for ca in sa.competencyarea_set.filter(subdiscipline_area=None)]
            current_ca_index = ca_sda_pks.index(int(child_id))
            if current_ca_index != 0:
                # move ca up in the subset
                # find pk of ca to switch with, then find index of that ca in order
                #  then switch the two indices
                target_ca_pk = ca_sda_pks[current_ca_index-1]
                target_ca_order_index = order.index(target_ca_pk)
                current_ca_order_index = order.index(int(child_id))
                order[current_ca_order_index], order[target_ca_order_index] = order[target_ca_order_index], order[current_ca_order_index]
                getattr(parent_object, set_order_method)(order)
        else:
            # Swap child id with element before it
            order[child_index], order[child_index-1] = order[child_index-1], order[child_index]
            getattr(parent_object, set_order_method)(order)
    if direction == 'down' and child_index != (len(order)-1):
        if child_type == 'competencyarea':
            # Need to move after next ca in given sda, or in general sa
            #  Get pks of all cas in this sda
            #  Get order, find next element
            ca = CompetencyArea.objects.get(id=child_id)
            sda = ca.subdiscipline_area
            if sda:
                # pks for cas in this sda only
                ca_sda_pks = [ca.pk for ca in sda.competencyarea_set.all()]
            else:
                # sda None, this is a ca for a general sa
                # pks for cas in this general sa
                sa = ca.subject_area
                ca_sda_pks = [ca.pk for ca in sa.competencyarea_set.filter(subdiscipline_area=None)]
            current_ca_index = ca_sda_pks.index(int(child_id))
            if current_ca_index != (len(ca_sda_pks)-1):
                # move ca down in the subset
                # find pk of ca to switch with, then find index of that ca in order
                #  then switch the two indices
                target_ca_pk = ca_sda_pks[current_ca_index+1]
                target_ca_order_index = order.index(target_ca_pk)
                current_ca_order_index = order.index(int(child_id))
                order[current_ca_order_index], order[target_ca_order_index] = order[target_ca_order_index], order[current_ca_order_index]
                getattr(parent_object, set_order_method)(order)
        else:
            # Swap child id with element after it
            order[child_index], order[child_index+1] = order[child_index+1], order[child_index]
            getattr(parent_object, set_order_method)(order)

    print 'new order:', order

    redirect_url = '/edit_order/' + school_id
    return redirect(redirect_url)

@login_required
def edit_visibility(request, school_id):
    """Allows user to set the visibility of any item in the school's system."""
    school = School.objects.get(id=school_id)
    # all subject areas for a school
    sas = school.subjectarea_set.all()
    # all subdiscipline areas for each subject area
    #  using OrderedDict to preserve order of subject areas
    sa_sdas = OrderedDict()
    for sa in sas:
        sa_sdas[sa] = sa.subdisciplinearea_set.all()
    # all general competency areas for a subject
    #  need to preserve order for these as well
    sa_cas = OrderedDict()
    for sa in sas:
        sa_cas[sa] = sa.competencyarea_set.all().filter(subdiscipline_area=None)
    # all competency areas for each subdiscipline area
    sda_cas = {}
    for sa in sas:
        for sda in sa_sdas[sa]:
            sda_cas[sda] = sda.competencyarea_set.all()
    # all essential understandings for each competency area
    #  loop through all sa_cas, sda_cas
    # also grab level descriptions for each competency area
    ca_eus = {}
    ca_levels = {}
    for cas in sda_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    for cas in sa_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
            ca_levels[ca] = [Level.objects.get(pk=level_pk) for level_pk in ca.get_level_order()]
    # all learning targets for each essential understanding
    eu_lts = {}
    for eus in ca_eus.values():
        for eu in eus:
            if request.user.is_authenticated():
                eu_lts[eu] = eu.learningtarget_set.all()
            else:
                eu_lts[eu] = eu.learningtarget_set.filter(public=True)

    return render_to_response('competencies/edit_visibility.html', 
                              {'school': school, 'subject_areas': sas,
                               'sa_sdas': sa_sdas, 'sa_cas': sa_cas,
                               'sda_cas': sda_cas, 'ca_eus': ca_eus,
                               'ca_levels': ca_levels, 'eu_lts': eu_lts},
                              context_instance = RequestContext(request))

@login_required    
def change_visibility(request, school_id, object_type, object_pk, visibility_mode):
    # Get object, and toggle attribute 'public'
    current_object = get_model('competencies', object_type).objects.get(pk=object_pk)
    # Hack to deal with bug around ordering
    #  Saving an object after toggling 'public' attribute can affect _order
    #  Probably need a custom migration that stops db from setting _order=0 on every save
    old_order = get_parent_order(current_object)
    if visibility_mode == 'public':
        # Need to check that parent is public
        if current_object.is_parent_public():
            current_object.public = True
            current_object.save()
            check_parent_order(current_object, old_order)
    elif visibility_mode == 'cascade_public':
        if current_object.is_parent_public():
            current_object.public = True
            current_object.save()
            check_parent_order(current_object, old_order)
            set_related_visibility(current_object, 'public')
    else:  # visibility mode == 'private'
        # Setting an object private implies all the elements under it should be private.
        current_object.public = False
        current_object.save()
        check_parent_order(current_object, old_order)
        set_related_visibility(current_object, 'private')

    redirect_url = '/edit_visibility/' + school_id
    return redirect(redirect_url)

def set_related_visibility(object_in, visibility_mode):
    """Finds all related objects, and sets them all to the appropriate visibility mode."""
    links = [rel.get_accessor_name() for rel in object_in._meta.get_all_related_objects()]
    for link in links:
        objects = getattr(object_in, link).all()
        for object in objects:
            try:
                # Hack to deal with ordering issue
                old_order = get_parent_order(object)
                if visibility_mode == 'public':
                    object.public = True
                    object.save()
                else:
                    object.public = False
                    object.save()
                check_parent_order(object, old_order)
            except:
                # Must not be a public/ private object
                pass
            # Check if this object has related objects, if so use recursion
            if object._meta.get_all_related_objects():
                set_related_visibility(object, visibility_mode)

# Methods to deal with ordering issue around order_with_respect_to
def check_parent_order(child_object, correct_order):
    """Hack to address ordering issue around order_with_respect_to."""
    if get_parent_order(child_object) != correct_order:
        set_parent_order(child_object, correct_order)

def get_parent_order(child_object):
    parent_object = child_object.get_parent()
    order_method = 'get_' + child_object.__class__.__name__.lower() + '_order'
    parent_order = getattr(parent_object, order_method)()
    return parent_order

def set_parent_order(child_object, order):
    parent_object = child_object.get_parent()
    order_method = 'set_' + child_object.__class__.__name__.lower() + '_order'
    getattr(parent_object, order_method)(order)


# --- Pathways pages ---
def pathways(request, school_id):
    """Lists all pathways for a given school."""
    school = School.objects.get(id=school_id)
    pathways = school.pathway_set.all()

    return render_to_response('competencies/pathways.html',
                              {'school': school, 'pathways': pathways},
                              context_instance = RequestContext(request))

def pathway(request, pathway_id):
    """Shows entire school system for a given pathway, with elements of the pathway highlighted."""
    pathway = Pathway.objects.get(id=pathway_id)
    school = pathway.school

    # data to render a school's entire system:
    # all subject areas for a school
    sas = school.subjectarea_set.all()
    # all subdiscipline areas for each subject area
    sa_sdas = {sa: sa.subdisciplinearea_set.all() for sa in sas}
    # all general competency areas for a subject
    sa_cas = {sa: sa.competencyarea_set.all().filter(subdiscipline_area=None) for sa in sas}
    # all competency areas for each subdiscipline area
    sda_cas = {}
    for sa in sas:
        for sda in sa_sdas[sa]:
            sda_cas[sda] = sda.competencyarea_set.all()
    # all essential understandings for each competency area
    #  loop through all sa_cas, sda_cas
    ca_eus = {}
    for cas in sda_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
    for cas in sa_cas.values():
        for ca in cas:
            ca_eus[ca] = ca.essentialunderstanding_set.all()
    # all learning targets for each essential understanding
    eu_lts = {}
    for eus in ca_eus.values():
        for eu in eus:
            eu_lts[eu] = eu.learningtarget_set.all()

    return render_to_response('competencies/pathway.html',
                              {'school': school, 'pathway': pathway, 'subject_areas': sas,
                               'sa_sdas': sa_sdas, 'sa_cas': sa_cas,
                               'sda_cas': sda_cas, 'ca_eus': ca_eus,
                               'eu_lts': eu_lts},
                              context_instance = RequestContext(request))

@login_required
def create_pathway(request, school_id):
    """Allows user to create a new pathway.
    Links to pages that edit the pathway.
    """
    school = School.objects.get(id=school_id)
    PathwayFormSet = modelformset_factory(Pathway, fields=('name',))
    saved_msg = ''

    if request.method == 'POST':
        pw_formset = PathwayFormSet(request.POST)
        if pw_formset.is_valid():
            instances = pw_formset.save(commit=False)
            for instance in instances:
                instance.school = school
                instance.save()
                saved_msg = 'Your changes were saved.'

    pw_formset = PathwayFormSet()

    return render_to_response('competencies/create_pathway.html',
                              {'school': school,
                               'pw_formset': pw_formset, 'saved_msg': saved_msg,},
                              context_instance = RequestContext(request))

@login_required
def edit_pathway(request, pathway_id):
    """Allows a user to add or remove elements in a pathway."""
    pathway = Pathway.objects.get(id=pathway_id)
    school = pathway.school
    saved_msg = ''

    # Only include relevant parts of a pathway
    #  If empty pathway, only show subject areas
    #  If subject areas defined, show sdas...
    PathwayFormSet = modelformset_factory(Pathway, form=PathwayForm, fields=get_fields(pathway), extra=0)

    if request.method == 'POST':
        pw_formset = PathwayFormSet(request.POST)
        if pw_formset.is_valid():
            instances = pw_formset.save(commit=True)
            saved_msg = 'Your changes were saved.'
        else:
            # debugging:
            pass #saved_msg = 'Invalid form.' + str(pw_formset.errors)

    # Get new formset, based on updated pathway object
    PathwayFormSet = modelformset_factory(Pathway, form=PathwayForm, fields=get_fields(pathway), extra=0)

    pw_formset = PathwayFormSet(queryset=Pathway.objects.all().filter(id=pathway_id))

    return render_to_response('competencies/edit_pathway.html',
                              {'school': school,
                               'pathway': pathway, 'pw_formset': pw_formset,
                               'saved_msg': saved_msg,
                               },
                              context_instance = RequestContext(request))

def get_fields(pathway):
    fields = ['name', 'subject_areas',]
    if pathway.subject_areas.all():
        fields.append('subdiscipline_areas',)
        fields.append('competency_areas',)
    if pathway.competency_areas.all():
        fields.append('essential_understandings',)
    if pathway.essential_understandings.all():
        fields.append('learning_targets',)

    return tuple(fields)


# --- Forking pages: pages related to forking an existing school ---
@login_required
def fork(request, school_id):
    empty_school = School.objects.get(id=school_id)
    # Only get schools that have at least one subject area:
    forkable_schools = [school for school in School.objects.all() if school.subjectarea_set.all()]
    return render_to_response('competencies/fork.html',
                              {'empty_school': empty_school, 'forkable_schools': forkable_schools},
                              context_instance = RequestContext(request))

@login_required
def confirm_fork(request, forking_school_id, forked_school_id):
    """Forks the requested school, and confirms success."""
    forking_school = School.objects.get(id=forking_school_id)
    forked_school = School.objects.get(id=forked_school_id)
    fork_school(forking_school, forked_school)
    return render_to_response('competencies/confirm_fork.html',
                              {'forking_school': forking_school, 'forked_school': forked_school},
                              context_instance = RequestContext(request))

@login_required
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
