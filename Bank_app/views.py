from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Custom decorator to redirect unauthenticated users to the login page
def login_required_custom(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrapper

# Home page
def home(request):
    return render(request, 'home.html')

# Login page
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('new_page')
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs['value'] = ''  # Set initial value for username to blank
        form.fields['password'].widget.attrs['value'] = ''  # Set initial value for password to blank
    return render(request, 'login.html', {'form': form})

# Registration page
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Logout page
def user_logout(request):
    logout(request)
    return redirect('login')

# New page
@login_required_custom
def new_page_view(request):
    return render(request, 'new_page.html')

# Form page
@login_required_custom
def form(request):
    return render(request, "form.html")
