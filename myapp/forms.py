from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from .models import User_App, Client, Partenaire,Domaine
from django.db import transaction

from .models import  Entrepot,Produit
class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
class EntrepotForm(ModelForm):
    class Meta:
        model = Entrepot
        fields = ['nom','Telephone','Address','localisation']

class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields ="__all__"


class DomaineForm(ModelForm):
    class Meta:
        model = Domaine
        fields ="__all__"


class ClientSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placholder": "enter username",
    }), label="Username")
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placholder": "enter password",
    }), label="Password")
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placholder": "re-enter password",
    }), label="Confirm Password")
    nom = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placholder": "enter nom",
    }), label="Nom")
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placholder": "enter prenom",
    }), label="Prenom")
    telephone = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placholder": "enter telephone",
    }), label="Telephone")
    NNI = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placholder": "enter NNI",
    }), label="NNI")

    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    telephone = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User_App

    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.nom = self.cleaned_data.get('nom')
        user.prenom = self.cleaned_data.get('prenom')
        user.telephone = self.cleaned_data.get('telephone')
        user.save()
        client = Client.objects.create(user=user)
        client.save()
        return user


# --------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------#
class PartenaireSignUpForm(UserCreationForm):
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    NNI = forms.CharField(required=True)
    telephone = forms.CharField(required=True)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User_App

    def save(self):
        user = super().save(commit=False)
        user.is_partenaire = True
        user.nom = self.cleaned_data.get('nom')
        user.prenom = self.cleaned_data.get('prenom')
        user.telephone = self.cleaned_data.get('telephone')
        user.save()
        partenaire = Partenaire.objects.create(user=user, NNI=self.cleaned_data.get('NNI'),
                                               photo=self.cleaned_data.get('photo'))
        partenaire.save()
        return user