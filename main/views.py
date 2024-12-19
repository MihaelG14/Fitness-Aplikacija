from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import KorisnickiProfil, FitnessCilj, Vjezba
from django.db.models import Q

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




class KorisnickiProfilListView(LoginRequiredMixin, ListView):
    model = KorisnickiProfil
    template_name = 'main/korisnicki_profil_list.html'
    context_object_name = 'profili'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        min_godine = self.request.GET.get('min_godine')
        max_godine = self.request.GET.get('max_godine')
        min_tezina = self.request.GET.get('min_tezina')
        max_tezina = self.request.GET.get('max_tezina')
        
        if search_query:
            queryset = queryset.filter(
                Q(korisnik__username__icontains=search_query) |
                Q(opis__icontains=search_query) |
                Q(godine__icontains=search_query) |
                Q(visina__icontains=search_query) |
                Q(tezina__icontains=search_query)
            )
        
        if min_godine:
            queryset = queryset.filter(godine__gte=min_godine)
        if max_godine:
            queryset = queryset.filter(godine__lte=max_godine)
        if min_tezina:
            queryset = queryset.filter(tezina__gte=min_tezina)
        if max_tezina:
            queryset = queryset.filter(tezina__lte=max_tezina)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_godine'] = self.request.GET.get('min_godine', '')
        context['max_godine'] = self.request.GET.get('max_godine', '')
        context['min_tezina'] = self.request.GET.get('min_tezina', '')
        context['max_tezina'] = self.request.GET.get('max_tezina', '')
        return context
    
class FitnessCiljListView(LoginRequiredMixin, ListView):
    model = FitnessCilj
    template_name = 'main/fitness_cilj_list.html'
    context_object_name = 'ciljevi'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        min_ciljna = self.request.GET.get('min_ciljna')
        max_ciljna = self.request.GET.get('max_ciljna')
        min_trenutna = self.request.GET.get('min_trenutna')
        max_trenutna = self.request.GET.get('max_trenutna')
        
        if search_query:
            queryset = queryset.filter(
                Q(naziv_cilja__icontains=search_query) |
                Q(korisnik__korisnik__username__icontains=search_query)
            )
        
        if min_ciljna:
            queryset = queryset.filter(ciljna_vrijednost__gte=min_ciljna)
        if max_ciljna:
            queryset = queryset.filter(ciljna_vrijednost__lte=max_ciljna)
        if min_trenutna:
            queryset = queryset.filter(trenutna_vrijednost__gte=min_trenutna)
        if max_trenutna:
            queryset = queryset.filter(trenutna_vrijednost__lte=max_trenutna)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_ciljna'] = self.request.GET.get('min_ciljna', '')
        context['max_ciljna'] = self.request.GET.get('max_ciljna', '')
        context['min_trenutna'] = self.request.GET.get('min_trenutna', '')
        context['max_trenutna'] = self.request.GET.get('max_trenutna', '')
        return context

class VjezbaListView(LoginRequiredMixin, ListView):
    model = Vjezba
    template_name = 'main/vjezba_list.html'
    context_object_name = 'vjezbe'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        min_trajanje = self.request.GET.get('min_trajanje')
        max_trajanje = self.request.GET.get('max_trajanje')
        min_kalorije = self.request.GET.get('min_kalorije')
        max_kalorije = self.request.GET.get('max_kalorije')
        
        if search_query:
            queryset = queryset.filter(
                Q(naziv_vjezbe__icontains=search_query) |
                Q(korisnik__korisnik__username__icontains=search_query)
            )
        
        if min_trajanje:
            queryset = queryset.filter(trajanje__gte=min_trajanje)
        if max_trajanje:
            queryset = queryset.filter(trajanje__lte=max_trajanje)
        if min_kalorije:
            queryset = queryset.filter(potrosene_kalorije__gte=min_kalorije)
        if max_kalorije:
            queryset = queryset.filter(potrosene_kalorije__lte=max_kalorije)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_trajanje'] = self.request.GET.get('min_trajanje', '')
        context['max_trajanje'] = self.request.GET.get('max_trajanje', '')
        context['min_kalorije'] = self.request.GET.get('min_kalorije', '')
        context['max_kalorije'] = self.request.GET.get('max_kalorije', '')
        return context
    
class KorisnickiProfilDetailView(LoginRequiredMixin, DetailView):
    model = KorisnickiProfil
    template_name = 'main/korisnicki_profil_detail.html'
    context_object_name = 'profil'

class FitnessCiljDetailView(LoginRequiredMixin, DetailView):
    model = FitnessCilj
    template_name = 'main/fitness_cilj_detail.html'
    context_object_name = 'cilj'

class VjezbaDetailView(LoginRequiredMixin, DetailView):
    model = Vjezba
    template_name = 'main/vjezba_detail.html'
    context_object_name = 'vjezba'