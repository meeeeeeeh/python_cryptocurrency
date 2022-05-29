from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import views, authenticate, login
from .forms import SignUpForm, LoginForm
from bitcoin import *


def signup(request):
    private_key = random_key()
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            User.objects.create_user(username=username, email=email, password=password, first_name=address)
            return redirect("/")
    else:
        form = SignUpForm()
    context = {'form': form}

    return render(request, "signup.html", context)


def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("core:home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user.is_active:
                login(request, user)
                return redirect("core:home")
            else:
                request.session['username'] = username
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.is_active = True
                user.save()
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, "login.html", context)


def wallet(request):
    return render(request, 'wallet.html')
