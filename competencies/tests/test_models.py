from django.test import TestCase
from django.contrib.auth.models import User

from competencies.models import *


class ModelTests(TestCase):
    """Test aspects of models."""

    def test_userprofile(self):
        """Test that a userprofile connects properly to a user."""
        new_user = User()
        new_user.username = 'new_user'
        new_user.password = 'new_user_pw'
        new_user.save()

        new_up = UserProfile()
        new_up.user = new_user
        new_up.save()

        self.assertEqual(new_user.userprofile, new_up)
