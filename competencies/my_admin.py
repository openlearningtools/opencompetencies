"""Functions that help administer the site."""
import os

#from django.contrib.auth import createsuperuser
from django.contrib.auth.models import User
from django.db import IntegrityError

from competencies.models import *

def add_userprofile(user):
    """Make a new userprofile, and connect it to a new user."""
    new_userprofile = UserProfile()
    new_userprofile.user = user
    new_userprofile.save()

    
    
def initialize_data():
    """For use when re-creating the db locally."""
    # To use this, import into django shell and run it.
    # Should I restructure this to run it directly from cli?

    # Create superuser, and regular user.
    ru_username = os.environ['RU_USERNAME']
    su_username = os.environ['SU_USERNAME']

    try:
        su = User.objects.create_superuser(username=su_username,
                                           password=os.environ['SU_PASSWORD'],
                                           email='')
        add_userprofile(su)
        print("Created superuser %s." % su_username)
    except IntegrityError:
        print('The user %s already exists.' % su_username)
        su = User.objects.filter(username=su_username)[0]

    try:
        ru = User.objects.create_user(username=ru_username,
                                      password=os.environ['RU_PASSWORD'])
        add_userprofile(ru)
        print("Created regular user %s." % ru_username)
    except IntegrityError:
        print('The user %s already exists.' % ru_username)
        ru = User.objects.filter(username=ru_username)[0]

def build_test_schools(num_elements=2):
    """Build a set of test schools for dev work."""

    # DEV: This is quite redundant with tests.test_views.setUp().
    #  If I keep this, that redundancy should be removed somehow.

    # Build an organization, down to the performance indicator level.
    num_elements = num_elements

    user = User.objects.filter(username=os.environ['RU_USERNAME'])[0]
    su_user = User.objects.filter(username=os.environ['SU_USERNAME'])[0]

    # Build num_elements test organizations that user 0 is associated with,
    #  num_elements the user 1 is associated with.
    test_organizations, test_sas = [], []
    for organization_num in range(6):
        name = "Test Organization %d" % organization_num
        if organization_num < num_elements/2:
            new_organization = Organization.objects.create(name=name, owner=user)
            user.userprofile.organizations.add(new_organization)
        else:
            new_organization = Organization.objects.create(name=name, owner=su_user)
            su_user.userprofile.organizations.add(new_organization)
        test_organizations.append(new_organization)

        # Create num_elements subject areas for each organization.
        for sa_num in range(num_elements):
            sa_name = "Test SA %d-%d" % (organization_num, sa_num)
            new_sa = SubjectArea.objects.create(subject_area=sa_name,
                                                organization=new_organization)
            test_sas.append(new_sa)

            # Create num_elements grad standards for each subject area.
            for gs_num in range(num_elements):
                gs_body = "Test GS %d-%d-%d" % (organization_num, sa_num, gs_num)
                new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                           competency_area=gs_body)

                # Create num_elements perf indicators for each grad std.
                for pi_num in range(num_elements):
                    pi_body = "Test PI %d-%d-%d-%d" % (organization_num, sa_num, gs_num, pi_num)
                    new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                 competency_area=new_gs)

            # Create num_elements sdas for each sa.
            for sda_num in range(num_elements):
                sda_name = "Test SDA %d-%d-%d" % (organization_num, sa_num, sda_num)
                new_sda = SubdisciplineArea.objects.create(subject_area=new_sa,
                                                           subdiscipline_area=sda_name)

                # Create num_elements grad standards for each sda.
                for gs_num in range(num_elements):
                    gs_body = "Test GS %d-%d-%d-%d" % (organization_num, sa_num, sda_num, gs_num)
                    new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                               subdiscipline_area=new_sda,
                                                               competency_area=gs_body)

                    # Create num_elements perf indicators for each grad std.
                    for pi_num in range(num_elements):
                        pi_body = "Test PI %d-%d-%d-%d-%d" % (organization_num, sa_num, sda_num, gs_num, pi_num)
                        new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                     competency_area=new_gs)
