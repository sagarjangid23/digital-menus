from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, HttpResponseRedirect
from account.forms import LoginForm, RegistrationForm


def signup_view(request):

    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password')
            authenticate(username=username, password=raw_pass)
            return HttpResponseRedirect('login')
    else:
        form = RegistrationForm()
    return render(request, "account/signup.html", {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("login")

def login_view(request):

    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {'form': form})
