from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registracija uspješna!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_staff': user.is_staff,
    }
    return render(request, 'main/profile.html', context)

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'main/admin_dashboard.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_staff = request.POST.get('is_staff') == 'on'
        
        if username and email:
            user.username = username
            user.email = email
            user.is_staff = is_staff
            user.save()
            messages.success(request, 'Korisnik uspješno ažuriran.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Molimo popunite sva polja.')
    
    return render(request, 'main/edit_user.html', {'edit_user': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if user != request.user:
            user.delete()
            messages.success(request, 'Korisnik uspješno obrisan.')
        else:
            messages.error(request, 'Ne možete obrisati vlastiti račun.')
    return redirect('admin_dashboard')
    

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_staff = request.POST.get('is_staff') == 'on'
            user.is_staff = is_staff
            user.save()
            messages.success(request, 'Korisnički račun uspješno kreiran!')
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/create_user.html', {'form': form})