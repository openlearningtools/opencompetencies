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

