from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from articles.models import Article
from .forms import SignupForm, LoginForm

def home(request):
    articles = Article.objects.filter(status='approved')[:5]
    return render(request, 'core/home.html', {'articles': articles})


def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                # ROLE BASED REDIRECT
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'journalist':
                    return redirect('journalist_dashboard')
                elif user.role == 'reader':
                    return redirect('reader_dashboard')
                elif user.role == 'advertiser':
                    return redirect('advertiser_dashboard')

            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

