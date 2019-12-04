from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf

from UserApp.forms import RegistrationForm, AccountAuthenticationForm
from GameShop.urls import path


# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('GameShop:index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'UserApp/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('GameShop:index')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('GameShop:index')
    # if user.is_active == False:
    #     # user.is_anonymous = True
    #     HttpResponse('You are banned')
    #     return redirect('GameShop:index')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('GameShop:index')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    # context.update(csrf(request))
    return render(request, 'UserApp/login.html', context)