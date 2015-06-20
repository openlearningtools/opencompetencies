from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from competencies.models import *
from competencies.views import school


class CompetencyViewTests(TestCase):
    """Needed tests:
    - queryset tests for all pages
    - no-data tests
    """

    def setUp(self):
        # Build a school, down to the performance indicator level.
        #  These should be a few loops, making a number of elements at each level.

        self.client = Client()

        # Create a test user.
        self.test_user = User.objects.create(username='testuser')
        self.test_user.set_password('pw')
        self.test_user.save()
        new_up = UserProfile()
        new_up.user = self.test_user
        new_up.save()

        # Create test school.
        self.test_school = School.objects.create(name="Test School")
        self.test_sa = SubjectArea.objects.create(subject_area="Science", school=self.test_school)
        self.test_sda = SubdisciplineArea.objects.create(subject_area=self.test_sa,
                                                         subdiscipline_area="Physical Science")

        # Give test user permissions to work with this school.
        self.test_user.userprofile.schools.add(self.test_school)



    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        self.assertEqual(response.status_code, 200)

    def test_schools_view(self):
        """Schools page lists all schools, links to detail view of that school."""
        response = self.client.get(reverse('competencies:schools'))
        self.assertEqual(response.status_code, 200)
        # Make sure list of schools appears in context, and that test_school
        #  is in that list.
        self.assertTrue('schools' in response.context)
        self.assertTrue(self.test_school in response.context['schools'])

    def test_school_view(self):
        """School page lists subject areas and subdiscipline areas for that school."""
        logged_in = self.client.login(username='testuser', password='pw')
        print('logged in: ', logged_in)
        
        response = self.client.get(reverse('competencies:school', args=(self.test_school.id,)))
        self.assertEqual(response.status_code, 200)

        # Make sure subject and sda appear in context.
        self.assertTrue('school' in response.context)
        self.assertTrue('subject_areas' in response.context)
        self.assertTrue('sa_sdas' in response.context)

        #return 'done'
        # Is this because I'm not logged in?
        # Yes! Create a user and log in?
        #  Test logged in, logged out version of page.
        print(response.context['user'])
        print(response.context['school'])
        print(response.context['subject_areas'])
        print(response.context['sa_sdas'])
        print(response.context['sa_sdas'].keys())
        print(response.context.keys())
        print(reverse('competencies:school', args=(self.test_school.id,)))
        
        return 'done'


        self.assertEqual(self.test_school, response.context['school'])
        self.assertTrue(self.test_sa in response.context['subject_areas'])
        #self.assertTrue(self.test_sda in response.context['sa_sdas'][self.test_sa])

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
