from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserProfile(models.Model):
    """Was here to manage m2m relation to Organization."""
    # Keeping this, because I'll store more information about users at some point.
    user = models.OneToOneField(User)


# --- Forms ---

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
