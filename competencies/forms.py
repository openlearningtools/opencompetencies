from django import forms

from .models import *

class ForkForm(forms.Form):
    """Presents a list of orgs to choose from when forking an org."""

    # DEV: Exclude forking org from this queryset.
    #  Requires passing forking_org to __init__().
    available_organizations = Organization.objects.filter(public=True)
    organization = forms.ModelChoiceField(queryset=available_organizations, empty_label=None)
