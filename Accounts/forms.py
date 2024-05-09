from django.forms import DateTimeInput, ModelForm
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def validate_mobile_number(value):
    allowed_chars = set("0123456789+")
    if not set(value).issubset(allowed_chars):
        raise ValidationError("Nedovolené znaky v telefoním čísle.")
def validate_psc_number(value):
    allowed_chars = set("0123456789 ")
    if not set(value).issubset(allowed_chars):
        raise ValidationError("nesprávné znaky v PSC")
def validate_alpha_characters(value):
    regex_pattern = r'^[a-zA-ZěščřžýáíéťďňúůüĚŠČŘŽÝÁÍÉŤĎŇÚŮÜ ,.\-\']+?$'

    # Kontrola řetězce pomocí regulárního výrazu
    if re.match(regex_pattern, value):
        print("ok")
    else:
        raise ValidationError('Názvy měst mohou obsahovat pouze písmena české abecedy, mezery následující (,),(-),(.)')


class NewMemeberForm(ModelForm):
    class Meta:
        model = member
        fields = ['jmeno', 'surname', 'birthday','GDPR', 'healthProblems']
        labels={
            "jmeno": ('Jméno:'),
            "surname": ('Příjmení:'),
            "birthday":('Datum narození '),
            "GDPR": ('Souhlasím s tím, aby byly pořizovány a uchovávány fotografie a osobní údaje člena.'),
            "healthProblems": ('Zdravotní problémy a jiná důležitá omezení:'),
        }
        widgets={
            "jmeno": forms.TextInput(attrs={'class':'form-control form-control-lg','pattern': '^[A-Za-zÀ-ÖØ-öø-ÿĀ-žſ]+$'}),
            "surname": forms.TextInput(attrs={'class':'form-control form-control-lg','pattern': '^[A-Za-zÀ-ÖØ-öø-ÿĀ-žſ]+$'}),
            "birthday": forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            "GDPR": forms.CheckboxInput(attrs={'class':'form-check-input','id':'checkbox'}),
            "healthProblems": forms.Textarea(attrs= {"class":"form-control", "id":"exampleFormControlTextarea1","rows":"3"}),
        }
class NewAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['user','mobile1', 'addres1', 'city1', 'psc1','mobile2']
        labels={
            "user":(""),
            "mobile1": ('Telefon na rodiče nebo zákonného zástupce'),
            "addres1": ('Adresa bydliště'),
            "city1": ('Město'),
            "psc1": ('PSČ'),
            "mobile2":('Telefon na druhého rodiče nebo jiného člena rodiny')
        }
        widgets={
            "user": forms.TextInput(attrs= {'class':'form-control','readonly':'readonly'}),
            "mobile1": forms.TextInput(attrs={'class':'form-control'}),
            "addres1": forms.TextInput(attrs={'class':'form-control'}),
            "city1": forms.TextInput(attrs= {'class': 'form-control'}),
            "psc1": forms.TextInput(attrs= {'class': 'form-control'}),
            "mobile2":forms.TextInput(attrs= {'class': 'form-control'})
        }
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields=["username","password1","password2"]
        widgets={
            "username": forms.TextInput(),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }
        labels={
            "username": ('Emailová adresa'),
            "password1": ("Heslo"),
            "password2": ('Potvrzení hesla'),
        }
        help_texts = {
            "password1": "Heslo musí být 8 znaků dlouhé. Nesmí obsahovat pouze čísla nebo být seznamu snadno prolomitelných hesel.",
        }
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    
class AddUserForm(forms.Form):
    newUserEmail = forms.EmailField(
        label="Email, kterému chcete umožnit přístup.",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control mb-8'})
    )
class SetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Potvrzení hesla",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

class changeDataForm(forms.Form):
    mobile1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_mobile_number]
        )
    addres1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    city1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_alpha_characters]
        )
    psc1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_psc_number]
        )
    state1 = forms.ChoiceField(
        choices=(
            ('', 'Vyberte'),
            ('Česko', 'Česko'),
            ('Slovensko', 'Slovensko'),
            ('Německo', 'Německo'),
            ('Polsko', 'Polsko'),
            ('jiné', 'jiné'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    mobile2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_mobile_number]
        )
    addres2= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
        )
    city2= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        #validators=[validate_alpha_characters],
        required=False
        )
    psc2= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_psc_number],
        required=False
        )
    state2 = forms.ChoiceField(
        choices=(
            ('', 'Vyberte'),
            ('Česko', 'Česko'),
            ('Slovensko', 'Slovensko'),
            ('Německo', 'Německo'),
            ('Polsko', 'Polsko'),
            ('jiné', 'jiné'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Vyberte soubor',widget=forms.FileInput(attrs={'class': 'form-control','id':"fileInput"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nastavíme enctype na multipart/form-data
        self.fields['file'].widget.attrs.update({'enctype': 'multipart/form-data'})