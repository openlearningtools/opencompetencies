from django.db import models
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, CheckboxSelectMultiple
from django.contrib.auth.models import User

# --- Competency System Hierarchy ---

# Description of common attributes:
#  public: whether a non-logged in user can see this element
#  description: a public-facing narrative description of this element
#  student-friendly: Many parts of a standards system are written in 'teacher language',
#    which is not very accessible to students. This is a rephrasing of the element in
#    language that is easier for students to understand.

class School(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class SubjectArea(models.Model):
    subject_area = models.CharField(max_length=500)
    school = models.ForeignKey(School)
    public = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.subject_area

    class Meta:
        order_with_respect_to = 'school'

    def is_parent_public(self):
        return True

    def get_parent(self):
        return self.school

class SubdisciplineArea(models.Model):
    subdiscipline_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)
    public = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.subdiscipline_area

    class Meta:
        order_with_respect_to = 'subject_area'

    def is_parent_public(self):
        return self.subject_area.public

    def get_parent(self):
        return self.subject_area

class CompetencyArea(models.Model):
    competency_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)
    subdiscipline_area = models.ForeignKey(SubdisciplineArea, blank=True, null=True)
    public = models.BooleanField(default=False)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)
    alias = models.CharField(max_length=500, default="Graduation Standard")

    def __str__(self):
        return self.competency_area

    class Meta:
        order_with_respect_to = 'subject_area'

    def is_parent_public(self):
        # If no sda, then only use subject_area
        if self.subdiscipline_area:
            sda_public = self.subdiscipline_area.public
        else:
            sda_public = True

        if self.subject_area.public and sda_public:
            return True
        else:
            return False

    def get_parent(self):
        return self.subject_area

class Level(models.Model):
    APPRENTICE = 'Apprentice'
    TECHNICIAN = 'Technician'
    MASTER = 'Master'
    PROFESSIONAL = 'Professional'
    LEVEL_TYPE_CHOICES = ( (APPRENTICE, 'Apprentice'), (TECHNICIAN, 'Technician'),
                           (MASTER, 'Master'), (PROFESSIONAL, 'Professional') )
    level_type = models.CharField(max_length=500, choices=LEVEL_TYPE_CHOICES)
    level_description = models.CharField(max_length=5000)
    competency_area = models.ForeignKey(CompetencyArea)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.level_description

    class Meta:
        unique_together = ('competency_area', 'level_type',)
        order_with_respect_to = 'competency_area'

    def is_parent_public(self):
        return self.competency_area.public

    def get_parent(self):
        return self.competency_area

class EssentialUnderstanding(models.Model):
    essential_understanding = models.CharField(max_length=2000)
    competency_area = models.ForeignKey(CompetencyArea)
    public = models.BooleanField(default=False)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.essential_understanding

    class Meta:
        order_with_respect_to = 'competency_area'

    def is_parent_public(self):
        return self.competency_area.public

    def get_parent(self):
        return self.competency_area

class LearningTarget(models.Model):
    learning_target = models.CharField(max_length=2000)
    essential_understanding = models.ForeignKey(EssentialUnderstanding)
    public = models.BooleanField(default=False)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.learning_target

    class Meta:
        order_with_respect_to = 'essential_understanding'

    def is_parent_public(self):
        return self.essential_understanding.public

    def get_parent(self):
        return self.essential_understanding


# --- User Information ---

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # User is allowed to edit any aspect of any school in this list.
    schools = models.ManyToManyField(School, blank=True)
    # User is allowed to edit any descendent of any subject_area in this list.
    subject_areas = models.ManyToManyField(SubjectArea, blank=True)

# --- ModelForms ---
class SubjectAreaForm(ModelForm):
    class Meta:
        model = SubjectArea
        fields = ('subject_area', 'description')
        widgets = {
            'subject_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class SubdisciplineAreaForm(ModelForm):
    class Meta:
        model = SubdisciplineArea
        fields = ('subdiscipline_area', 'description')
        widgets = {
            'subdiscipline_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class CompetencyAreaForm(ModelForm):
    class Meta:
        model = CompetencyArea
        fields = ('competency_area', 'student_friendly', 'description')
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'competency_area': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class EssentialUnderstandingForm(ModelForm):
    class Meta:
        model = EssentialUnderstanding
        fields = ('essential_understanding', 'student_friendly', 'description')
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'essential_understanding': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class LevelForm(ModelForm):
    class Meta:
        model = Level
        fields = ('level_type', 'level_description',)
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'level_description': Textarea(attrs={'rows': 5, 'class': 'span8'}) }

class LearningTargetForm(ModelForm):
    class Meta:
        model = LearningTarget
        fields = ('learning_target', 'student_friendly', 'description')
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'learning_target': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }
