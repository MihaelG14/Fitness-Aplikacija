from django.contrib import admin
from .models import KorisnickiProfil, FitnessCilj, Vjezba
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(KorisnickiProfil)
class KorisnickiProfilAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'godine', 'visina', 'tezina')
    search_fields = ('korisnik__username',)

@admin.register(Vjezba)
class VjezbaAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'naziv_vjezbe', 'trajanje', 'potrosene_kalorije', 'datum')
    search_fields = ('korisnik__korisnik__username', 'naziv_vjezbe')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)