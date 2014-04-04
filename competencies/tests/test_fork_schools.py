from django.test import TestCase

from competencies.models import *
import testing_utilities as tu
import competencies.views as views

class TestForkSchools(TestCase):

    def setUp(self):
        num_schools = 3
        num_subject_areas = 5

        # Create some schools.
        self.schools = []
        for school_num in range(0, num_schools):
            school_name = "School %d" % school_num
            self.schools.append(tu.create_school(name=school_name))

        # Create some subject areas.
        for school in self.schools:
            for sa_num in range(0, num_subject_areas):
                subject_area = "Subject %d" % sa_num
                tu.create_subject_area(subject_area, school)
        
        #self.show_schools()
        

    def show_schools(self):

        for school in self.schools:
            print("\nSchool: %s" % school.name)
            for subject_area in SubjectArea.objects.filter(school=school):
                print("Subject area: %s" % subject_area)


    def test_fork_school(self):
        # Make a new school, and fork school_0's system.
        new_school = tu.create_school(name="New School")
        views.fork_school(new_school, school_0)


    def test_fork_school_from_view(self):
        # Do the same thing as test_fork_school, but through 
        #  view interface.
        pass
