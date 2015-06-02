from django.test import TestCase
from django.core.urlresolvers import reverse

from competencies.models import *
from competencies.tests import testing_utilities as tu


class CompetencyViewTests(TestCase):
    """Needed tests:
    - queryset tests for all pages
    - no-data tests
    """

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
        django_school = tu.create_school(name="The Django School")
        response = self.client.get(reverse('competencies:school', args=(django_school.id,)))
        self.assertEqual(response.status_code, 200)

    def test_subject_area_view(self):
        """Subject area page lists general competencies for a single subject area,
        and competencies for that subject's subdiscipline areas."""
        django_school = tu.create_school(name="The Django School")
        science = tu.create_subject_area(subject_area="Science", school=django_school)
        response = self.client.get(reverse('competencies:subject_area', args=(science.id,)))

    def test_competency_area_view(self):
        """Competency area page lists all essential understandings and learning targets
        associated with a given competency area."""
        # Need to make functions create_competency_area, create_essential_understanding,
        #  create_learning_target
        pass

    def test_new_school(self):
        """New school processes form to create a new school.
        """
        pass

    def test_edit_system(self):
        """Edit system allows user to edit a school's entire competency system
        on one page.
        """
        pass
