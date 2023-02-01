from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseServerError
import os
import logging
logger = logging.getLogger(__name__)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except: 
            messages.error(request, 'User does not exist')

        if username == 'guest': 
            password = os.environ.get('GUEST_PASSWORD')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': 'login'}
    return render(request, 'authentication/login_register.html', context)

def loginGuest(request):
    username = 'guest'
    password = os.environ.get('GUEST_PASSWORD')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Username or password does not exist')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    try:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                print(form)
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.first_name = request.POST.get('firstname')
                user.last_name = request.POST.get('lastname')
                user.save()
                login(request, user)
                return redirect('home')
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        print(f'Error in {field}: {error}')
                messages.error(request, 'An error occured during registration')
        return render(request, 'authentication/signup.html')
    except Exception as e:
        logger.error(str(e))
        return HttpResponseServerError("Something went wrong.")

        

