from django.db import models
from django.contrib.auth.models import User

class KorisnickiProfil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    godine = models.PositiveIntegerField()
    visina = models.FloatField(help_text="Visina u cm")
    tezina = models.FloatField(help_text="Težina u kg")
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.korisnik.username

class FitnessCilj(models.Model):
    korisnik = models.ForeignKey(KorisnickiProfil, on_delete=models.CASCADE, related_name="fitness_ciljevi")
    naziv_cilja = models.CharField(max_length=255)
    ciljna_vrijednost = models.FloatField(help_text="Ciljna vrijednost (npr. ciljna težina, udaljenost ili broj ponavljanja)")
    trenutna_vrijednost = models.FloatField(default=0, help_text="Trenutni napredak")
    rok = models.DateField()

    def __str__(self):
        return f"{self.naziv_cilja} ({self.korisnik.korisnik.username})"

class Vjezba(models.Model):
    korisnik = models.ForeignKey(KorisnickiProfil, on_delete=models.CASCADE, related_name="vjezbe")
    naziv_vjezbe = models.CharField(max_length=255)
    trajanje = models.PositiveIntegerField(help_text="Trajanje u minutama")
    potrosene_kalorije = models.FloatField()
    datum = models.DateField()

    def __str__(self):
        return f"{self.naziv_vjezbe} - {self.korisnik.korisnik.username} ({self.datum})"