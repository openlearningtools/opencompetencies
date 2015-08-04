"""Helper functions for views.py."""
from competencies.models import Organization


def cascade_visibility_down(element, visibility_mode):
    """Sets visibility for all descendents of an element. (cascades down)."""
    # Does nothing to given element.
    
    # Find all related objects, and set them all to the appropriate visibility mode.
    links = [rel.get_accessor_name() for rel in element._meta.get_all_related_objects()]
    for link in links:
        objects = getattr(element, link).all()
        for object in objects:
            try:
                if visibility_mode == 'private':
                    if object.public:
                        object.public = False
                        object.save()
                elif visibility_mode == 'public':
                    if not object.public:
                        object.public = True
                        object.save()
            except Exception as e:
                # Must not be a public/ private object
                print("Can't set object private:", object, e)

            # Check if this object has related objects, if so continue cascading.
            if object._meta.get_all_related_objects():
                cascade_visibility_down(object, visibility_mode)

def cascade_public_up(element):
    """Sets visibility to public for all ancestors of an element. (cascades up)."""
    # Does nothing to given element.
    # Does not affect organization; that is managed separately.
    #   This allows an organization to be set up, and then made visible all at once.
    # Only sets elements public, because I can't see any reason to cascade private upwards.

    element = element.get_parent()
    while element.__class__ != Organization:
        if not element.public:
            element.public = True
            element.save()
        # Get next parent element.
        element = element.get_parent()

def fork_organization(forking_org, original_org):
    """Copy all elements of original_org to forking_org."""
    # Make sure forking_org is empty, and original_org is public.
    # Make sure original_org is public, and forking_org is empty.
    print("Forking", original_org.name, "to", forking_org.name, "...")
    if not original_org.public:
        print("Can't fork - original org is private.")
        return None
    if forking_org.subjectarea_set.all():
        print("Can't fork - forking org is not empty.")
        return None
    if original_org == forking_org:
        print("Can't fork - original org is forking org.")
        return None

    # Copy all elements from original to forking org.
    #   There's definitely a more efficient way to do this, but quick and dirty for now.
    #   (Follow relations automatically.)
    # DEV: Copy public elements only.
    from copy import deepcopy
    for sa in original_org.subjectarea_set.filter(public=True):
        original_sa = deepcopy(sa)
        sa.pk = None
        sa.organization = forking_org
        sa.save()

        # Copy this sa's sdas.
        for sda in original_sa.subdisciplinearea_set.filter(public=True):
            original_sda = deepcopy(sda)
            sda.pk = None
            sda.subject_area = sa
            sda.save()

            # Copy this sda's cas.
            for ca in original_sda.competencyarea_set.filter(public=True):
                original_ca = deepcopy(ca)
                ca.pk = None
                ca.subject_area = sa
                ca.subdiscipline_area = sda
                ca.save()

                # Copy this ca's eus.
                for eu in original_ca.essentialunderstanding_set.filter(public=True):
                    eu.pk = None
                    eu.competency_area = ca
                    eu.save()

        # Copy this sa's cas.
        for ca in original_sa.competencyarea_set.filter(subdiscipline_area=None):
            original_ca = deepcopy(ca)
            ca.pk = None
            ca.subject_area = sa
            ca.save()
            
            # Copy this ca's eus.
            for eu in original_ca.essentialunderstanding_set.filter(public=True):
                eu.pk = None
                eu.competency_area = ca
                eu.save()
