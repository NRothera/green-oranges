from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required # can use this so a view can only be seen if someone is logged in




def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('You are logged in, you go man!')

@login_required #with this, you can only see the logout page if you are logged in
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def registration(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)#this hases the password
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user #from models, user is = to a OnetoOne relationship,
            #which is turn is the UserForm in forms.py

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html',
                        {'user_form':user_form, 'profile_form':profile_form,
                        'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password = password)#will authenticate user for you
        if user:#is authenticated
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))#once logged in, will redirect them back to the home page
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed dude')
            print('Username: {} and password {}'.format(username, password))
            return HttpResponse('Invalid login')
    else:
        return render(request, 'basic_app/login.html')


# Create your views here.
