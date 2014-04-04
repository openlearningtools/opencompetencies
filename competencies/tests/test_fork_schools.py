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
        views.fork_school(new_school, self.schools[0])

        # Verify that all of forking school's subject areas are in forked school's sa's.
        #  Get sa objects. Then get sa names for the forked school.
        #  Really want to verify that the names of each sa are in the forked school.
        #  Not testing for object identity.
        new_school_sas = SubjectArea.objects.filter(school=new_school)
        forked_school_sas = SubjectArea.objects.filter(school=self.schools[0])
        forked_school_sa_names = [sa.subject_area for sa in forked_school_sas]

        for sa in new_school_sas:
            self.assertEqual(sa.subject_area in forked_school_sa_names, True)

        # DEV: Full test will verify that all appropriate aspects of a forked school
        #  get copied over correctly to the new school.


    def test_fork_school_from_view(self):
        # Do the same thing as test_fork_school, but through 
        #  view interface.
        pass
