# Generated by Django 5.1.2 on 2024-11-28 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KorisnickiProfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('godine', models.PositiveIntegerField()),
                ('visina', models.FloatField(help_text='Visina u cm')),
                ('tezina', models.FloatField(help_text='Težina u kg')),
                ('opis', models.TextField(blank=True, null=True)),
                ('korisnik', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessCilj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv_cilja', models.CharField(max_length=255)),
                ('ciljna_vrijednost', models.FloatField(help_text='Ciljna vrijednost (npr. ciljna težina, udaljenost ili broj ponavljanja)')),
                ('trenutna_vrijednost', models.FloatField(default=0, help_text='Trenutni napredak')),
                ('rok', models.DateField()),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fitness_ciljevi', to='main.korisnickiprofil')),
            ],
        ),
        migrations.CreateModel(
            name='Vjezba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv_vjezbe', models.CharField(max_length=255)),
                ('trajanje', models.PositiveIntegerField(help_text='Trajanje u minutama')),
                ('potrosene_kalorije', models.FloatField()),
                ('datum', models.DateField()),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vjezbe', to='main.korisnickiprofil')),
            ],
        ),
    ]
