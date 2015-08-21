from django.test import TestCase
from django.contrib.auth.models import User

from competencies.models import *
from competencies import my_admin

class MyAdminTests(TestCase):
    """Test individual functions in my_admin.py."""

    def test_add_userprofile(self):
        """Make sure new user gets a userprofile."""
        new_user = User.objects.create_user(username='randy', password='pw')
        my_admin.add_userprofile(new_user)
        self.assertTrue(hasattr(new_user, 'userprofile'))
