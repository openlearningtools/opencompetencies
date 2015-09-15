from django.db import models
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, CheckboxSelectMultiple
from django.forms import EmailField
from django.contrib.auth.models import User

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
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    editors = models.ManyToManyField(User, related_name='org_editors')

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

    def get_organization(self):
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

    def get_organization(self):
        return self.subject_area.get_organization()

    def get_alias(self):
        return self.get_organization().alias_sda

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
        # Maybe this should just return subject area?
        #   Would make managing ordering easier.
        if self.subdiscipline_area:
            return self.subdiscipline_area
        else:
            return self.subject_area

    def get_organization(self):
        return self.subject_area.get_organization()

    def get_alias(self):
        return self.get_organization().alias_ca

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

    def get_organization(self):
        return self.competency_area.get_organization()

    def get_alias(self):
        return self.get_organization().alias_eu

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

    def get_organization(self):
        return self.essential_understanding.get_organization()


# --- ModelForms ---
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'org_type')
        labels = {'name': 'Name of new school or organization',
                  'org_type': 'Type of organization',}
        widgets = {
            'name': TextInput(attrs={'class': 'span4'}),
            'org_type': TextInput(attrs={'class': 'span4'}),
            }

class OrganizationAdminForm(OrganizationForm):
    """Extends OrganizationForm to include admin elements."""
    class Meta(OrganizationForm.Meta):
        fields = ('name', 'org_type', 'public',
                  'alias_sa', 'alias_sda', 'alias_ca', 'alias_eu', 'alias_lt',
                  'editors',
                  )
        OrganizationForm.Meta.labels['name'] = 'Name'
        OrganizationForm.Meta.labels['alias_sa'] = 'Alias - subject area'
        OrganizationForm.Meta.labels['alias_sda'] = 'Alias - subdiscipline area'
        OrganizationForm.Meta.labels['alias_ca'] = 'Alias - competency area'
        OrganizationForm.Meta.labels['alias_eu'] = 'Alias - essential understanding'
        OrganizationForm.Meta.labels['alias_lt'] = 'Alias - learning target'



class SubjectAreaForm(ModelForm):
    class Meta:
        model = SubjectArea
        fields = ('subject_area', 'description', 'public')
        widgets = {
            'subject_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class SubdisciplineAreaForm(ModelForm):
    # Hacky way to get id of instance from a form in a template (edit_sa_summary).
    my_id = None
    class Meta:
        model = SubdisciplineArea
        fields = ('subdiscipline_area', 'description', 'public')
        widgets = {
            'subdiscipline_area': TextInput(attrs={'class': 'span4'}),
            'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
            }

class CompetencyAreaForm(ModelForm):
    # Hacky way to get id of instance from a form in a template (edit_sa_summary).
    my_id = None
    class Meta:
        model = CompetencyArea
        fields = ('competency_area', 'student_friendly', 'description', 'public')
        labels = {'competency_area': 'Competency Area'}
        # Bootstrap controls width of Textarea, ignoring the 'cols' setting. Can also use 'class': 'input-block-level'
        widgets = {'competency_area': Textarea(attrs={'rows': 5, 'class': 'span4'}),
                   'student_friendly': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   'description': Textarea(attrs={'rows': 5, 'class': 'span8'}),
                   }

class EssentialUnderstandingForm(ModelForm):
    class Meta:
        model = EssentialUnderstanding
        fields = ('essential_understanding', 'student_friendly', 'description', 'public')
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
