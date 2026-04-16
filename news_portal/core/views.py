from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from articles.models import Article
from advertisements.models import Advertisement
from .forms import SignupForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    articles = Article.objects.filter(status='approved').order_by('-created_at')[:5]
    ads = Advertisement.objects.filter(status='approved').order_by('-created_at')[:3]

    return render(request, 'core/home.html', {
        'articles': articles,
        'ads': ads
    })


def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # SEND EMAIL
            send_mail(
                subject='Welcome to News Portal',
                message=f'''
        Hello {user.first_name},

        Your account has been created successfully!

        Username: {user.username}

        You can login here:
        http://127.0.0.1:8000/login/

        Thank you!
                ''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # 🔥 ROLE BASED REDIRECT
            if user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'journalist':
                return redirect('journalist_dashboard')

            elif user.role == 'reader':
                return redirect('reader_dashboard')

            elif user.role == 'advertiser':
                return redirect('advertiser_dashboard')
           
    else:
        form = SignupForm()

    return render(request, 'core/register.html', {'form': form})

print("VIEW WORKING")
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

