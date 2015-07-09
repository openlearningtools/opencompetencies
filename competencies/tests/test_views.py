from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from competencies.models import *
from competencies.views import organization
from competencies import my_admin

"""DEV NOTES
  - Maybe instead of using indices to store organizations, use separate lists:
    - test_organizations_has_perm
    - test_organizations_no_perm
    - test_organizations_all_private
    - test_organizations_all_public

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

    # setUp() should build an organization, but then have separate methods to
    #  build the organization out to subject area levels, sda, grad std, or perf indicator.
    # Then each test method can only call the level it needs. Testing efficiency
    #  should be greatly improved. Methdods such as build_to_sas(), build_to_eus().

    def setUp(self, num_elements=2):
        # Build an organization, down to the performance indicator level.
        self.num_elements = num_elements
        self.client = Client()

        # Create 2 test users.
        self.test_user_0 = User.objects.create_user(username='testuser0', password='pw')
        new_up = UserProfile(user=self.test_user_0)
        new_up.save()

        self.test_user_1 = User.objects.create_user(username='testuser1', password='pw')
        new_up = UserProfile(user=self.test_user_1)
        new_up.save()

        # Build num_elements test organizations that user 0 is associated with,
        #  num_elements the user 1 is associated with.
        self.test_organizations, self.test_sas = [], []
        for organization_num in range(6):
            name = "Test Organization %d" % organization_num
            if organization_num < num_elements:
                new_organization = Organization.objects.create(name=name, owner=self.test_user_0)
                self.test_user_0.userprofile.organizations.add(new_organization)
            else:
                new_organization = Organization.objects.create(name=name, owner=self.test_user_1)
                self.test_user_1.userprofile.organizations.add(new_organization)
            self.test_organizations.append(new_organization)

            # Create num_elements subject areas for each organization.
            for sa_num in range(num_elements):
                sa_name = "Test SA %d-%d" % (organization_num, sa_num)
                new_sa = SubjectArea.objects.create(subject_area=sa_name,
                                                    organization=new_organization)
                self.test_sas.append(new_sa)

                # Create num_elements grad standards for each subject area.
                for gs_num in range(num_elements):
                    gs_body = "Test GS %d-%d-%d" % (organization_num, sa_num, gs_num)
                    new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                               competency_area=gs_body)

                    # Create num_elements perf indicators for each grad std.
                    for pi_num in range(num_elements):
                        pi_body = "Test PI %d-%d-%d-%d" % (organization_num, sa_num, gs_num, pi_num)
                        new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                     competency_area=new_gs)

                # Create num_elements sdas for each sa.
                for sda_num in range(num_elements):
                    sda_name = "Test SDA %d-%d-%d" % (organization_num, sa_num, sda_num)
                    new_sda = SubdisciplineArea.objects.create(subject_area=new_sa,
                                                               subdiscipline_area=sda_name)

                    # Create num_elements grad standards for each sda.
                    for gs_num in range(num_elements):
                        gs_body = "Test GS %d-%d-%d-%d" % (organization_num, sa_num, sda_num, gs_num)
                        new_gs = CompetencyArea.objects.create(subject_area=new_sa,
                                                                   subdiscipline_area=new_sda,
                                                                   competency_area=gs_body)

                        # Create num_elements perf indicators for each grad std.
                        for pi_num in range(num_elements):
                            pi_body = "Test PI %d-%d-%d-%d-%d" % (organization_num, sa_num, sda_num, gs_num, pi_num)
                            new_pi = EssentialUnderstanding.objects.create(essential_understanding=pi_body,
                                                                         competency_area=new_gs)


    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        self.assertEqual(response.status_code, 200)

    def test_organizations_view(self):
        """Organizations page lists all organizations, links to detail view of that organization."""
        response = self.client.get(reverse('competencies:organizations'))
        self.assertEqual(response.status_code, 200)

        # Make sure list of organizations appears in context, and that test_organization
        #  is in that list.
        self.assertTrue('organizations' in response.context)
        for organization in self.test_organizations:
            self.assertTrue(organization in response.context['organizations'])


    def test_organization_view_logged_in(self):
        """Organization page lists subject areas and subdiscipline areas for that organization."""
        self.client.login(username='testuser0', password='pw')

        for organization_num, organization in enumerate(self.test_organizations):
            test_url = reverse('competencies:organization', args=(organization.id,))
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 200)

            # For now, all users can see the names of all organizations.
            self.assertEqual(organization, response.context['organization'])

            if organization_num < self.num_elements:
                # User should see sa and sdas for organization they have permissions on.
                for sa in organization.subjectarea_set.all():
                    self.assertTrue(sa in response.context['subject_areas'])
                    for sda in sa.subdisciplinearea_set.all():
                        self.assertTrue(sda in response.context['sa_sdas'][sa])
            else:
                # All elements are private by default, so user should not see sas
                #  or sdas for this organization.
                for sa in organization.subjectarea_set.all():
                    self.assertFalse(sa in response.context['subject_areas'])
                    self.assertFalse(sa in response.context['sa_sdas'].keys())

    def test_new_organization_view(self):
        """New organization allows uer to create a new organization."""
        test_url = reverse('competencies:new_organization')
        self.generic_test_blank_form(test_url)

        # Test user can create a new organization, current user is owner,
        #  and user can modify organization.
        response = self.client.post(test_url, {'name': 'my new organization',
                                               'org_type': 'school',})
        self.assertEqual(response.status_code, 302)
        organization_names = [organization.name for organization in Organization.objects.all()]
        self.assertTrue('my new organization' in organization_names)

        for organization in Organization.objects.all():
            if organization.name == 'my new organization':
                self.assertTrue(organization.owner, self.test_user_0)
                self.assertTrue(organization in self.test_user_0.userprofile.organizations.all())

        # Test that user can't create a second organization of the same name.
        # DEV: DB error causes test to fail. How test this properly?
        #  Start by creating server error page.
        # response = self.client.post(test_url, {'name': 'my new organization'})
        # Something like:
        #   fn = self.client.post(...)
        #   self.assertRaises(DBError, fn)
        # self.assertEqual(response.status_code, 500)

        # But another user can create an organization of that same name.
        self.client.login(username='testuser1', password='pw')
        response = self.client.post(test_url, {'name': 'my new organization',
                                               'org_type': 'school',})
        self.assertEqual(response.status_code, 302)
        organization_names = [organization.name for organization in Organization.objects.all()]
        # DEV: Verify name 'my new organization' appears twice in list.
        self.assertTrue('my new organization' in organization_names)

        owner_correct = False
        for organization in Organization.objects.all():
            if organization.name == 'my new organization' and organization.owner == self.test_user_1:
                owner_correct = True
        self.assertTrue(owner_correct)



    def test_new_sa_view(self):
        """Lets user create a new subject area."""
        test_url = reverse('competencies:new_sa', args=(self.test_organizations[0].id,))
        self.generic_test_blank_form(test_url)
        
        # Test user can create a new subject area, and it's stored in db.
        response = self.client.post(test_url, {'subject_area': 'english', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sa_names = [sa.subject_area for sa in self.test_organizations[0].subjectarea_set.all()]
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
        sa = self.test_organizations[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:sa_summary', args=(sa.id,))
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

        # Check that cas for sa are in context.
        self.assertTrue('ca_eus' in response.context)
        ca_eus = response.context['ca_eus']
        cas = sa.competencyarea_set.filter(subdiscipline_area=None)
        # print(ca_eus)
        # print(cas)
        for ca in cas:
            # print('ok', ca, ca_eus.keys())
            self.assertTrue(ca in ca_eus.keys())
            # Check that eus for each ca are in context.
            eus = ca.essentialunderstanding_set.all()
            # print(eus)
            for eu in eus:
                self.assertTrue(eu in ca_eus[ca])
                # Check that eu is on the rendered page.
                self.assertTrue(eu.essential_understanding in response.content.decode())


        # Check that cas for sda are in context.
        sda = sa.subdisciplinearea_set.all()[0]
        # print(sda, '\n')
        self.assertTrue('sda_cas' in response.context)

        sda_cas = response.context['sda_cas']
        sda_ca_eus = response.context['sda_ca_eus']
        # print('here', sda_ca_eus, '\n')
        # print(sda_cas, '\n')
        # print(sda_cas.keys(), '\n')
        
        cas = sda.competencyarea_set.all()
        # print(cas, '\n')

        for ca in cas:
            # print(ca, sda_cas.keys(), '\n\n')
            self.assertTrue(ca in sda_cas[sda])
            # Check that eus for each ca are in context.
            eus = ca.essentialunderstanding_set.all()
            for eu in eus:
                self.assertTrue(eu in sda_ca_eus[ca])
                # print('--- context ---\n', response.content.decode())
                # Check that eu is on rendered page.
                self.assertTrue(eu.essential_understanding in response.content.decode())

    def test_edit_sa_summary_view(self):
        """Lets user edit a subject area and its sdas, gstds, and pis."""

        # Test submitting blank form.
        sa = self.test_organizations[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:edit_sa_summary', args=(sa.id,))
        self.generic_test_blank_form(test_url)

        # Test submitting data modifies elements.
        post_data = {'subject_area': 'modifed subject area'}
        response = self.client.post(test_url, post_data)
        #self.assertEqual(response.status_code, 302)
        self.assertEqual(sa.subject_area, 'modified subject area')


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
