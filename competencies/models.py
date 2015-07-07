from django.db import models
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, CheckboxSelectMultiple
from django.forms import EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# --- Competency System Hierarchy ---

# Description of common attributes:
#  public: whether a non-logged in user can see this element
#  description: a public-facing narrative description of this element
#  student-friendly: Many parts of a standards system are written in 'teacher language',
#    which is not very accessible to students. This is a rephrasing of the element in
#    language that is easier for students to understand.

class Organization(models.Model):
    name = models.CharField(max_length=500)
    org_type = models.CharField(max_length=500, default='school')
    owner = models.ForeignKey(User)

    # Allow organizations to rename taxonomy elements.
    alias_sa = models.CharField(max_length=500, default='subject area')
    alias_sda = models.CharField(max_length=500, default='subdiscipline area')
    alias_ca = models.CharField(max_length=500, default='competency area')
    alias_eu = models.CharField(max_length=500, default='essential understanding')
    alias_lt = models.CharField(max_length=500, default='learning target')

    class Meta:
        unique_together = ('name', 'owner',)

    def __str__(self):
        return self.name

class CoreElement(models.Model):
    public = models.BooleanField(default=False)
    student_friendly = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

class SubjectArea(CoreElement):
    subject_area = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.subject_area

    class Meta:
        order_with_respect_to = 'organization'

    def is_parent_public(self):
        return True

    def get_parent(self):
        return self.organization

class SubdisciplineArea(CoreElement):
    subdiscipline_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)

    def __str__(self):
        return self.subdiscipline_area

    class Meta:
        order_with_respect_to = 'subject_area'

    def is_parent_public(self):
        return self.subject_area.public

    def get_parent(self):
        return self.subject_area

class CompetencyArea(CoreElement):
    competency_area = models.CharField(max_length=500)
    subject_area = models.ForeignKey(SubjectArea)
    subdiscipline_area = models.ForeignKey(SubdisciplineArea, blank=True, null=True)

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

class EssentialUnderstanding(CoreElement):
    essential_understanding = models.CharField(max_length=2000)
    competency_area = models.ForeignKey(CompetencyArea)

    def __str__(self):
        return self.essential_understanding

    class Meta:
        order_with_respect_to = 'competency_area'

    def is_parent_public(self):
        return self.competency_area.public

    def get_parent(self):
        return self.competency_area

class LearningTarget(CoreElement):
    learning_target = models.CharField(max_length=2000)
    essential_understanding = models.ForeignKey(EssentialUnderstanding)

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
    # User is allowed to edit any aspect of any organization in this list.
    organizations = models.ManyToManyField(Organization, blank=True)
    # User is allowed to edit any descendent of any subject_area in this list.
    subject_areas = models.ManyToManyField(SubjectArea, blank=True)


# --- ModelForms ---
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        labels = {'name': 'New organization name',}
        widgets = {
            'name': TextInput(attrs={'class': 'span4'}),
            }

class SubjectAreaForm(ModelForm):
    class Meta:
        model = SubjectArea
        fields = ('subject_area', 'description')
        widgets = {
            'subject_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class SubdisciplineAreaForm(ModelForm):
    # Hacky way to get id of instance from a form in a template (edit_sa_summary).
    my_id = None
    class Meta:
        model = SubdisciplineArea
        fields = ('subdiscipline_area', 'description')
        widgets = {
            'subdiscipline_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class CompetencyAreaForm(ModelForm):
    # Hacky way to get id of instance from a form in a template (edit_sa_summary).
    my_id = None
    class Meta:
        model = CompetencyArea
        fields = ('competency_area', 'student_friendly', 'description')
        labels = {'competency_area': 'Competency Area'}
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'competency_area': Textarea(attrs={'rows': 5, 'class': 'span4'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class EssentialUnderstandingForm(ModelForm):
    class Meta:
        model = EssentialUnderstanding
        fields = ('essential_understanding', 'student_friendly', 'description')
        labels = {'essential_understanding': 'Essential Understanding'}
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'essential_understanding': Textarea(attrs={'rows': 5, 'class': 'span7'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class LearningTargetForm(ModelForm):
    class Meta:
        model = LearningTarget
        fields = ('learning_target', 'student_friendly', 'description')
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'learning_target': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class RegisterUserForm(UserCreationForm):
    #email = EmailField(required=False, label='Email (optional)')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {'email': 'Email (optional)'}

        widgets = {
            'username': TextInput(attrs={'class': 'span5'}),
            'email': TextInput(attrs={'class': 'span5'}),
            }

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        if self.cleaned_data["email"]:
            user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
