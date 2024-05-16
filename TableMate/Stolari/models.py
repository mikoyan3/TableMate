from django.db import models
from django.shortcuts import get_object_or_404


# Create your models here.

class Admin(models.Model):
    idadmin = models.AutoField(db_column='IdAdmin', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=40)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Galerija(models.Model):
    idslika = models.AutoField(db_column='IdSlika', primary_key=True)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=255)  # Field name made lowercase.
    tipslike = models.CharField(db_column='TipSlike', max_length=1)  # Field name made lowercase.
    idobj = models.IntegerField(db_column='IdObj', blank=True, null=True)  # Field name made lowercase.
    idvest = models.IntegerField(db_column='IdVest', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'galerija'


class Iznajmljivanje(models.Model):
    idizn = models.AutoField(db_column='IdIzn', primary_key=True)  # Field name made lowercase.
    datumpocetak = models.DateTimeField(db_column='DatumPocetak')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=40)  # Field name made lowercase.
    datumkraj = models.DateTimeField(db_column='DatumKraj')
    idobj = models.IntegerField(db_column='IdObj')  # Field name made lowercase.
    idrreg = models.IntegerField(db_column='IdrReg')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'iznajmljivanje'




class Menadzer(models.Model):
    idmen = models.AutoField(db_column='IdMen', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=40)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=40)  # Field name made lowercase.
    ime = models.CharField(db_column='Ime', max_length=40)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=40)  # Field name made lowercase.
    pol = models.CharField(db_column='Pol', max_length=40)  # Field name made lowercase.
    broj = models.CharField(db_column='Broj', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'menadzer'


class Objekat(models.Model):
    idobj = models.AutoField(db_column='IdObj', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', max_length=40)  # Field name made lowercase.
    adresa = models.CharField(db_column='Adresa', max_length=40)  # Field name made lowercase.
    grad = models.CharField(db_column='Grad', max_length=40)  # Field name made lowercase.
    tipobj = models.CharField(db_column='TipObj', max_length=40)  # Field name made lowercase.
    tipkuhinje = models.CharField(db_column='TipKuhinje', max_length=40)  # Field name made lowercase.
    ukocena = models.IntegerField(db_column='UkOcena')  # Field name made lowercase.
    brocena = models.IntegerField(db_column='BrOcena')  # Field name made lowercase.
    opis = models.CharField(db_column='Opis', max_length=1000) #Field name made lowercas
    idmen = models.IntegerField(db_column='IdMen')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'objekat'
    def getAvgOcena(self): #dohvatanje srednje ocene
        if self.brocena!=0:
            srednja = self.ukocena/self.brocena
            zaokruzena = round(srednja, 2)
        else:
            zaokruzena = 0
        return zaokruzena
    def getMojaSlikaObjekat(self): #dohvatanje slike koja se ugradjuje u stranicu objekta
        slika = Galerija.objects.filter(idobj=self.idobj, tipslike='O').last()
        if slika is not None:
            return slika.path
        return 0

    def getMojaSlikaCard(self): #dohvatanje slike koja se ugradjuje u karticu objekta
        slika = Galerija.objects.filter(idobj=self.idobj, tipslike='k').last()
        if slika is not None:
            return slika.path
        return 0

    def getMojaSlikaMenu(self): #dohvatanje menija objekta
        slika = Galerija.objects.filter(idobj=self.idobj, tipslike='M').last()
        if slika is not None:
            return slika.path
        return 0

    def getBrojRezervacijaZaMojObjekat(self):
        stoloviUObjektu = Sto.objects.filter(idobj=self.idobj)
        brStolova = stoloviUObjektu.count()
        idStolova = stoloviUObjektu.values_list('idsto', flat=True).distinct()
        rezervacijeZaMojeStolove = Rezervacija.objects.filter(idsto__in=idStolova)
        iznajmljivanjaZaMojObjekat = Iznajmljivanje.objects.filter(idobj=self.idobj)
        brIznajmljivanja = iznajmljivanjaZaMojObjekat.count()
        sveUkupno = brIznajmljivanja*brStolova + rezervacijeZaMojeStolove.count()
        return sveUkupno



class Omiljeni(models.Model):
    idrreg = models.IntegerField(db_column='IdrReg', primary_key=True)
    idobj = models.IntegerField(db_column='IdObj')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'omiljeni'
        unique_together = (('idrreg', 'idobj'),)


class Registrovani(models.Model):
    idrreg = models.AutoField(db_column='IdrReg', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=40)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=64)  # Field name made lowercase.
    ime = models.CharField(db_column='Ime', max_length=40)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=40)  # Field name made lowercase.
    brtelefona = models.CharField(db_column='BrTelefona', max_length=40)  # Field name made lowercase.
    pol = models.CharField(db_column='Pol', max_length=40)  # Field name made lowercase.
    pozpoeni = models.IntegerField(db_column='PozPoeni')  # Field name made lowercase.
    negpoeni = models.IntegerField(db_column='NegPoeni')  # Field name made lowercase.
    datumrodjenja = models.DateTimeField(db_column='DatumRodjenja')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registrovani'

    def dovoljnoPoena(self):
        stanjePoena = self.pozpoeni - self.negpoeni
        if stanjePoena >= 10:
            return 1
        return 0


class Rezervacija(models.Model):
    idrez = models.AutoField(db_column='IdRez', primary_key=True)  # Field name made lowercase.
    datumpocetak = models.DateTimeField(db_column='DatumPocetak')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=40)  # Field name made lowercase.
    datumkraj = models.DateTimeField(db_column='DatumKraj')
    idsto = models.IntegerField(db_column='IdSto')  # Field name made lowercase.
    idrreg = models.IntegerField(db_column='IdrReg')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rezervacija'

    def dohImeRegistrovanog(self): #dohvatanje imena registrovanog koji je napravio rezervaciju
        korisnik = get_object_or_404(Registrovani, idrreg=self.idrreg)
        if korisnik is not None:
            return korisnik.ime
        return 0

    def dohPrezimeRegistrovanog(self): #dohvatanje prezimena registrovanog koji je napravio rezervaciju
        korisnik = get_object_or_404(Registrovani, idrreg=self.idrreg)
        if korisnik is not None:
            return korisnik.prezime
        return 0

class Sto(models.Model):
    idsto = models.AutoField(db_column='IdSto', primary_key=True)  # Field name made lowercase.
    idobj = models.IntegerField(db_column='IdObj')  # Field name made lowercase.
    idtip = models.IntegerField(db_column='IdTip')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sto'

    def dohTip(self): #dohvatanje tipa stola
        tip = get_object_or_404(Tip, idtip=self.idtip)
        if tip is not None:
            return tip.naziv
        return 0
class Tip(models.Model):
    idtip = models.AutoField(db_column='IdTip', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', max_length=40)  # Field name made lowercase.
    opis = models.CharField(db_column='Opis', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tip'


class Vest(models.Model):
    idvest = models.AutoField(db_column='IdVest', primary_key=True)  # Field name made lowercase.
    naslov = models.CharField(db_column='Naslov', max_length=40)  # Field name made lowercase.
    tekst = models.CharField(db_column='Tekst', max_length=255)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'vest'

    def getMojaSlika(self): #dohvatanje slike za datu vest
        slika = Galerija.objects.filter(idvest=self.idvest, tipslike='v').last()
        if slika is not None:
            return slika.path
        return 0
