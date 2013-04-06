from django.test import TestCase
from django.core.urlresolvers import reverse

from competencies.models import *


def create_school(name):
    """Creates a school with the given name."""
    return School.objects.create(name=name)

class CompetencyViewTests(TestCase):
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
        django_school = create_school(name="The Django School")
        response = self.client.get(reverse('competencies:school', args=(django_school.id,)))
        self.assertEqual(response.status_code, 200)
