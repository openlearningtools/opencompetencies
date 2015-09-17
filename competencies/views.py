from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.apps import apps
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from copy import copy
from collections import OrderedDict

from competencies.models import *
from competencies.forms import ForkForm
from competencies import my_admin
from . import utils


def index(request):
    return render_to_response('competencies/index.html',
                              {},
                              context_instance=RequestContext(request))

# --- Authorization views ---
def no_edit_permission(request, school_id):
    """Displays message that user does not have permission to make requested edits."""
    school = Organization.objects.get(id=school_id)
    return render_to_response('competencies/no_edit_permission.html',
                              {'school': school},
                              context_instance=RequestContext(request))

# --- Simple views, for exploring system without changing it: ---
def organizations(request):
    my_organizations, editor_organizations = [], []
    if request.user.is_authenticated():
        my_organizations = Organization.objects.filter(owner=request.user)
        editor_organizations = request.user.organization_set.all()
    # Remove owned orgs from editor_organizations
    editor_organizations = [org for org in editor_organizations if org not in my_organizations]
    public_organizations = Organization.objects.filter(public=True)
    return render_to_response('competencies/organizations.html',
                              {'my_organizations': my_organizations,
                               'editor_organizations': editor_organizations,
                               'public_organizations': public_organizations,
                               },
                              context_instance=RequestContext(request))

def organization(request, organization_id):
    """Displays subject areas and subdiscipline areas for a given organization."""
    organization = Organization.objects.get(id=organization_id)
    editors = organization.editors.all()
    if organization.subjectarea_set.all():
        can_fork = False
    else:
        can_fork = True
    kwargs = get_visibility_filter(request.user, organization)
    sas = organization.subjectarea_set.filter(**kwargs)
    sdas = [sda for sa in sas for sda in sa.subdisciplinearea_set.filter(**kwargs)]    
    return render_to_response('competencies/organization.html',
                              {'organization': organization, 'subject_areas': sas,
                               'sdas': sdas, 'can_fork': can_fork,
                               'editors': editors,
                               },
                              context_instance=RequestContext(request))

def sa_summary(request, sa_id):
    """Shows a simple summary for a subject area."""
    sa = SubjectArea.objects.get(id=sa_id)
    organization = sa.organization
    kwargs = get_visibility_filter(request.user, organization)

    sdas, cas, eus = get_sda_ca_eu_elements(sa, kwargs)
    
    return render_to_response('competencies/sa_summary.html',
                              {'subject_area': sa, 'organization': organization,
                               'sdas': sdas, 'cas': cas, 'eus': eus,},
                              context_instance=RequestContext(request))

def sa_summary_pdf(request, sa_id):
    """Return a pdf of the sa_summary page."""
    #print('Generating pdf of sa_summary...')

    sa = SubjectArea.objects.get(id=sa_id)
    org = sa.organization
    kwargs = get_visibility_filter(request.user, org)

    sdas, cas, eus = get_sda_ca_eu_elements(sa, kwargs)

    response = HttpResponse(content_type='application/pdf')
    filename = 'sa_summary_%s.pdf' % sa.subject_area
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    from competencies.sa_summary_pdf import PDFTest
    pdf_test = PDFTest(response)
    pdf = pdf_test.makeSummary(org, sa, sdas, cas, eus)

    return pdf

@login_required
def organization_admin_summary(request, organization_id):
    """See an administrative summmary of an organization. Restricted to owners of the org."""
    organization = Organization.objects.get(id=organization_id)
    # Make sure user owns this org.
    if request.user != organization.owner:
        return redirect(reverse('competencies:organizations'))

    editors = organization.editors.all()

    return render_to_response('competencies/organization_admin_summary.html',
                              {'organization': organization, 'editors': editors,
                               },
                              context_instance=RequestContext(request))


# --- Views for editing content. ---
@login_required
def organization_admin_edit(request, organization_id):
    """Administer an organization. Restricted to owners of the org."""
    # DEV: This page will need a list of the organization's editors.

    organization = Organization.objects.get(id=organization_id)
    # Make sure user owns this org.
    if request.user != organization.owner:
        return redirect(reverse('competencies:organizations'))

    if request.method != 'POST':
        organization_form = OrganizationAdminForm(instance=organization)
    else:
        organization_form = OrganizationAdminForm(request.POST, instance=organization)
        if organization_form.is_valid():
            organization_form.save()
            # If org has been made private, set all elements private.
            if 'public' in organization_form.changed_data:
                if not organization_form.cleaned_data.get('public'):
                    utils.cascade_visibility_down(organization, 'private')

        # Make sure no organization owner was not removed from editors.
        # DEV: Should prevent this from happening at all, by overriding form.save()?
        if organization.owner not in organization.editors.all():
            organization.editors.add(organization.owner)

        # Redirect to summary page after processing form.
        return redirect(reverse('competencies:organization_admin_summary', args=[organization_id]))

    return render_to_response('competencies/organization_admin_edit.html',
                              {'organization': organization, 'organization_form': organization_form,
                               },
                              context_instance=RequestContext(request))
                                  
@login_required
def fork(request, organization_id):
    """Fork an existing school."""
    forking_organization = Organization.objects.get(id=organization_id)
    if request.method != 'POST':
        fork_form = ForkForm()
    else:
        fork_form = ForkForm(request.POST)
        if fork_form.is_valid():
            original_org = Organization.objects.get(pk=request.POST['organization'])
            utils.fork_organization(forking_organization, original_org)
            return redirect(reverse('competencies:organization', args=[organization_id,]))
        else:
            #print('\n\ninvalid:', fork_form)
            # Report error appropriately.
            pass

    return render_to_response('competencies/fork.html',
                              {'forking_organization': forking_organization,
                               'organizations': organizations,
                               'fork_form': fork_form,
                               },
                              context_instance=RequestContext(request))

@login_required
def edit_sa_summary(request, sa_id):
    """Edit the elements in sa_summary."""
    # This should work for a given sa_id, or with no sa_id.
    # Have an id, edit a subject area.
    # No id, create a new subject area.

    subject_area = SubjectArea.objects.get(id=sa_id)
    organization = subject_area.organization
    kwargs = get_visibility_filter(request.user, organization)

    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    sdas, cas, eus = get_sda_ca_eu_elements(subject_area, kwargs)

    # Respond to submitted data.
    if request.method == 'POST':
        # Store elements that have had their privacy setting changed,
        #   for processing after all forms have been processed.
        privacy_changed = []
        process_form(request, subject_area, 'sa', privacy_changed)
        for sda in sdas:
            process_form(request, sda, 'sda', privacy_changed)
        for ca in cas:
            process_form(request, ca, 'ca', privacy_changed)
        for eu in eus:
            process_form(request, eu, 'eu', privacy_changed)

        # Cascade privacy settings appropriately.
        #   Change to private takes precedence, so process changes to public first.
        changed_to_public = [element for element in privacy_changed if element.public]
        changed_to_private = [element for element in privacy_changed if not element.public]

        # Cascading public happens upwards. Setting an element public makes all its
        #   ancestors public.
        for element in changed_to_public:
            utils.cascade_public_up(element)
        
        # Cascading private happens downwards. Setting an element private hides all
        #   its descendants.
        for element in changed_to_private:
            utils.cascade_visibility_down(element, 'private')

        # If any privacy settings were changed, need to refresh elements
        #   to make sure forms are based on updated elements.
        subject_area = SubjectArea.objects.get(id=sa_id)
        organization = subject_area.organization
        sdas, cas, eus = get_sda_ca_eu_elements(subject_area, kwargs)

        # Redirect back to view page.
        return redirect('/sa_summary/%s' % sa_id)

    # Build forms. Not in an else clause, because even POST requests need
    #  forms re-generated.
    sa_form = generate_form(subject_area, 'sa')
    sda_forms = []
    for sda in sdas:
        sda_form = generate_form(sda, 'sda')
        sda_form.my_id = sda.id
        sda_forms.append(sda_form)
    zipped_sda_forms = list(zip(sdas, sda_forms))

    ca_forms = []
    for ca in cas:
        ca_form = generate_form(ca, 'ca')
        ca_form.my_id = ca.id
        ca_forms.append(ca_form)
    zipped_ca_forms = list(zip(cas, ca_forms))

    eu_forms = []
    for eu in eus:
        eu_form = generate_form(eu, 'eu')
        eu_form.my_id = eu.id
        eu_forms.append(eu_form)
    zipped_eu_forms = list(zip(eus, eu_forms))
    

    return render_to_response('competencies/edit_sa_summary.html',
                              {'subject_area': subject_area, 'organization': organization,
                               'sdas': sdas, 'cas': cas, 'eus': eus,
                               'sa_form': sa_form,
                               'zipped_sda_forms': zipped_sda_forms,
                               'zipped_ca_forms': zipped_ca_forms,
                               'zipped_eu_forms': zipped_eu_forms,
                               },
                              context_instance=RequestContext(request))

def edit_sa_summary_order(request, sa_id):
    """Modify the order of sdas, cas, and eus within a subject area."""

    subject_area = SubjectArea.objects.get(id=sa_id)
    organization = subject_area.organization
    kwargs = get_visibility_filter(request.user, organization)

    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    sdas, cas, eus = get_sda_ca_eu_elements(subject_area, kwargs)


    return render_to_response('competencies/edit_sa_summary_order.html',
                              {'subject_area': subject_area, 'organization': organization,
                               'sdas': sdas, 'cas': cas, 'eus': eus,
                               },
                              context_instance=RequestContext(request))

def move_element(request, element_type, element_id, direction, sa_id):
    """Modify the position of an element within its set of elements."""
    # Get the element whose position is being changed, get its order,
    #   and modify the order if appropriate.
    sa = SubjectArea.objects.get(id=sa_id)
    edit_order_url = reverse('competencies:edit_sa_summary_order', args=[sa.id])
    object_to_move = get_model('competencies', element_type).objects.get(id=element_id)
    order = get_parent_order(object_to_move)

    # Make sure user can edit this organization.
    if request.user not in sa.organization.editors.all():
        redirect_url = reverse('competencies:index')
        return redirect(redirect_url)
    
    # If element_type is ca, get group of cas with no sda or same sda,
    #   then get ca to switch with.
    if element_type == 'CompetencyArea':
        ca = object_to_move
        if not ca.subdiscipline_area:
            ca_group = sa.competencyarea_set.filter(subdiscipline_area=None)
        else:
            ca_group = sa.competencyarea_set.filter(subdiscipline_area=ca.subdiscipline_area)
        for index, cand_ca in enumerate(ca_group):
            if cand_ca == ca:
                ca_index = index
        if direction == 'up' and ca_index > 0:
            ca_target = ca_group[ca_index-1]
        elif direction == 'down' and ca_index < len(ca_group)-1:
            ca_target = ca_group[ca_index+1]
        else:
            return(redirect(edit_order_url))

        # Get indices in order, and swap positions.
        original_index = order.index(ca.id)
        target_index = order.index(ca_target.id)
        order[original_index], order[target_index] = order[target_index], order[original_index]
        set_parent_order(object_to_move, order)
        return(redirect(edit_order_url))
    
    # Get index of element_id, switch places with previous or next element.
    index = order.index(int(element_id))
    if direction == 'up' and index > 0:
        order[index], order[index-1] = order[index-1], order[index]
        set_parent_order(object_to_move, order)
    elif direction == 'down' and index < len(order) - 1:
        order[index], order[index+1] = order[index+1], order[index]
        set_parent_order(object_to_move, order)

    return redirect(edit_order_url)

@login_required
def delete_element(request, element_type, element_id):
    """Confirm that user wants to delete an element, and all its descendants.
    Option to cancel, which will go back to edit_sa_summary,
    or delete element which will then redirect to sa_summary."""
    #  GET request shows confirmation form; POST request follows through on delete.

    # DEV: This needs to be generalized.
    model = apps.get_model(app_label='competencies', model_name=element_type)
    object_to_delete = model.objects.get(id=element_id)
    org = object_to_delete.get_organization()

    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, org):
        redirect_url = '/no_edit_permission/' + str(org.id)
        return redirect(redirect_url)

    # Get sa, regardless of which element is being deleted.
    cand_sa = object_to_delete
    while cand_sa.__class__.__name__ != 'SubjectArea':
        cand_sa = cand_sa.get_parent()
    sa = cand_sa

    # Get related elements that will be deleted.
    from django.contrib.admin.utils import NestedObjects
    from django.db import DEFAULT_DB_ALIAS
    collector = NestedObjects(using=DEFAULT_DB_ALIAS)
    collector.collect([object_to_delete])
    try:
        cascade_elements = collector.nested()[1]
    except IndexError:
        cascade_elements = []
        
    if request.method == 'POST' and request.POST['confirm_delete']:
        object_to_delete.delete()
        return redirect(reverse('competencies:sa_summary', args=[sa.id,]))

    return render_to_response('competencies/delete_element.html',
                              {'organization': org, 'subject_area': sa,
                               'object_to_delete': object_to_delete,
                               'cascade_elements': cascade_elements,
                               },
                              context_instance=RequestContext(request))


def get_sda_ca_eu_elements(subject_area, kwargs):
    """Get all sdas, cas, and eus associated with a subject area."""
    sdas = subject_area.subdisciplinearea_set.filter(**kwargs)
    cas = subject_area.competencyarea_set.filter(**kwargs)
    eus = []
    for ca in cas:
        for eu in ca.essentialunderstanding_set.filter(**kwargs):
            eus.append(eu)
    return (sdas, cas, eus)

def process_form(request, instance, element_type, privacy_changed):
    """Process a form for a single element."""
    prefix = '%s_form_%d' % (element_type, instance.id)

    if element_type == 'sa':
        form = SubjectAreaForm(request.POST, instance=instance)
    elif element_type == 'sda':
        form = SubdisciplineAreaForm(request.POST, prefix=prefix, instance=instance)
    elif element_type == 'ca':
        form = CompetencyAreaForm(request.POST, prefix=prefix, instance=instance)
    elif element_type == 'eu':
        form = EssentialUnderstandingForm(request.POST, prefix=prefix, instance=instance)

    if form.is_valid():
        modified_element = form.save()
        # If privacy setting changed, add to list for processing.
        if 'public' in form.changed_data:
            privacy_changed.append(modified_element)

    return form

def generate_form(instance, element_type):
    """Generate a form for a single element."""
    prefix = '%s_form_%d' % (element_type, instance.id)

    if element_type == 'sa':
        return SubjectAreaForm(instance=instance)
    elif element_type == 'sda':
        return SubdisciplineAreaForm(prefix=prefix, instance=instance)
    elif element_type == 'ca':
        return CompetencyAreaForm(prefix=prefix, instance=instance)
    elif element_type == 'eu':
        return EssentialUnderstandingForm(prefix=prefix, instance=instance)

def new_sa(request, org_id):
    """Create a new subject area for a given organization."""
    organization = Organization.objects.get(id=org_id)
    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    if request.method == 'POST':
        sa_form = SubjectAreaForm(request.POST)
        if sa_form.is_valid():
            new_sa = sa_form.save(commit=False)
            new_sa.organization = organization
            new_sa.save()
            return redirect('/edit_sa_summary/%d' % new_sa.id)

    sa_form = SubjectAreaForm()

    return render_to_response('competencies/new_sa.html',
                              {'organization': organization, 'sa_form': sa_form,},
                              context_instance=RequestContext(request))

def new_sda(request, sa_id):
    """Create a new subdiscipline area for a given subject area."""
    sa = SubjectArea.objects.get(id=sa_id)
    organization = sa.organization
    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    if request.method == 'POST':
        sda_form = SubdisciplineAreaForm(request.POST)
        if sda_form.is_valid():
            new_sda = sda_form.save(commit=False)
            new_sda.subject_area = sa
            new_sda.save()
            return redirect('/edit_sa_summary/%d' % sa.id)

    sda_form = SubdisciplineAreaForm()

    return render_to_response('competencies/new_sda.html',
                              {'organization': organization, 'sa': sa,
                               'sda_form': sda_form,},
                              context_instance=RequestContext(request))

def new_ca(request, sa_id):
    """Create a new competency area for a given general subject area."""
    sa = SubjectArea.objects.get(id=sa_id)
    organization = sa.organization
    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    if request.method == 'POST':
        ca_form = CompetencyAreaForm(request.POST)
        if ca_form.is_valid():
            new_ca = ca_form.save(commit=False)
            new_ca.subject_area = sa
            new_ca.save()
            return redirect('/edit_sa_summary/%d' % sa.id)

    ca_form = CompetencyAreaForm()

    return render_to_response('competencies/new_ca.html',
                              {'organization': organization, 'sa': sa, 'ca_form': ca_form,},
                              context_instance=RequestContext(request))

def new_sda_ca(request, sda_id):
    """Create a new competency area for a given subdiscipline area."""
    sda = SubdisciplineArea.objects.get(id=sda_id)
    sa = sda.subject_area
    organization = sa.organization
    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    if request.method == 'POST':
        ca_form = CompetencyAreaForm(request.POST)
        if ca_form.is_valid():
            new_ca = ca_form.save(commit=False)
            new_ca.subject_area = sa
            new_ca.subdiscipline_area = sda
            new_ca.save()
            return redirect('/edit_sa_summary/%d' % sa.id)

    ca_form = CompetencyAreaForm()

    return render_to_response('competencies/new_sda_ca.html',
                              {'organization': organization, 'sa': sa, 'sda': sda,
                               'ca_form': ca_form,},
                              context_instance=RequestContext(request))

def new_eu(request, ca_id):
    """Create a new essential understanding for given ca."""
    ca = CompetencyArea.objects.get(id=ca_id)
    sa = ca.subject_area
    organization = sa.organization
    # Test if user allowed to edit this organization.
    if not has_edit_permission(request.user, organization):
        redirect_url = '/no_edit_permission/' + str(organization.id)
        return redirect(redirect_url)

    if request.method == 'POST':
        eu_form = EssentialUnderstandingForm(request.POST)
        if eu_form.is_valid():
            new_eu = eu_form.save(commit=False)
            new_eu.competency_area = ca
            new_eu.save()
            return redirect('/edit_sa_summary/%d' % sa.id)

    eu_form = EssentialUnderstandingForm()

    return render_to_response('competencies/new_eu.html',
                              {'organization': organization, 'sa': sa, 'ca': ca,
                               'eu_form': eu_form,},
                              context_instance=RequestContext(request))
    

# helper methods to get elements of the system.

def get_visibility_filter(user, organization):
    # Get filter for visibility, based on logged-in status.
    if user.is_authenticated() and user in organization.editors.all():
        kwargs = {}
    else:
        kwargs = {'{0}'.format('public'): True}
    return kwargs

# --- Edit views, for editing parts of the system ---
def has_edit_permission(user, organization):
    """Checks whether given user has permission to edit given object.
    """
    # Returns True if allowed to edit, False if not allowed to edit
    if user in organization.editors.all():
        return True
    else:
        return False


# Methods to deal with ordering issue around order_with_respect_to
def check_parent_order(child_object, correct_order):
    """Hack to address ordering issue around order_with_respect_to."""
    if get_parent_order(child_object) != correct_order:
        set_parent_order(child_object, correct_order)

def get_parent_order(child_object):
    parent_object = child_object.get_parent()
    # DEV: May make ca.get_parent() always return sa?
    if parent_object.__class__.__name__ == 'SubdisciplineArea':
        parent_object = parent_object.subject_area
    order_method = 'get_' + child_object.__class__.__name__.lower() + '_order'
    parent_order = getattr(parent_object, order_method)()
    return parent_order

def set_parent_order(child_object, order):
    parent_object = child_object.get_parent()
    # DEV: May make ca.get_parent() always return sa?
    if parent_object.__class__.__name__ == 'SubdisciplineArea':
        parent_object = parent_object.subject_area
    order_method = 'set_' + child_object.__class__.__name__.lower() + '_order'
    getattr(parent_object, order_method)(order)

@login_required
def new_organization(request):
    """Creates a new organization."""

    if request.method == 'POST':
        new_organization_form = OrganizationForm(request.POST)
        if new_organization_form.is_valid():
            new_organization = new_organization_form.save(commit=False)
            new_organization.owner = request.user
            new_organization.save()
            new_organization.editors.add(request.user)
            return redirect(reverse('competencies:organizations'))

    new_organization_form = OrganizationForm()

    return render_to_response('competencies/new_organization.html',
                              {'new_organization_form': new_organization_form,},
                              context_instance=RequestContext(request))

