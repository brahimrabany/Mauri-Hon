from django.db import models
from django.contrib.auth.models import AbstractUser


class User_App(AbstractUser):
    nom = models.CharField(max_length=30, null=True)
    prenom = models.CharField(max_length=30, null=True)
    telephone = models.IntegerField(null=True)
    is_partenaire = models.BooleanField('Is_partenaire', default=False)
    is_client = models.BooleanField('Is_client', default=False)


class Client(models.Model):
    user = models.OneToOneField(User_App, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.nom


class Partenaire(models.Model):
    user = models.OneToOneField(User_App, on_delete=models.CASCADE, primary_key=True, blank=True, default=False)
    NNI = models.IntegerField()
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.nom
class Message(models.Model):
    sender = models.ForeignKey(User_App, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User_App, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class Entrepot(models.Model):
    nom=models.CharField(max_length=50,unique=True)
    Telephone=models.IntegerField(null=True)
    Address = models.CharField(max_length =50 ,null=True)
    localisation=models.CharField(max_length=50 ,null=True)
    user = models.ForeignKey(User_App, on_delete = models.CASCADE, null=True,default=1)
    def __str__(self):
        return self.nom
class Produit(models.Model):
    nom = models.CharField(max_length=30)
    date_production = models.DateField(auto_now=True, auto_now_add=False)
    date_expire = models.DateField(auto_now=True, auto_now_add=False)
    prix = models.FloatField(max_length=40)
    quantite = models.IntegerField()
    image= models.ImageField(upload_to="images/")
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
    def get_entrepot(self):
        return self.entrepot.nom

class Notification(models.Model):
    sender   = models.ForeignKey(User_App,on_delete=models.CASCADE,null=True,blank=True,related_name='senderr', )
    receiver = models.ForeignKey(User_App, on_delete=models.CASCADE, null=True, blank=True,related_name='receiverr' ,  )
    sujet    = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    idProduit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True, blank=True )

    def get_produit(self):
        return self.produit.nom
    class Meta:
        ordering = ('timestamp',)


class Domaine(models.Model):
   domaine=models.CharField(max_length=50)
   image = models.ImageField(upload_to="images/",null=True, blank=True,)

   def __str__(self):
        return self.categorie

