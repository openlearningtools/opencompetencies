from django.db import models

class School(models.Model):
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

class SubjectArea(models.Model):
    subject_area = models.CharField(max_length=500)
    school = models.ForeignKey(School)

    def __unicode__(self):
        return self.subject_area

class SubdisciplineArea(models.Model):
    subdiscipline_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)

    def __unicode__(self):
        return self.subdiscipline_area

class CompetencyArea(models.Model):
    competency_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)
    subdiscipline_area = models.ForeignKey(SubdisciplineArea, blank=True, null=True)

    def __unicode__(self):
        return self.competency_area

class EssentialUnderstanding(models.Model):
    essential_understanding = models.CharField(max_length=2000)
    competency_area = models.ForeignKey(CompetencyArea)

    def __unicode__(self):
        return self.essential_understanding

class LearningTarget(models.Model):
    learning_target = models.CharField(max_length=2000)
    essential_understanding = models.ForeignKey(EssentialUnderstanding)

    def __unicode__(self):
        return self.learning_target
