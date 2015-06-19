from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from competencies.models import *


class CompetencyViewTests(TestCase):
    """Needed tests:
    - queryset tests for all pages
    - no-data tests
    """

    def setUp(self):
        self.test_school = School.objects.create(name="Test School")
        self.test_sa = SubjectArea.objects.create(subject_area="Science", school=self.test_school)

    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        self.assertEqual(response.status_code, 200)

    def test_schools_view(self):
        """Schools page lists all schools, links to detail view of that school."""
        response = self.client.get(reverse('competencies:schools'))
        self.assertEqual(response.status_code, 200)

    def test_school_view(self):
        """School page lists subject areas and subdiscipline areas for that school."""
        response = self.client.get(reverse('competencies:school', args=(self.test_school.id,)))
        self.assertEqual(response.status_code, 200)

    def test_new_school(self):
        """New school processes form to create a new school.
        """
        pass


class FormTests(TestCase):
    """Test the custom forms in OC."""

    def test_registeruserform(self):
        """Test that the registration form works."""
        form = RegisterUserForm()
        # finish!


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
