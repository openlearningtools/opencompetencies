from random import choice

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from competencies.models import *
from competencies.views import organization
from competencies import my_admin, utils
from users.models import UserProfile

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
        self.test_sas, self.test_sdas = [], []
        self.test_cas, self.test_eus = [], []

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

    def build_to_sas(self):
        """Build out system to the subject area level."""
        self.build_to_organizations()

        # Create num_elements subject areas for each organization.
        for organization_num, organization in enumerate(self.test_organizations):

            for sa_num in range(self.num_elements):
                sa_name = "Test SA %d-%d %d" % (organization_num, sa_num, self.element_number)
                new_sa = SubjectArea.objects.create(subject_area=sa_name,
                                                    organization=organization)
                self.test_sas.append(new_sa)
                self.element_number += 1

    def build_to_sdas(self):
        """Build out system to the subdiscipline_area level."""
        self.build_to_sas()
        for sa in self.test_sas:
            # Create num_elements sdas for each sa.
            for sda_num in range(self.num_elements):
                sda_name = "Test SDA %d %d" % (sda_num, self.element_number)
                new_sda = SubdisciplineArea.objects.create(subject_area=sa,
                                                           subdiscipline_area=sda_name)
                self.test_sdas.append(new_sda)
                self.element_number += 1

    def build_to_cas(self):
        """Build out system to the competency_area level."""
        # Be sure to include general sa cas, and sda cas.
        self.build_to_sdas()

        for sa in self.test_sas:
            # Create num_elements competency areas for each subject area.
            for ca_num in range(self.num_elements):
                ca_body = "Test CA %d %d" % (ca_num, self.element_number)
                new_ca = CompetencyArea.objects.create(subject_area=sa,
                                                           competency_area=ca_body)
                self.test_cas.append(new_ca)
                self.element_number += 1

        for sda in self.test_sdas:
            # Create num_elements competency areas for each sda.
            for ca_num in range(self.num_elements):
                ca_body = "Test CA %d %d" % (ca_num, self.element_number)
                new_ca = CompetencyArea.objects.create(subject_area=sda.subject_area,
                                                           subdiscipline_area=sda,
                                                           competency_area=ca_body)
                self.test_cas.append(new_ca)
                self.element_number += 1

    def build_to_eus(self):
        """Build out a system to the essential understanding level."""
        self.build_to_cas()
        
        for ca in self.test_cas:
            # Create num_elements eus for each grad std.
            for eu_num in range(self.num_elements):
                eu_body = "Test EU %d %d" % (eu_num, self.element_number)
                new_eu = EssentialUnderstanding.objects.create(essential_understanding=eu_body,
                                                             competency_area=ca)
                self.test_eus.append(new_eu)
                self.element_number += 1


    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        self.assertEqual(response.status_code, 200)

    def test_organizations_view(self):
        """Organizations page lists all orgs user owns, can edit, and public organizations;
           links to detail view of that organization."""
        self.build_to_organizations()

        test_url = reverse('competencies:organizations')

        # Test for anonymous users, my_orgs and editor_orgs are empty.
        #  Also test that private orgs not in public_orgs.
        self.client.logout()
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['my_organizations']), 0)
        self.assertEqual(len(response.context['editor_organizations']), 0)
        for org in self.test_organizations:
            if org.public:
                self.assertTrue(org in response.context['public_organizations'])
            else:
                self.assertFalse(org in response.context['public_organizations'])

        # Test for logged in users.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
        for org in self.test_organizations:
            # Make sure owned org is in my_orgs
            # Make sure owned org is not in editor_orgs
            # Make sure not owned org is not in my_orgs
            if org.owner == self.test_user_0:
                self.assertTrue(org in response.context['my_organizations'])
                self.assertFalse(org in response.context['editor_organizations'])
            else:
                self.assertFalse(org in response.context['my_organizations'])

            # Make sure can edit org is in editor_orgs
            # Make sure non edit org is not in editor_orgs
            if (self.test_user_0 in org.editors.all()
                and org.owner != self.test_user_0):
                self.assertTrue(org in response.context['editor_organizations'])
            else:
                self.assertFalse(org in response.context['editor_organizations'])

            # Make sure private org is not in public orgs
            if org.public:
                self.assertTrue(org in response.context['public_organizations'])
            else:
                self.assertFalse(org in response.context['public_organizations'])


    def test_organization_view_logged_in(self):
        """Organization page lists subject areas and subdiscipline areas for that organization."""
        self.build_to_sas()
        
        self.client.login(username='testuser0', password='pw')

        for organization_num, organization in enumerate(self.test_organizations):
            test_url = reverse('competencies:organization', args=(organization.id,))
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 200)

            # For now, all users can see the names of all organizations.
            self.assertEqual(organization, response.context['organization'])

            if organization_num < self.num_orgs/2:
                # User should see sa and sdas for organization they have permissions on.
                for sa in organization.subjectarea_set.all():
                    self.assertTrue(sa in response.context['subject_areas'])
                    for sda in sa.subdisciplinearea_set.all():
                        self.assertTrue(sda in response.context['sdas'])
            else:
                # All elements are private by default, so user should not see sas
                #  or sdas for this organization.
                for sa in organization.subjectarea_set.all():
                    self.assertFalse(sa in response.context['subject_areas'])
                    for sda in sa.subdisciplinearea_set.all():
                        self.assertFalse(sda in response.context['sdas'])

    def test_organization_admin_summary_view(self):
        """Displays a summary of org to owner."""

        # Use test_user_1's org as test org.
        self.build_to_organizations()
        for org in self.test_organizations:
            if org.owner == self.test_user_1:
                organization = org
                org_id = org.id
                break
        self.assertTrue(organization)

        # --- Critical security tests ---
        # -- Test that an anonymous user is redirected.
        self.client.logout()
        test_url = reverse('competencies:organization_admin_summary', args=(organization.id,))
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)

        # -- Test that a non-owner is redirected.
        logged_in = self.client.login(username='testuser0', password='pw')
        self.assertTrue(logged_in)
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        
        # -- Test that a owner can see page.
        logged_in = self.client.login(username='testuser1', password='pw')
        self.assertTrue(logged_in)
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

    def test_organization_admin_edit_view(self):
        """Organization_admin_edit allows org owner to administer organization."""
        # DEV: Incomplete
        
        # Use test_user_1's org as test org.
        self.build_to_eus()
        for org in self.test_organizations:
            if org.owner == self.test_user_1:
                organization = org
                org_id = org.id
                break
        self.assertTrue(organization)
        # --- Critical security tests ---
        # -- Test that an anonymous user is redirected.
        self.client.logout()
        test_url = reverse('competencies:organization_admin_edit', args=(organization.id,))
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)

        # -- Test that a non-owner is redirected.
        logged_in = self.client.login(username='testuser0', password='pw')
        self.assertTrue(logged_in)
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)

        # -- Test changing a school from public to private works.
        self.client.login(username='testuser1', password='pw')
        # Set organization public.
        organization.public = True
        organization.save()
        modified_org = Organization.objects.get(id=org_id)
        self.assertTrue(modified_org.public)

        # Set all elements in the school public.
        utils.cascade_visibility_down(modified_org, 'public')

        # Submit post request changing public to private.
        post_data = self.get_org_admin_post_data(organization)
        post_data['public'] = False
        response = self.client.post(test_url, post_data)
        self.assertEqual(response.status_code, 302)
        modified_org = Organization.objects.get(id=org_id)
        self.assertFalse(modified_org.public)

        # Test that making org private cascades down through all elements.
        modified_sas = modified_org.subjectarea_set.all()
        for sa in modified_sas:
            self.assertFalse(sa.public)
            for sda in sa.subdisciplinearea_set.all():
                self.assertFalse(sda.public)
            for ca in sa.competencyarea_set.all():
                self.assertFalse(ca.public)
                for eu in ca.essentialunderstanding_set.all():
                    self.assertFalse(eu.public)

        # Test an org owner can not remove self from editors.
        #   Send a request with owner not selected, verify still in editors.
        post_data = self.get_org_admin_post_data(organization)
        # Since editors is required field, something needs to be selected.
        post_data['editors'] = [str(self.test_user_0.id)]
        response = self.client.post(test_url, post_data)
        # Verify two editors - owner, and non-owner selected.
        self.assertTrue(self.test_user_1 in organization.editors.all())
        self.assertTrue(self.test_user_0 in organization.editors.all())

        # Test an org owner can remove another editor.
        #   Do this by selecting only the owner.
        post_data['editors'] = [str(organization.owner.id)]
        response = self.client.post(test_url, post_data)
        # Verify owner is the only editor.
        editors = organization.editors.all()
        self.assertTrue(self.test_user_1 in editors)
        self.assertEqual(len(editors), 1)

        # --- Non-security tests ---
        # Test that form works for name, type, aliases, etc.

        # -- Test that form works for changing org type.
        self.assertEqual(organization.org_type, 'school')
        self.client.login(username='testuser1', password='pw')

        post_data = self.get_org_admin_post_data(organization)
        post_data['org_type'] = 'nonprofit'
        response = self.client.post(test_url, post_data)

        self.assertEqual(response.status_code, 302)
        modified_org = Organization.objects.get(id=org_id)
        self.assertEqual(modified_org.org_type, 'nonprofit')

    def get_org_admin_post_data(self, organization):
        """Get default initial post data for org."""
        post_data = {'name': organization.name,
                     'org_type': organization.org_type,
                     'public': organization.public,
                     'alias_sa': organization.alias_sa,
                     'alias_sda': organization.alias_sda,
                     'alias_ca': organization.alias_ca,
                     'alias_eu': organization.alias_eu,
                     'alias_lt': organization.alias_lt,
                     'editors': [str(organization.owner.id)]
                     }
        return post_data

    def test_fork_view(self):
        """Fork allows a new, empty org to copy all elements from an existing public org."""
        # This test takes longer than most, because it makes a larger dataset
        #   with randomized privacy values.

        # DEV: Test that a non-empty org remains unchanged.
        # DEV: Test that only public organizations can be forked.
        #   Can't even do this right now; it returns 200, because private orgs are not in form.
        #   Submitting a private org's id results in a form error.
        # Fork an org, and...
        # Test all elements in new org match public elements of original org.
        # DEV: Test there's nothing in new org that's not in original.
        # Test there's no private elements in new org.
        # DEV: Test adding a new sa to original org only affects original org.
        # DEV: Test adding a new sa to forking org only affects forking org.
        # Test that forking user is only editor of new org.

        # For a more rigorous test, set this to a higher number like 5 or 8.
        self.num_elements = 3
        self.build_to_eus()

        # --- Testuser0 will fork testuser1's org.
        # Testuser0 needs to create a new school.
        self.client.login(username='testuser0', password='pw')
        post_data = {'name': 'test fork school', 'org_type': 'school'}
        new_org_url = reverse('competencies:new_organization')
        response = self.client.post(new_org_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('test fork school' in [org.name for org in Organization.objects.filter(owner=self.test_user_0)])
        forking_org = Organization.objects.filter(name='test fork school')[0]

        # Get original org, set it public, and randomly set some of its elements public.
        #   (an element can only be public if its parent is public)
        original_org = Organization.objects.filter(owner=self.test_user_1)[0]
        original_org_pk = original_org.pk
        original_org.public = True
        original_org.save()

        for sa in original_org.subjectarea_set.all():
            sa.public = choice([True, False])
            sa.save()
            
            for sda in sa.subdisciplinearea_set.all():
                if sa.public:
                    sda.public = choice([True, False])
                    sda.save()

                for ca in sda.competencyarea_set.all():
                    if sda.public:
                        ca.public = choice([True, False])
                        ca.save()

                    for eu in ca.essentialunderstanding_set.all():
                        if ca.public:
                            eu.public = choice([True, False])
                            eu.save()

            for ca in sa.competencyarea_set.filter(subdiscipline_area=None):
                if sa.public:
                    ca.public = choice([True, False])
                    ca.save()

                for eu in ca.essentialunderstanding_set.all():
                    if ca.public:
                        eu.public = choice([True, False])
                        eu.save()

        # Set post data for fork.
        post_data = {'organization': original_org.pk}
        test_url = reverse('competencies:fork', args=[forking_org.id])
        response = self.client.post(test_url, post_data)
        self.assertEqual(response.status_code, 302)

        # Verify that elements match appropriately.
        #   These tests depend on every element having a unique name.
        forked_sas = forking_org.subjectarea_set.all()
        forked_sdas, forked_cas, forked_eus = [], [], []
        for sa in forked_sas:
            for sda in sa.subdisciplinearea_set.all():
                forked_sdas.append(sda)
                for ca in sda.competencyarea_set.all():
                    forked_cas.append(ca)
                    for eu in ca.essentialunderstanding_set.all():
                        forked_eus.append(eu)
            for ca in sa.competencyarea_set.filter(subdiscipline_area=None):
                forked_cas.append(ca)
                for eu in ca.essentialunderstanding_set.all():
                    forked_eus.append(eu)
                    
        forked_sas = [sa.subject_area for sa in forked_sas]
        forked_sdas = [sda.subdiscipline_area for sda in forked_sdas]
        forked_cas = [ca.competency_area for ca in forked_cas]
        forked_eus = [eu.essential_understanding for eu in forked_eus]
        for l in [forked_sas, forked_sdas, forked_cas, forked_eus]:
            print(len(l))

        for sa in original_org.subjectarea_set.all():
            if sa.public:
                self.assertTrue(sa.subject_area in forked_sas)
            else:
                self.assertFalse(sa.subject_area in forked_sas)

            for sda in sa.subdisciplinearea_set.all():
                if sda.public:
                    self.assertTrue(sda.subdiscipline_area in forked_sdas)
                else:
                    self.assertFalse(sda.subdiscipline_area in forked_sdas)

                for ca in sda.competencyarea_set.all():
                    if ca.public:
                        self.assertTrue(ca.competency_area in forked_cas)
                    else:
                        self.assertFalse(ca.competency_area in forked_cas)

                    for eu in ca.essentialunderstanding_set.all():
                        if eu.public:
                            self.assertTrue(eu.essential_understanding in forked_eus)
                        else:
                            self.assertFalse(eu.essential_understanding in forked_eus)

            for ca in sa.competencyarea_set.filter(subdiscipline_area=None):
                if ca.public:
                    self.assertTrue(ca.competency_area in forked_cas)
                else:
                    self.assertFalse(ca.competency_area in forked_cas)

                for eu in ca.essentialunderstanding_set.all():
                    if eu.public:
                        self.assertTrue(eu.essential_understanding in forked_eus)
                    else:
                        self.assertFalse(eu.essential_understanding in forked_eus)

        self.assertEqual(len(forking_org.editors.all()), 1)


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
                self.assertTrue(self.test_user_0 in organization.editors.all())

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
        self.num_orgs = 1
        self.build_to_organizations()
        
        test_url = reverse('competencies:new_sa', args=(self.test_organizations[0].id,))
        self.generic_test_blank_form(test_url)
        
        # Test user can create a new subject area, and it's stored in db.
        response = self.client.post(test_url, {'subject_area': 'english', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sa_names = [sa.subject_area for sa in self.test_organizations[0].subjectarea_set.all()]
        self.assertTrue('english' in sa_names)
        
    def test_new_sda_view(self):
        """Lets user create a new subdiscipline area."""
        self.num_orgs = 1
        self.build_to_sas()

        # Get a test_sa that's connected to the user that generic_test_blank_form will use.
        sa = self.test_organizations[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:new_sda', args=(sa.id,))
        self.generic_test_blank_form(test_url)

        # Test user can create a new subdiscipline area, and it's stored in db.
        response = self.client.post(test_url, {'subdiscipline_area': 'life science', 'description': ''})
        self.assertEqual(response.status_code, 302)
        sda_names = [sda.subdiscipline_area for sda in self.test_sas[0].subdisciplinearea_set.all()]
        self.assertTrue('life science' in sda_names)

    def test_new_ca_view(self):
        """Lets user create a new competency area for a general subject area."""
        self.num_orgs = 1
        self.build_to_sas()

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
        self.num_orgs = 1
        self.build_to_sdas()

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
        self.num_orgs = 1
        self.build_to_eus()

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
        self.num_orgs = 1
        self.build_to_eus()

        sa = self.test_organizations[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:sa_summary', args=(sa.id,))
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

        # Test that appropriate sa, sdas, cas, and eus are in context.
        #  Also test that these elements are in the final rendered content.
        content_str = response.content.decode()
        self.assertEqual(sa, response.context['subject_area'])
        self.assertTrue(sa.subject_area in content_str)

        sdas = sa.subdisciplinearea_set.all()
        for sda in sdas:
            self.assertTrue(sda in response.context['sdas'])
            self.assertTrue(sda.subdiscipline_area in content_str)

        cas = sa.competencyarea_set.all()
        for ca in cas:
            self.assertTrue(ca in response.context['cas'])
            self.assertTrue(ca.competency_area in content_str)

        eus = ca.essentialunderstanding_set.all()
        for eu in eus:
            self.assertTrue(eu in response.context['eus'])
            self.assertTrue(eu.essential_understanding in content_str)



    def test_edit_sa_summary_view(self):
        """Lets user edit a subject area and its sdas, gstds, and pis."""

        # DEV - possible improvements
        #   Test that unmodified elements are unchanged after submission.
        #   Test modifying multiple instances of sdas, cas, and eus.

        self.num_orgs = 1
        self.build_to_eus()

        # Test submitting blank form.
        sa = self.test_organizations[0].subjectarea_set.all()[0]
        test_url = reverse('competencies:edit_sa_summary', args=(sa.id,))
        self.generic_test_blank_form(test_url)

        # Test submitting data modifies elements.
        # DEV: All of these could probably be generalized and refactored.
        # DEV: Each of these generates many form errors. I'm only submitting post data
        #   relevant to the form being tested. The browser submits unchanged required
        #   data for each form. So if I print form errors, I get many invalid forms.
        #   But the tests pass because the individual form being tested works.
        #   Perhaps this could be addressed by testing all of the forms in one
        #   post request?

        # --- Test modifying subject area. ---

        sa_pk = sa.pk
        post_data = {'subject_area': 'modified subject area',}
        response = self.client.post(test_url, post_data)

        self.assertEqual(response.status_code, 302)
        sa = SubjectArea.objects.get(pk=sa_pk)
        self.assertEqual(sa.subject_area, 'modified subject area')

        # --- Test modifying a subdiscipline area. ---
        sda = sa.subdisciplinearea_set.all()[0]
        sda_pk = sda.pk
        sda_form_element_name = 'sda_form_%d-subdiscipline_area' % sda.id
        post_data = {sda_form_element_name: 'modified sda',}
        response = self.client.post(test_url, post_data)

        self.assertEqual(response.status_code, 302)
        sda = SubdisciplineArea.objects.get(pk=sda_pk)
        self.assertEqual(sda.subdiscipline_area, 'modified sda')

        # --- Test modifying a competency area. ---
        ca = sa.competencyarea_set.all()[0]
        ca_pk = ca.pk
        ca_form_element_name = 'ca_form_%d-competency_area' % ca.id
        post_data = {ca_form_element_name: 'modified ca',}
        response = self.client.post(test_url, post_data)

        self.assertEqual(response.status_code, 302)
        ca = CompetencyArea.objects.get(pk=ca_pk)
        self.assertEqual(ca.competency_area, 'modified ca')

        # --- Test modifying an essential understanding. ---
        eu = ca.essentialunderstanding_set.all()[0]
        eu_pk = eu.pk
        eu_form_element_name = 'eu_form_%d-essential_understanding' % eu.id
        post_data = {eu_form_element_name: 'modified eu',}
        response = self.client.post(test_url, post_data)

        self.assertEqual(response.status_code, 302)
        eu = EssentialUnderstanding.objects.get(pk=eu_pk)
        self.assertEqual(eu.essential_understanding, 'modified eu')

        # --- Test that setting sa private sets all descendants private.
        # Start with sa, and all descendants public.
        sa_id = sa.id
        sa.public = True
        sa.save()
        utils.cascade_visibility_down(sa, 'public')
        sa = SubjectArea.objects.get(id=sa_id)
        # Verify sa, and at least its sdas are now public.
        self.assertTrue(sa.public)
        for sda in sa.subdisciplinearea_set.all():
            self.assertTrue(sda.public)
        # Set sa private through view, and verify all elements are private.
        post_data = {'subject_area': sa.subject_area, 'public': False}
        response = self.client.post(test_url, post_data)
        self.assertEqual(response.status_code, 302)
        sa = SubjectArea.objects.get(id=sa_id)
        self.assertFalse(sa.public)
        for sda in sa.subdisciplinearea_set.all():
            self.assertFalse(sda.public)
        for ca in sa.competencyarea_set.all():
            self.assertFalse(ca.public)
            for eu in ca.essentialunderstanding_set.all():
                self.assertFalse(eu.public)

        # --- Test that setting eu public cascades up to sa.
        pass


    def generic_test_blank_form(self, test_url):
        """A helper method to test that a form-based page returns a blank form properly."""
        # Test that a logged in user can get a blank form properly.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)


    # --- Test view utilities ---
    def test_cascade_visibility_down(self):
        """Test that cascading visibility reaches all elements."""
        self.num_orgs = 1
        self.build_to_eus()

        # Verify that all elements start out private.
        element_lists = [self.test_sas, self.test_sdas, self.test_cas, self.test_eus]
        for element_list in element_lists:
            for element in element_list:
                self.assertFalse(element.public)

        # Set each org public, and cascade public down for each org.
        for org in self.test_organizations:
            org.public = True
            org.save()
            # Calling utils.cvd() saves to db, but doesn't modify original objects.
            utils.cascade_visibility_down(org, 'public')

        # Test that all orgs are public.
        for org in self.test_organizations:
            self.assertTrue(org.public)

        # Test that all related elements in the db are public.
        for element_list in element_lists:
            db_elements = element_list[0].__class__.objects.all()
            for db_element in db_elements:
                self.assertTrue(db_element.public)

        # Set each org private, and cascade private down for each org.
        for org in self.test_organizations:
            org.public = False
            org.save()
            # Calling utils.cvd() saves to db, but doesn't modify original objects.
            utils.cascade_visibility_down(org, 'private')

        # Test that all orgs are private.
        for org in self.test_organizations:
            self.assertFalse(org.public)

        # Test that all related elements in the db are private.
        for element_list in element_lists:
            db_elements = element_list[0].__class__.objects.all()
            for db_element in db_elements:
                self.assertFalse(db_element.public)

    def test_cascade_public_up(self):
        """Test utils.cascade_public_up()."""
        # Make sure to test that organization is not set public on cascade.
        self.build_to_eus()
        org = Organization.objects.get(id=1)
        # Grab first available eu from the org.
        for eu in EssentialUnderstanding.objects.all():
            if eu.get_organization() == org:
                break
        # Verify eu private, then set public.
        self.assertFalse(eu.public)
        eu.public = True
        # Cascade public up, and test cascade.
        utils.cascade_public_up(eu)
        element = eu.get_parent()
        while element.__class__ != Organization:
            self.assertTrue(element.public)
            element = element.get_parent()
        # Element is now org, verify it's still private.
        self.assertFalse(element.public)

    def test_move_element(self):
        """Test that move_element() results in the proper new order when appropriate."""
        # Tests: sa eu, sda eu; sa first eu up, sa last eu down
        self.num_elements = 4
        self.build_to_eus()
        org = Organization.objects.get(id=1)

        # --- General sa ca eus. ---
        # Get an sa, ca, and eu.
        sa = org.subjectarea_set.all()[0]
        ca = sa.competencyarea_set.all()[0]
        eus = ca.essentialunderstanding_set.all()
        original_order = ca.get_essentialunderstanding_order()
        first_eu = eus[0]

        # Call move_element without logging in, make sure order doesn't change.
        test_url = reverse('competencies:move_element', args=['EssentialUnderstanding', first_eu.id,
                                                                 'down', sa.id])
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        current_order = ca.get_essentialunderstanding_order()
        self.assertEqual(current_order, original_order)

        # Log in, move first element down, and make sure order has changed correctly.
        self.client.login(username='testuser0', password='pw')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        correct_order = [original_order[1], original_order[0]]
        for item in original_order[2:]:
            correct_order.append(item)
        current_order = ca.get_essentialunderstanding_order()
        self.assertEqual(current_order, correct_order)

        # Move first element up, make sure order doesn't change.
        eus = ca.essentialunderstanding_set.all()
        original_order = ca.get_essentialunderstanding_order()
        first_eu = eus[0]
        test_url = reverse('competencies:move_element', args=['EssentialUnderstanding', first_eu.id,
                                                                 'up', sa.id])
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        current_order = ca.get_essentialunderstanding_order()
        self.assertEqual(current_order, original_order)

        # Move last element up, and make sure order has changed correctly.
        eus = ca.essentialunderstanding_set.all()
        original_order = ca.get_essentialunderstanding_order()
        last_eu = eus.reverse()[0]
        test_url = reverse('competencies:move_element', args=['EssentialUnderstanding', last_eu.id,
                                                                 'up', sa.id])
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        correct_order = original_order[:]
        correct_order[-1], correct_order[-2] = correct_order[-2], correct_order[-1]
        current_order = ca.get_essentialunderstanding_order()
        self.assertEqual(current_order, correct_order)

        # Move last element down, make sure order doesn't change.
        eus = ca.essentialunderstanding_set.all()
        original_order = ca.get_essentialunderstanding_order()
        last_eu = eus.reverse()[0]
        test_url = reverse('competencies:move_element', args=['EssentialUnderstanding', last_eu.id,
                                                                 'down', sa.id])
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        current_order = ca.get_essentialunderstanding_order()
        self.assertEqual(current_order, original_order)

        # Test moving first general sa ca down, changes; then first up with no change.

        # Test moving last general sa ca up, changes; then down with no change.
