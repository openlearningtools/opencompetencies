"""Functions that help administer the site."""

from competencies.models import UserProfile

def add_userprofile(user):
    """Make a new userprofile, and connect it to a new user."""
    new_userprofile = UserProfile()
    new_userprofile.user = user
    new_userprofile.save()

    
    
