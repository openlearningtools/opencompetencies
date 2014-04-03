from django.test import TestCase

from competencies.models import *
import testing_utilities as tu

class TestForkSchools(TestCase):

    def setUp(self):
        # Create a school.
        self.school_0 = tu.create_school(name="School 0")

    def test_fork_school(self):
        # Make a new school, and fork school_o's system.
        pass

    def test_fork_school_from_view(self):
        # Do the same thing as test_fork_school, but through 
        #  view interface.
        pass
