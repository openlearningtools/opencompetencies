from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from competencies.models import *
from competencies.views import school
from competencies import my_admin

"""DEV NOTES
  - Maybe instead of using indices to store schools, use separate lists:
    - test_schools_has_perm
    - test_schools_no_perm
    - test_schools_all_private
    - test_schools_all_public

    Any test that doesn't interact with db should inherit from
     unittest.TestCase, not django's TestCase:
     https://docs.djangoproject.com/en/1.8/topics/testing/overview/#writing-tests

    Not sure why I need __init__.py.
     Shouldn't test utility find any class under /tests that inherits from TestCase?
     Why do the tests in other modules like test_forms.py run?

"""

class CompetencyViewTests(TestCase):
    """Tests for all views in competencies."""
    # May want to use simpler password hashing in tests.
    #  https://docs.djangoproject.com/en/1.8/topics/testing/overview/#speeding-up-the-tests

    # setUp() should build a school, but then have separate methods to
    #  build the school out to subject area levels, sda, grad std, or perf indicator.
    # Then each test method can only call the level it needs. Testing efficiency
    #  should be greatly improved. Methdods such as build_to_sas(), build_to_eus().

    def setUp(self, num_elements=2):
        # Build a school, down to the performance indicator level.
        self.num_elements = num_elements
        self.client = Client()

        # Create 2 test users.
        self.test_user_0 = User.objects.create_user(username='testuser0', password='pw')
        new_up = UserProfile(user=self.test_user_0)
        new_up.save()

        self.test_user_1 = User.objects.create_user(username='testuser1', password='pw')
        new_up = UserProfile(user=self.test_user_1)
        new_up.save()

        # Build num_elements test schools that user 0 is associated with,
        #  num_elements the user 1 is associated with.
        self.test_schools, self.test_sas = [], []
        for school_num in range(6):
            name = "Test Organization %d" % school_num
            if school_num < num_elements:
                new_school = Organization.objects.create(name=name, owner=self.test_user_0)
                self.test_user_0.userprofile.organizations.add(new_school)
            else:
                new_school = Organization.objects.create(name=name, owner=self.test_user_1)
                self.test_user_1.userprofile.organizations.add(new_school)
            self.test_schools.append(new_school)

            # Create num_elements subject areas for each school.
            for sa_num in range(num_elements):
                sa_name = "Test SA %d-%d" % (school_num, sa_num)
                new_sa = SubjectArea.objects.create(subject_area=sa_name,
                                                    organization=new_school)
                self.test_sas.append(new_sa)

                # Create num_elements grad standards for each subject area.
                for gs_num in range(num_elements):
                    gs_body = "Test GS %d-%d-%d" % (school_num, sa_num, gs_num)
                    new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                               competency_area=gs_body)

                    # Create num_elements perf indicators for each grad std.
                    for pi_num in range(num_elements):
                        pi_body = "Test PI %d-%d-%d-%d" % (school_num, sa_num, gs_num, pi_num)
                        new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                     competency_area=new_gs)

                # Create num_elements sdas for each sa.
                for sda_num in range(num_elements):
                    sda_name = "Test SDA %d-%d-%d" % (school_num, sa_num, sda_num)
                    new_sda = SubdisciplineArea.objects.create(subject_area=new_sa,
                                                               subdiscipline_area=sda_name)

                    # Create num_elements grad standards for each sda.
                    for gs_num in range(num_elements):
                        gs_body = "Test GS %d-%d-%d-%d" % (school_num, sa_num, sda_num, gs_num)
                        new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                                   subdiscipline_area=new_sda,
                                                                   competency_area=gs_body)

                        # Create num_elements perf indicators for each grad std.
                        for pi_num in range(num_elements):
                            pi_body = "Test PI %d-%d-%d-%d-%d" % (school_num, sa_num, sda_num, gs_num, pi_num)
                            new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                         competency_area=new_gs)


    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        self.assertEqual(response.status_code, 200)

    def test_schools_view(self):
        """Schools page lists all schools, links to detail view of that school."""
        response = self.client.get(reverse('competencies:organizations'))
        self.assertEqual(response.status_code, 200)

        # Make sure list of schools appears in context, and that test_school
        #  is in that list.
        self.assertTrue('schools' in response.context)
        for school in self.test_schools:
            self.assertTrue(school in response.context['schools'])


    def test_school_view_logged_in(self):
        """School page lists subject areas and subdiscipline areas for that school."""
        self.client.login(username='testuser0', password='pw')

        for school_num, school in enumerate(self.test_schools):
            test_url = reverse('competencies:school', args=(school.id,))
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 200)

            # For now, all users can see the names of all schools.
            self.assertEqual(school, response.context['school'])

            if school_num < self.num_elements:
                # User should see sa and sdas for school they have permissions on.
                for sa in school.subjectarea_set.all():
                    self.assertTrue(sa in response.context['subject_areas'])
                    for sda in sa.subdisciplinearea_set.all():
                        self.assertTrue(sda in response.context['sa_sdas'][sa])
            else:
                # All elements are private by default, so user should not see sas
                #  or sdas for this school.
                for sa in school.subjectarea_set.all():
                    self.assertFalse(sa in response.context['subject_areas'])
                    self.assertFalse(sa in response.context['sa_sdas'].keys())

    def test_new_school(self):
        """New school allows uer to create a new school."""
        test_url = reverse('competencies:new_school')
        self.generic_test_blank_form(test_url)

        # Test user can create a new school, current user is owner,
        #  and user can modify school.
        response = self.client.post(test_url, {'name': 'my new school'})
        self.assertEqual(response.status_code, 302)
        school_names = [school.name for school in Organization.objects.all()]
        self.assertTrue('my new school' in school_names)

        for school in Organization.objects.all():
            if school.name == 'my new school':
                self.assertTrue(school.owner, self.test_user_0)
                self.assertTrue(school in self.test_user_0.userprofile.organizations.all())

        # Test that user can't create a second school of the same name.
        # DEV: DB error causes test to fail. How test this properly?
        #  Start by creating server error page.
        # response = self.client.post(test_url, {'name': 'my new school'})
        # self.assertEqual(response.status_code, 500)

        # But another user can create a school of that same name.
        self.client.login(username='testuser1', password='pw')
        response = self.client.post(test_url, {'name': 'my new school'})
        self.assertEqual(response.status_code, 302)
        school_names = [school.name for school in Organization.objects.all()]
        # DEV: Verify name 'my new school' appears twice in list.
        self.assertTrue('my new school' in school_names)

        owner_correct = False
        for school in Organization.objects.all():
            if school.name == 'my new school' and school.owner == self.test_user_1:
                owner_correct = True
        self.assertTrue(owner_correct)



    def test_new_sa_view(self):
        """Lets user create a new subject area."""
        test_url = reverse('competencies:new_sa', args=(self.test_schools[0].id,))
        self.generic_test_blank_form(test_url)
        
        # Test user can create a new subject area, and it's stored in db.
        response = self.client.post(test_url, {'subject_area': 'english', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sa_names = [sa.subject_area for sa in self.test_schools[0].subjectarea_set.all()]
        self.assertTrue('english' in sa_names)
        
    def test_new_sda_view(self):
        """Lets user create a new subdiscipline area."""
        test_url = reverse('competencies:new_sda', args=(self.test_sas[0].id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new subdiscipline area, and it's stored in db.
        response = self.client.post(test_url, {'subdiscipline_area': 'life science', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sda_names = [sda.subdiscipline_area for sda in self.test_sas[0].subdisciplinearea_set.all()]
        self.assertTrue('life science' in sda_names)

    def test_new_ca_view(self):
        """Lets user create a new competency area for a general subject area."""
        test_url = reverse('competencies:new_ca', args=(self.test_sas[0].id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new ca, and it's stored in db.
        data = {'competency_area': 'knows science',
                'student_friendly': '', 'description': '', 'phrase': '',
                }
        response = self.client.post(test_url, data)
        self.assertEqual(response.status_code, 302)
        ca_titles = [ca.competency_area for ca in self.test_sas[0].competencyarea_set.all()]
        self.assertTrue('knows science' in ca_titles)

    def test_new_sda_ca_view(self):
        """Lets user create a new competency area for a subdiscipline area."""
        test_sdas = [sda for sda in self.test_sas[0].subdisciplinearea_set.all()]
        test_url = reverse('competencies:new_sda_ca', args=(test_sdas[0].id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new ca for the sda, and it's stored in db.
        data = {'competency_area': 'knows Newtons Laws',
                'student_friendly': '', 'description': '', 'phrase': '',
                }
        response = self.client.post(test_url, data)
        self.assertEqual(response.status_code, 302)
        ca_titles = [ca.competency_area for ca in test_sdas[0].competencyarea_set.all()]
        self.assertTrue('knows Newtons Laws' in ca_titles)

    def test_new_eu_view(self):
        """Lets user create a new essential understanding for a ca."""
        test_gstds = CompetencyArea.objects.all()
        test_url = reverse('competencies:new_eu', args=(test_gstds[0].id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new eu for the gs, and it's stored in db.
        data = {'essential_understanding': 'can state first law',
                'student_friendly': '', 'description': '',
                }
        response = self.client.post(test_url, data)
        self.assertEqual(response.status_code, 302)
        eu_bodies = [eu.essential_understanding for eu in test_gstds[0].essentialunderstanding_set.all()]
        self.assertTrue('can state first law' in eu_bodies)

    def test_sa_summary_view(self):
        sa = self.test_schools[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:sa_summary', args=(sa.id,))
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

        # Check that grad stds for sa are in context.
        self.assertTrue('grad_std_eus' in response.context)
        grad_std_eus = response.context['grad_std_eus']
        grad_stds = sa.competencyarea_set.filter(subdiscipline_area=None)
        # print(grad_std_eus)
        # print(grad_stds)
        for grad_std in grad_stds:
            # print('ok', grad_std, grad_std_eus.keys())
            self.assertTrue(grad_std in grad_std_eus.keys())
            # Check that pis for each grad std are in context.
            pis = grad_std.essentialunderstanding_set.all()
            # print(pis)
            for pi in pis:
                self.assertTrue(pi in grad_std_eus[grad_std])
                # Check that pi is on the rendered page.
                self.assertTrue(pi.essential_understanding in response.content.decode())


        # Check that grad stds for sda are in context.
        sda = sa.subdisciplinearea_set.all()[0]
        # print(sda, '\n')
        self.assertTrue('sda_grad_stds' in response.context)

        sda_grad_stds = response.context['sda_grad_stds']
        sda_grad_std_eus = response.context['sda_grad_std_eus']
        # print('here', sda_grad_std_eus, '\n')
        # print(sda_grad_stds, '\n')
        # print(sda_grad_stds.keys(), '\n')
        
        grad_stds = sda.competencyarea_set.all()
        # print(grad_stds, '\n')

        for grad_std in grad_stds:
            # print(grad_std, sda_grad_stds.keys(), '\n\n')
            self.assertTrue(grad_std in sda_grad_stds[sda])
            # Check that pis for each grad std are in context.
            pis = grad_std.essentialunderstanding_set.all()
            for pi in pis:
                self.assertTrue(pi in sda_grad_std_eus[grad_std])
                # print('--- context ---\n', response.content.decode())
                # Check that pi is on rendered page.
                self.assertTrue(pi.essential_understanding in response.content.decode())

    def test_edit_sa_summary_view(self):
        """Lets user edit a subject area and its sdas, gstds, and pis."""
        # Bug that page does not display gstds for sdas.
        pass

    def test_register_view(self):
        """Lets new user register an account."""
        test_url = reverse('register')
        self.generic_test_blank_form(test_url)

        # Test new user can be created, and userprofile connected properly.
        response = self.client.post(test_url, {'username': 'ozzy', 'email': '',
                                               'password1': 'pw', 'password2': 'pw',
                                               })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.filter(username='ozzy')[0]
        self.assertTrue(hasattr(new_user, 'userprofile'))


    def generic_test_blank_form(self, test_url):
        """A helper method to test that a form-based page returns a blank form properly."""
        # Test that a logged in user can get a blank form properly.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
