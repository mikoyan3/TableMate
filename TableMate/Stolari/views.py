import random

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, Menadzer, Registrovani, Galerija, Vest, Objekat, Sto, Rezervacija, Omiljeni, Iznajmljivanje
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
import hashlib


def login(request): #login logika - Pavle Perovic
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if Admin.objects.filter(username=username, password=password).exists() or Admin.objects.filter(username=username, password=hashed_password).exists():
            request.session['username'] = username
            return render(request, 'admin.html')
        elif Menadzer.objects.filter(username=username, password=password).exists() or Menadzer.objects.filter(username=username, password=hashed_password).exists():
            request.session['username'] = username
            return render(request, 'menadzer.html')
        elif Registrovani.objects.filter(username=username, password=password).exists() or Registrovani.objects.filter(username=username, password=hashed_password).exists():
            request.session['username'] = username
            return render(request, 'userIndex.html')
        else:
            poruka = "Pogresan username ili password"
            return render(request, 'login.html', {'poruka': poruka, 'template_name': 'login.html'})
    else:
        return render(request, 'login.html', {'template_name': 'login.html'})

def logout_view(request): #logout logika - Pavle Perovic
    logout(request) #logout radi i flush i modified = true
    return redirect('login') #skoci na pocetnu stranu

def register_render(request): #hendler za redirect - Pavle Perovic
    return render(request, 'register.html')

def register(request): #registracija korisnika - Pavle Perovic
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        number = request.POST.get('number')
        gender = request.POST.get('gender')
        datetime = request.POST.get('datetime')

        if username is None or password is None or first_name is None or last_name is None or number is None or gender is None or datetime is None:
            error = 'Neispravan unos!'
            return render(request, 'register.html', {'error': error})
        if username.strip() == '' or password.strip() == '' or first_name.strip() == '' or last_name.strip() == '' or number.strip() == '' or gender.strip() == '' or datetime.strip() == '':
            error = 'Sva polja moraju biti popunjena!'
            return render(request, 'register.html', {'error': error})

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        #Obrada unique podataka.
        if Registrovani.objects.filter(username=username).exists():
            error = 'Username vec postoji!'
            return render(request, 'register.html', {'error': error})
        if Registrovani.objects.filter(brtelefona=number).exists():
            error = 'Broj telefona vec postoji!'
            return render(request, 'register.html', {'error': error})

        # Insert
        user = Registrovani(username=username, password=hashed_password, ime=first_name, prezime=last_name, brtelefona=number, pol=gender, datumrodjenja=datetime, pozpoeni=0, negpoeni=0)
        user.save()

        # Redirektujemo se na pocetnu stranicu
        return redirect('login')

    # ako metoda nije POST
    error = 'Metoda nije POST!'
    return render(request, 'register.html', {'error': error})


def pregledKorisnika(request): #popunjavanje tabele kod pregleda korisnika koji radi administrator - Pavle Perovic
    korisnici = Registrovani.objects.all()
    context = {'korisnici': korisnici}
    return render(request, 'pregledKorisnika.html', context)

def registerRender(request): #Pavle Perovic
    return render(request, 'register.html')

def obrisiKorisnika(request, idrreg): #brisanje korisnika iz baze - Pavle Perovic
    korisnik = get_object_or_404(Registrovani, idrreg=idrreg)
    korisnik.delete()
    return redirect('pregledKorisnika')

def prikazVesti(request): #prikaz vesti samo za testiranje trenutno - Pavle Perovic
    vesti = Vest.objects.all()
    context = {'vesti': vesti}
    return render(request, 'prikazVesti.html', context)

def prikaziOdgovarajucuVest(request, idvest): #prikaz stranice za kliknutu vest - Pavle Perovic
    vest = get_object_or_404(Vest, idvest=idvest)
    context = {'vest': vest}
    return render(request, 'stranicaVest.html', context)

def formaDodajVesti(request): #pomocna za otvaranje stranice sa formom za dodavanje vesti - Pavle Perovic
    return render(request, 'FormaDodajVesti.html')

def dodajVesti(request): #Dodavanje vesti funkcionalnost - Pavle Perovic
    error = ''
    if request.method == 'POST':
        naslov = request.POST.get('naslov')
        tekst = request.POST.get('tekst')
        path = request.POST.get('path')
    if naslov is None or tekst is None or path is None:
        error = 'Neispravan unos!'
        return render(request, 'FormaDodajVesti.html', {'error': error})
    if naslov.strip() == '' or tekst.strip() == '' or path.strip() == '':
        error = 'Sva polja moraju biti popunjena!'
        return render(request, 'FormaDodajVesti.html', {'error': error})
    if Vest.objects.filter(naslov=naslov).exists():
        error = 'Vec postoji naslov za ovu vest!'
        return render(request, 'FormaDodajVesti.html', {'error': error})
    vest = Vest(naslov=naslov, tekst=tekst)
    vest.save()
    slika = Galerija(path=path, tipslike='v', idvest=vest.idvest)
    slika.save()
    return render(request, 'admin.html')
    # ako metoda nije POST
    error = 'Metoda nije POST!'
    return render(request, 'register.html', {'error': error})

def flushSession(request):
    request.session.flush()
    return redirect('prikaziExplore')

def prikaziExplore(request): #prikazivanje explore stranice
    objekti = Objekat.objects.all()
    gradovi = objekti.values_list('grad', flat=True).distinct()
    kuhinje = objekti.values_list('tipkuhinje', flat=True).distinct()
    usr = request.session.get('username')
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziOdgovarajuciSeeMore(request, idobj): #See more dugme na kartici
    prosledi = 3
    if 'username' in request.session:
        username = request.session.get('username')
        korisnik = get_object_or_404(Registrovani, username=username)
        omiljeni = Omiljeni.objects.filter(idrreg=korisnik.idrreg, idobj=idobj)
        if omiljeni.exists():
            prosledi = 0
        else:
            prosledi = 1
    objekat = get_object_or_404(Objekat, idobj=idobj)
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekat': objekat,
               'prosledi': prosledi,
               'logged_in': logged_in}
    return render(request, 'templateStranicaObjekta.html', context)

def pregledRezervacijaIIznajmljivanja(request): #prikazivanje rezervacija na stranici menadzera
    username = request.session.get('username')
    menadzer = get_object_or_404(Menadzer, username=username)
    objekti = Objekat.objects.filter(idmen=menadzer.idmen)
    stolovi = Sto.objects.filter(idobj__in=list(objekti.values_list('idobj', flat=True)))
    sveRezervacije = Rezervacija.objects.filter(idsto__in=list(stolovi.values_list('idsto', flat=True)))
    unmarkedRezervacije = Rezervacija.objects.filter(status='unmarked')
    idUnmarked = unmarkedRezervacije.values_list('idrez', flat=True)
    rezervacije = sveRezervacije.filter(idrez__in=idUnmarked)
    context = {'rezervacije': rezervacije}
    return render(request, 'menadzerPregledRezervacija.html', context)

def dodajOmiljeni(request, idobj): #dodavanje u listu omiljenih
    username = request.session.get('username')
    user = Registrovani.objects.get(username=username)
    omiljeni = Omiljeni.objects.create(idrreg=user.idrreg, idobj=idobj)
    objekat = get_object_or_404(Objekat, idobj=idobj)
    prosledi = 0
    context = {'objekat': objekat,
               'prosledi': prosledi}
    return render(request, 'templateStranicaObjekta.html', context)

def obrisiOmiljeni(request, idobj): #brisanje iz liste omiljenih
    username = request.session.get('username')
    user = Registrovani.objects.get(username=username)
    omiljeni = Omiljeni.objects.filter(idrreg=user.idrreg, idobj=idobj).delete()
    objekat = get_object_or_404(Objekat, idobj=idobj)
    prosledi = 1
    context = {'objekat': objekat,
               'prosledi': prosledi}
    return render(request, 'templateStranicaObjekta.html', context)

def reserveTable(request, idobj): #kada se stisne na dugme reserve table salje se na stranicu sa formom za biranje datuma i trajanja rezervacije
    objekat = get_object_or_404(Objekat, idobj=idobj)
    context = {'objekat': objekat}
    return render(request, 'rezervacijaStola.html', context)

def viewFreeTables(request, idobj): #kada se izabere datum i trajanje rezervacije dolazi se na novu stranicu koja prikazuje sliku rasporeda stolova i slobodnih stolova za rezervisanje
    error = ''
    if request.method == 'POST':
        objekat = get_object_or_404(Objekat, idobj=idobj)
        datumPocetak = request.POST.get('date')
        trajanje = request.POST.get('trajanje')
        start_time = timezone.make_aware(datetime.strptime(datumPocetak, "%Y-%m-%dT%H:%M"))
        if start_time < timezone.now():
            error = 'Trazeno vreme rezervacije je u proslosti'
            context = {'objekat': objekat,
                       'error': error}
            return render(request, 'rezervacijaStola.html', context)
        end_time = start_time + timedelta(hours=int(trajanje))
        #PROVERA DA LI JE OBJEKAT IZNAJMLJEN U OVO VREME
        iznajmljivanja = Iznajmljivanje.objects.filter(
            Q(datumpocetak__lte=start_time, datumkraj__gt=start_time) |
            Q(datumpocetak__lt=end_time, datumkraj__gte=end_time) |
            Q(datumpocetak__gte=start_time, datumkraj__lte=end_time),
            idobj=idobj
        )
        if iznajmljivanja.exists():
            error = 'Objekat je iznajmljen u ovo vreme'
            context = {'objekat': objekat,
                       'error': error}
            return render(request, 'rezervacijaStola.html', context)
        #FILTRIRANJE SLOBODNIH STOLOVA
        rezervacijeKojeSePreklapaju = Rezervacija.objects.filter(
                                            Q(datumpocetak__lte=start_time, datumkraj__gt=start_time) |
                                            Q(datumpocetak__lt=end_time, datumkraj__gte=end_time) |
                                            Q(datumpocetak__gte=start_time, datumkraj__lte=end_time)
        )
        idStoPreklapaju = rezervacijeKojeSePreklapaju.values_list('idsto', flat=True)
        stoloviUObjektu = Sto.objects.filter(idobj=idobj)
        stolovi = stoloviUObjektu.exclude(idsto__in=idStoPreklapaju)
        dostupniStolovi = Sto.objects.filter(idsto__in=stolovi)
        context = {'dostupniStolovi': dostupniStolovi,
                   'start_time': start_time,
                   'end_time': end_time}
        return render(request, 'prikazStolova.html', context)


def rezervisiSto(request, start_time, end_time): #funkcionalnost rezervisanja stola, moze da se prosledjuje vise argumenata view-u, ne mora samo jedan
    if request.method == 'POST':
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        selected_sto = request.POST.get('stolovi')
        username = request.session.get('username')
        korisnik = get_object_or_404(Registrovani, username=username)
        idkor = korisnik.idrreg
        rez = Rezervacija(datumpocetak=start_time, status='unmarked', datumkraj=end_time, idsto=selected_sto, idrreg=idkor)
        rez.save()
        return HttpResponse("Uspesno rezervisano")

def reservePlace(request, idobj): #kada se klikne na reserve the whole place
    objekat = get_object_or_404(Objekat, idobj=idobj)
    context = {'objekat': objekat}
    return render(request, 'rezervacijaObjekta.html', context)

def iznajmi(request, idobj): #obrada forme i iznajmljivanje objekta
    error = ''
    if request.method == 'POST':
        objekat = get_object_or_404(Objekat, idobj=idobj)
        datumPocetak = request.POST.get('date')
        trajanje = request.POST.get('trajanje')
        start_time = timezone.make_aware(datetime.strptime(datumPocetak, "%Y-%m-%dT%H:%M"))
        if start_time < timezone.now():
            error = 'Trazeno vreme iznajmljivanja je u proslosti'
            context = {'objekat': objekat,
                       'error': error}
            return render(request, 'rezervacijaObjekta.html', context)
        end_time = start_time + timedelta(hours=int(trajanje))
        #PROVERA DA LI JE OBJEKAT IZNAJMLJEN U OVO VREME
        iznajmljivanja = Iznajmljivanje.objects.filter(
            Q(datumpocetak__lte=start_time, datumkraj__gt=start_time) |
            Q(datumpocetak__lt=end_time, datumkraj__gte=end_time) |
            Q(datumpocetak__gte=start_time, datumkraj__lte=end_time),
            idobj=idobj
        )
        if iznajmljivanja.exists():
            error = 'Objekat je iznajmljen u ovo vreme'
            context = {'objekat': objekat,
                       'error': error}
            return render(request, 'rezervacijaObjekta.html', context)
        #TRAZENJE DA LI POSTOJI REZERVISAN STO U TRAZENO VREME
        rezervacijeKojeSePreklapaju = Rezervacija.objects.filter(
                                            Q(datumpocetak__lte=start_time, datumkraj__gt=start_time) |
                                            Q(datumpocetak__lt=end_time, datumkraj__gte=end_time) |
                                            Q(datumpocetak__gte=start_time, datumkraj__lte=end_time)
        )
        idStoPreklapaju = rezervacijeKojeSePreklapaju.values_list('idsto', flat=True)
        stoloviUObjektu = Sto.objects.filter(idobj=idobj)
        postojeRezervacije = stoloviUObjektu.filter(idsto__in=idStoPreklapaju)
        if postojeRezervacije.exists():
            error = 'Postoje rezervacije u ovo vreme'
            context = {'objekat': objekat,
                       'error': error}
            return render(request, 'rezervacijaObjekta.html', context)

        # datumpocetak, status, datumkraj, idobj, idrreg
        username = request.session.get('username')
        korisnik = get_object_or_404(Registrovani, username=username)
        idkor = korisnik.idrreg
        izn = Iznajmljivanje(datumpocetak=start_time, status='unmarked', datumkraj=end_time, idobj=idobj, idrreg=idkor)
        izn.save()
        return HttpResponse("Uspesno iznajmljeno")

def prikaziPoGradu(request, grad): #filter po gradovima
    objekti = Objekat.objects.filter(grad=grad)
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziPoKuhinji(request, kuhinja): #filter po kuhinji
    objekti = Objekat.objects.filter(tipkuhinje=kuhinja)
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziPabove(request): #filter za pabove
    objekti = Objekat.objects.filter(tipobj='pab')
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziRestorane(request): #filter za restorane
    objekti = Objekat.objects.filter(tipobj='restoran')
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziKlubove(request): #filter za klubove
    objekti = Objekat.objects.filter(tipobj='klub')
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziPoReviews(request): #prikazi sortirano po oceni
    objekti = sorted(
        Objekat.objects.all(),
        key=lambda objekat: objekat.getAvgOcena(),
        reverse=True
    )
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikaziPoPopularnosti(request): #prikazi sortirano po popularnosti
    objekti = sorted(
        Objekat.objects.all(),
        key = lambda objekat: objekat.getBrojRezervacijaZaMojObjekat(),
        reverse=True
    )
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    if 'username' in request.session:
        logged_in = True
    else:
        logged_in = False
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje,
               'logged_in': logged_in}
    return render(request, 'templateExplore.html', context)

def prikazProfila(request): #prikaz userProfile stranice
    username = request.session.get('username')
    korisnik = get_object_or_404(Registrovani, username=username)
    popust=0
    context = {'korisnik': korisnik,
               'popust': popust}
    return render(request, 'userProfile.html', context)

def ostvariPopust(request): #ostvarivanje popusta funkcionalnost
    username = request.session.get('username')
    korisnik = get_object_or_404(Registrovani, username=username)
    korisnik.pozpoeni=0
    korisnik.negpoeni=0
    korisnik.save()
    popust = random.randint(10000, 99999)
    context = {'korisnik': korisnik,
               'popust': popust}
    return render(request, 'userProfile.html', context)

def prikaziOmiljene(request): #prikaz omiljenih objekata za datog korisnika
    username = request.session.get('username')
    korisnik = get_object_or_404(Registrovani, username=username)
    omiljeni = Omiljeni.objects.filter(idrreg=korisnik.idrreg)
    idOmiljenihObjekata = omiljeni.values_list('idobj', flat=True).distinct()
    objekti = Objekat.objects.filter(idobj__in=idOmiljenihObjekata)
    gradovi = Objekat.objects.values_list('grad', flat=True).distinct()
    kuhinje = Objekat.objects.values_list('tipkuhinje', flat=True).distinct()
    context = {'objekti': objekti,
               'gradovi': gradovi,
               'kuhinje': kuhinje}
    return render(request, 'templateExplore.html', context)

def markirajPozitivno(request, idrreg, idrez): #menadzer markira rezervaciju kao ostvarena
    korisnik = get_object_or_404(Registrovani, idrreg=idrreg)
    rezervacija = get_object_or_404(Rezervacija, idrez=idrez)
    rezervacija.status = 'ostvaren'
    rezervacija.save()
    poz = korisnik.pozpoeni
    poz = poz + 1
    korisnik.pozpoeni = poz
    korisnik.save()
    return redirect('pregledRezervacijaIIznajmljivanja')

def markirajNegativno(request, idrreg, idrez): #menadzer markira rezervaciju kao neostvarenu
    korisnik = get_object_or_404(Registrovani, idrreg=idrreg)
    rezervacija = get_object_or_404(Rezervacija, idrez=idrez)
    rezervacija.status = 'neostvaren'
    rezervacija.save()
    neg = korisnik.negpoeni
    neg = neg + 1
    korisnik.negpoeni = neg
    korisnik.save()
    return redirect('pregledRezervacijaIIznajmljivanja')

