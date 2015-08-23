from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import password_change
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from competencies.models import *
from competencies import my_admin
from competencies import utils
from users.models import *

# Authentication views
def logout_view(request):
    logout(request)
    # Redirect to home page for now. Later, maybe stay on same page.
    return redirect('/')

@login_required
def profile(request):
    editor_orgs = request.user.organization_set.all()
    return render_to_response('users/profile.html',
                              {'editor_orgs': editor_orgs},
                              context_instance=RequestContext(request))

def password_change_form(request):
    if request.method == 'POST':
        return password_change(request, post_change_redirect='/password_change_successful')
    else:
        return render_to_response('users/password_change_form.html',
                                  {},
                                  context_instance=RequestContext(request))

def password_change_successful(request):
    return render_to_response('users/password_change_successful.html',
                              {},
                              context_instance=RequestContext(request))

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        # Process completed form.
        form = RegisterUserForm(data=request.POST)
        
        if form.is_valid():
            user = form.save()
            my_admin.add_userprofile(user)
            
            # Log the user in, and then redirect to home page.
            user = authenticate(username=user,
                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('competencies:index'))
    else:
        # Display blank registration form.        
        form = RegisterUserForm()
        
    context = {'form': form}
    return render_to_response('users/register.html',
                              context,
                              context_instance=RequestContext(request))
