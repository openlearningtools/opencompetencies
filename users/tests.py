from random import choice

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from users.models import *
from competencies.models import Organization
from competencies import my_admin, utils

from competencies import my_admin

class UserViewTests(TestCase):
    """Tests for all views in users."""
    # May want to use simpler password hashing in tests.
    #  https://docs.djangoproject.com/en/1.8/topics/testing/overview/#speeding-up-the-tests

    # Uses some functions that are copied directly from competencies.tests.
    #  Watch for these getting out of sync.

    def setUp(self):
        # Build an organization, down to the performance indicator level.
        self.num_orgs = 2
        self.num_elements = 2
        self.client = Client()

        # Create 2 test users.
        self.test_user_0 = User.objects.create_user(username='testuser0', password='pw')
        new_up = UserProfile(user=self.test_user_0)
        new_up.save()

        self.test_user_1 = User.objects.create_user(username='testuser1', password='pw')
        new_up = UserProfile(user=self.test_user_1)
        new_up.save()

        # Empty lists of elements.
        self.test_organizations = []

        # Increment for every element created.
        #   Ensures a unique name for every element, which makes testing some behaviors easier.
        self.element_number = 0

    def build_to_organizations(self):
        """Build out system to the organization level."""
        # Build a test organization that user 0 is associated with,
        #  and one that user 1 is associated with.
        # If a test only needs one org, it can set self.num_orgs = 1.
        for organization_num in range(2):
            name = "Test Organization %d" % organization_num
            if organization_num < self.num_orgs/2:
                new_organization = Organization.objects.create(name=name, owner=self.test_user_0)
                new_organization.editors.add(self.test_user_0)
            else:
                new_organization = Organization.objects.create(name=name, owner=self.test_user_1)
                new_organization.editors.add(self.test_user_1)
            self.test_organizations.append(new_organization)


    def test_login_view(self):
        """Lets user log in."""
        test_url = reverse('users:login')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        """Lets new user register an account."""
        test_url = reverse('users:register')
        self.generic_test_blank_form(test_url)

        # Test new user can be created, and userprofile connected properly.
        response = self.client.post(test_url, {'username': 'ozzy', 'email': '',
                                               'password1': 'pw', 'password2': 'pw',
                                               })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.filter(username='ozzy')[0]
        self.assertTrue(hasattr(new_user, 'userprofile'))

    def test_profile_view(self):
        """Lets user view their profile details."""
        self.build_to_organizations()
        test_url = reverse('users:profile')
        # Test that anonymous users are redirected.
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)

        # Test that registered users see appropriate information.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('testuser0' in response.content.decode())
        for user in User.objects.all():
            if user.username == 'testuser0':
                break
        for org in user.organization_set.all():
            self.assertTrue(org.name in response.content.decode())


    def generic_test_blank_form(self, test_url):
        """A helper method to test that a form-based page returns a blank form properly."""
        # Test that a logged in user can get a blank form properly.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)



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


class MyAdminTests(TestCase):
    """Test individual functions in my_admin.py."""

    def test_add_userprofile(self):
        """Make sure new user gets a userprofile."""
        new_user = User.objects.create_user(username='randy', password='pw')
        my_admin.add_userprofile(new_user)
        self.assertTrue(hasattr(new_user, 'userprofile'))
