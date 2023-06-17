from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import MusicFile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def home(request):
    user = request.user
    music_files = MusicFile.objects.filter(
        models.Q(access=MusicFile.PUBLIC) | models.Q(user=user) | models.Q(allowed_emails__contains=user.email)
    )
    return render(request, 'home.html', {'music_files': music_files})
