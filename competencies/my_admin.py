"""Functions that help administer the site."""

from competencies.models import UserProfile

def create_user():
    """Creates a new user, and attaches a userprofile to the new user."""
    # pass

def add_userprofile(user):
    """Make a new userprofile, and connect it to a new user."""
    new_userprofile = UserProfile()
    new_userprofile.user = user
    new_userprofile.save()

    
    
