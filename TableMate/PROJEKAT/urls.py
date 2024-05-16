"""
URL configuration for PROJEKAT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import Stolari.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Stolari.views.login, name='login'),
    path('logout/', Stolari.views.logout_view, name='logout'),
    path('register.html', Stolari.views.register_render, name='register_render'),
    path('register/', Stolari.views.register, name='register'),
    path('pregledKorisnika/', Stolari.views.pregledKorisnika, name='pregledKorisnika'),
    path('korisnik/<int:idrreg>', Stolari.views.obrisiKorisnika, name='obrisiKorisnika'),
    path('prikazVesti/', Stolari.views.prikazVesti, name='prikazVesti'),
    path('formaDodajVesti/', Stolari.views.formaDodajVesti, name='formaDodajVesti'),
    path('dodajVesti/', Stolari.views.dodajVesti, name='dodajVesti'),
    path('prikaziOdgovarajuciSeeMore/<int:idobj>/', Stolari.views.prikaziOdgovarajuciSeeMore, name='prikaziOdgovarajuciSeeMore'),
    path('prikaziExplore/', Stolari.views.prikaziExplore, name='prikaziExplore'),
    path('pregledRezervacijaIIznajmljivanja/', Stolari.views.pregledRezervacijaIIznajmljivanja, name='pregledRezervacijaIIznajmljivanja'),
    path('dodajOmiljeni/<int:idobj>/', Stolari.views.dodajOmiljeni, name='dodajOmiljeni'),
    path('obrisiOmiljeni/<int:idobj>/', Stolari.views.obrisiOmiljeni, name='obrisiOmiljeni'),
    path('reserveTable/<int:idobj>/', Stolari.views.reserveTable, name='reserveTable'),
    path('viewFreeTables/<int:idobj>/', Stolari.views.viewFreeTables, name='viewFreeTables'),
    path('rezervisi_sto/<str:start_time>/<str:end_time>/', Stolari.views.rezervisiSto, name='rezervisiSto'),
    path('reservePlace/<int:idobj>/', Stolari.views.reservePlace, name='reservePlace'),
    path('iznajmi/<int:idobj>/', Stolari.views.iznajmi, name='iznajmi'),
    path('prikaziPoGradu/<str:grad>', Stolari.views.prikaziPoGradu, name='prikaziPoGradu'),
    path('prikaziPoKuhinji/<str:kuhinja>', Stolari.views.prikaziPoKuhinji, name='prikaziPoKuhinji'),
    path('prikaziPabove', Stolari.views.prikaziPabove, name='prikaziPabove'),
    path('prikaziRestorane', Stolari.views.prikaziRestorane, name='prikaziRestorane'),
    path('prikaziKlubove', Stolari.views.prikaziKlubove, name='prikaziKlubove'),
    path('prikaziPoReviews', Stolari.views.prikaziPoReviews, name='prikaziPoReviews'),
    path('prikaziOdgovarajucuVest/<int:idvest>/', Stolari.views.prikaziOdgovarajucuVest, name='prikaziOdgovarajucuVest'),
    path('prikaziPoPopularnosti', Stolari.views.prikaziPoPopularnosti, name='prikaziPoPopularnosti'),
    path('prikazProfila', Stolari.views.prikazProfila, name='prikazProfila'),
    path('ostvariPopust', Stolari.views.ostvariPopust, name='ostvariPopust'),
    path('prikaziOmiljene', Stolari.views.prikaziOmiljene, name='prikaziOmiljene'),
    path('markirajPozitivno/<int:idrreg>/<int:idrez>/', Stolari.views.markirajPozitivno, name='markirajPozitivno'),
    path('markirajNegativno/<int:idrreg>/<int:idrez>/', Stolari.views.markirajNegativno, name='markirajNegativno'),
    path('flushSession', Stolari.views.flushSession, name='flushSession'),
]
