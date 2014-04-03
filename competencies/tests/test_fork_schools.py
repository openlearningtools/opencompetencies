from django.test import TestCase
from django.core.urlresolvers import reverse

from competencies.models import *


def create_school(name):
    """Creates a school with the given name."""
    return School.objects.create(name=name)

def create_subject_area(subject_area, school):
    """Creates a subject_area, with fk to given school."""
    return SubjectArea.objects.create(subject_area=subject_area, school=school)

class CompetencyViewTests2(TestCase):
    """Needed tests:
    - queryset tests for all pages
    - no-data tests
    """

    def test_index_view(self):
        """Index page is a static page for now, so just check status."""
        response = self.client.get(reverse('competencies:index'))
        print('here2')
        self.assertEqual(response.status_code, 200)

