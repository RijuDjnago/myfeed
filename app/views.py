from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from faker import Faker
import random
from datetime import datetime, timedelta
from .forms import SignUpForm, ProfileForm


def index(request):
    fake = Faker()
    suggested_users = [{'name': fake.name()} for _ in range(100)]
    posts = []
    for i in range(50):
        num_images = random.randint(1, 3)
        images = [f"https://picsum.photos/600/400?random={i * 3 + j}" for j in range(num_images)]
        post = {
            'author': random.choice(suggested_users)['name'],
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            'content': fake.text(max_nb_chars=200),
            'images': images,
            'comments': []
        }
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
            comment = {
                'author': random.choice(suggested_users)['name'],
                'text': fake.sentence(nb_words=10)
            }
            post['comments'].append(comment)
        posts.append(post)
    return render(request, 'sides/index.html', {'suggested_users': suggested_users, 'posts': posts})

def login_signup_view(request):
    login_form = AuthenticationForm()
    signup_form = SignUpForm()

    if request.method == 'POST':
        if request.POST.get('form_type') == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        elif request.POST.get('form_type') == 'signup':
            signup_form = SignUpForm(request.POST, request.FILES)
            if signup_form.is_valid():
                user = signup_form.save()
                profile = user.profile
                profile.gender = signup_form.cleaned_data.get('gender')
                profile.bio = signup_form.cleaned_data.get('bio')
                profile.profile_image = signup_form.cleaned_data.get('profile_image')
                profile.dob = signup_form.cleaned_data.get('dob')
                profile.save()
                username = signup_form.cleaned_data.get('username')
                password = signup_form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')

    return render(request, 'authentication/auth.html', {'login_form': login_form, 'signup_form': signup_form})

def profile_view(request):
    fake = Faker()
    if not request.user.is_authenticated:
        return redirect('login_signup')

    # Static feed data for profile
    profile_posts = []
    for i in range(5):  # 5 posts for demo
        num_images = random.randint(1, 3)
        images = [f"https://picsum.photos/600/400?random={i * 3 + j + 100}" for j in range(num_images)]
        post = {
            'author': request.user.username,
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            'content': fake.text(max_nb_chars=200),
            'images': images,
            'comments': []
        }
        num_comments = random.randint(0, 3)
        for _ in range(num_comments):
            comment = {
                'author': fake.name(),
                'text': fake.sentence(nb_words=10)
            }
            post['comments'].append(comment)
        profile_posts.append(post)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'sides/profile.html', {'form': form, 'posts': profile_posts})

