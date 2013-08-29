from django.db import models

class Initiative(models.Model):
    CCSS = 'CCSS'
    INITIATIVE_CHOICES = (
        (CCSS, 'Common Core State Standards'),
        )
    dot_notation = models.CharField(max_length=255)

    initiative = models.CharField(max_length=255,
                           choices=INITIATIVE_CHOICES,
                           default=CCSS)

    def __unicode__(self):
        return self.initiative

class Framework(models.Model):
    """Frameworks are basically subject areas."""
    # Existing frameworks/ subject areas
    ELA_LIT = 'ELA_LIT'
    MATH = 'Math'
    FRAMEWORK_CHOICES = (
        (ELA_LIT, 'ELA-Literacy'),
        (MATH, 'Math'),
        )

    # Dot notations for these frameworks
    DN_ELA_LIT = 'ELA-Literacy'
    DN_MATH = 'Math'
    DN_CHOICES = (
        (DN_ELA_LIT, 'ELA-Literacy'),
        (DN_MATH, 'Math'),
        )

    initiative = models.ForeignKey(Initiative)
    dot_notation = models.CharField(max_length=255, choices=DN_CHOICES)
    description = models.TextField(blank=True)

    framework = models.CharField(max_length=255,
                                 choices=FRAMEWORK_CHOICES,
                                 default=ELA_LIT)

    def __unicode__(self):
        return self.framework

class Set(models.Model):
    pass

class Domain(models.Model):
    """These are like subdiscipline areas."""
    WRITING = 'Writing'
    READING = 'Reading'
    SPEAKING_LISTENING = 'Speaking and Listening'
    SSE = 'Seeing Structure in Expressions'
    DOMAIN_CHOICES = (
        (WRITING, 'Writing'),
        (READING, 'Reading'),
        (SPEAKING_LISTENING, 'Speaking and Listening'),
        (SSE, 'Seeing Structure in Expressions'),
        )

    DN_WRITING = 'W'
    DN_READING = 'R'
    DN_SPEAKING_LISTENING = 'SL'
    DN_SSE = 'SSE'
    DN_CHOICES = (
        (DN_WRITING, 'W'),
        (DN_READING, 'R'),
        (DN_SPEAKING_LISTENING, 'SL'),
        (DN_SSE, 'SSE'),
        )

    framework = models.ForeignKey(Framework)
    dot_notation = models.CharField(max_length=255,
                                    choices=DN_CHOICES)
    description = models.TextField(blank=True)

    domain = models.CharField(max_length=255,
                                     choices=DOMAIN_CHOICES)

    def __unicode__(self):
        return self.domain

class Grade(models.Model):
    grade = models.CharField(max_length=255)
    dot_notation = models.CharField(max_length=255)

    def __unicode__(self):
        return self.grade

class Standard(models.Model):
    standard = models.TextField()
    domain = models.ForeignKey(Domain)
    grade = models.ManyToManyField(Grade)
    dot_notation = models.CharField(max_length=255)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.standard

class Component(models.Model):
    component = models.TextField()
    standard = models.ForeignKey(Standard)
    dot_notation = models.CharField(max_length=255)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.component

class ELAElement(models.Model):
    component = models.ForeignKey(Component, blank=True, null=True)
    dot_notation = models.CharField(max_length=255)

    def get_elements_from_dot_notation(self):
        pass #parse dot notation, return elements from that
