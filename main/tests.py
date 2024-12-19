from django.test import TestCase, Client
from django.urls import reverse, resolve
from main.views import FitnessCiljListView
from main.models import FitnessCilj, KorisnickiProfil
from django.contrib.auth.models import User

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.ciljevi_url = reverse('cilj-list')
        
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        self.profil = KorisnickiProfil.objects.create(
            korisnik=self.user,
            godine=25,
            visina=180,
            tezina=80
        )
        
    def test_ciljevi_url_resolves(self):
        url = reverse('cilj-list')
        self.assertEquals(resolve(url).func.view_class, FitnessCiljListView)
        
    def test_ciljevi_list_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.ciljevi_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/fitness_cilj_list.html')