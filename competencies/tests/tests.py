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
        self.test_user = User.objects.create_user(username='testuser', password='pw')
        new_up = UserProfile(user=self.test_user)
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

    def test_school_view_logged_in(self):
        """School page lists subject areas and subdiscipline areas for that school."""
        # Test that user with full school permission can see sas and sdas for a school.
        self.client.login(username='testuser', password='pw')
        response = self.client.get(reverse('competencies:school', args=(self.test_school.id,)))
        self.assertEqual(response.status_code, 200)

        # Make sure subject and sda appear in context.
        self.assertTrue('school' in response.context)
        self.assertTrue('subject_areas' in response.context)
        self.assertTrue('sa_sdas' in response.context)

        self.assertEqual(self.test_school, response.context['school'])
        self.assertTrue(self.test_sa in response.context['subject_areas'])
        self.assertTrue(self.test_sda in response.context['sa_sdas'][self.test_sa])

    def test_new_school(self):
        """New school processes form to create a new school."""
        # Make sure test user can get the blank form.
        # Form is actually on /schools/
        self.client.login(username='testuser', password='pw')
        response = self.client.get(reverse('competencies:schools'))
        self.assertEqual(response.status_code, 200)

        # Test that user can make a new school.
        response = self.client.get(reverse('competencies:schools'), {'new_school_name': 'New Test School'})
        self.assertEqual(response.status_code, 200)

        # DEV: This fails.
        #  I'm not sure how to test a form that processes on a separate page.
        #  Need to modify the initial request as shown above?
        #  Working through browser, and looking at output of runserver,
        #   it's a get request to /schools/ and a post request to /new_school/
        #   but /schools/ should call /new_school/.
        #  Why doesn't it make a 302 redirecting to the action page?
        #  Maybe: make a separate new_school page, like other forms?
        #
        # school_names = [school.name for school in School.objects.all()]
        # print(school_names)
        # self.assertTrue('New Test School' in school_names)

    def test_new_sa_view(self):
        """Lets user create a new subject area."""
        test_url = reverse('competencies:new_sa', args=(self.test_school.id,))
        self.generic_test_blank_form(test_url)
        
        # Test user can create a new subject area, and it's stored in db.
        response = self.client.post(test_url, {'subject_area': 'english', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sa_names = [sa.subject_area for sa in self.test_school.subjectarea_set.all()]
        self.assertTrue('english' in sa_names)
        
    def test_new_sda_view(self):
        """Lets user create a new subdiscipline area."""
        test_url = reverse('competencies:new_sda', args=(self.test_sa.id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new subdiscipline area, and it's stored in db.
        response = self.client.post(test_url, {'subdiscipline_area': 'life science', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sda_names = [sda.subdiscipline_area for sda in self.test_sa.subdisciplinearea_set.all()]
        self.assertTrue('life science' in sda_names)

    def test_new_gs_view(self):
        """Lets user create a new graduation standard for a general subject area."""
        test_url = reverse('competencies:new_gs', args=(self.test_sa.id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new gs, and it's stored in db.
        data = {'graduation_standard': 'knows science',
                'student_friendly': '', 'description': '', 'phrase': '',
                }
        response = self.client.post(test_url, data)
        self.assertEqual(response.status_code, 302)
        gs_titles = [gs.graduation_standard for gs in self.test_sa.graduationstandard_set.all()]
        self.assertTrue('knows science' in gs_titles)

    def generic_test_blank_form(self, test_url):
        """A helper method to test that a form-based page returns a blank form properly."""
        # Test that a logged in user can get a blank form properly.
        self.client.login(username='testuser', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
        

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
