from competencies.models import *


# Utility functions for all tests.

def create_school(name):
    """Creates a school with the given name."""
    return School.objects.create(name=name)

def create_subject_area(subject_area, school):
    """Creates a subject_area, with fk to given school."""
    return SubjectArea.objects.create(subject_area=subject_area, school=school)
