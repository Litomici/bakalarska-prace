from django.forms import DateTimeInput, ModelForm
from django import forms
from .models import Event

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['organizedBy','event_type','name', 'destination', 'meeting', 'ending', 'departure', 'arrival', 'notes','capacity','travel','price','description']
        labels={
            "event_type":('Typ akce'),
            "name": ('Název Události'),
            "destination": ('Cíl cesty/Místo konání'),
            "meeting": ('Datum a čas srazu'),
            "ending": ('Datum a čas příjezdu'),
            "departure": ('Místo srazu'),
            "arrival": ('Místo ukončení'),
            "notes": ('Co s sebou?'),
            "capacity": ("Maximální počet účastníků"),
            "price":("Celková cena/Vstupné"),
            "description":("Detailnější popis akce a její průběh"),
            "travel":("Vlastní doprava")
        }
        widgets={
            "organizedBy":forms.TextInput(attrs= {'class':'form-control','readonly':'readonly'}),
            'event_type': forms.Select(attrs={'class':'form-control'}, choices=Event.EVENT_TYPES),
            "name": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "destination": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "meeting": DateTimeInput(attrs={'class':'form-control','type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            'ending': DateTimeInput(attrs={'class':'form-control','type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            "departure": forms.TextInput(attrs={'class':'form-control'}),
            "arrival": forms.TextInput(attrs= {'class':'form-control'}),
            "notes": forms.Textarea(attrs= {"class":"form-control","rows":"3"}),
            "capacity": forms.NumberInput(attrs={'class': 'form-control','value':30, 'min': 0, 'max': 100}),
            "price": forms.NumberInput(attrs={'class': 'form-control','value':0, 'min': 0, 'max':100000}),
            "description": forms.Textarea(attrs= {"class":"form-control","rows":"3"}),
            "travel":forms.CheckboxInput(attrs={'class':'form-check-input','id':'checkbox'}),
        }

class EventEditForm(ModelForm):
    eventId = forms.CharField(widget=forms.TextInput(attrs={'id': 'eventId', "class":"invis"}))
    class Meta:
        model = Event
        fields = ('organizedBy','eventId','event_type','name', 'destination', 'meeting', 'ending', 'departure', 'arrival', 'notes','capacity','travel','price','description')
        labels={
            "event_type":('Typ akce'),
            "name": ('Název Události'),
            "destination": ('Cíl cesty/Místo konání'),
            "meeting": ('Datum a čas srazu'),
            "ending": ('Datum a čas příjezdu'),
            "departure": ('Místo srazu'),
            "arrival": ('Místo ukončení'),
            "notes": ('Co s sebou?'),
            "capacity": ("Maximální počet účastníků"),
            "price":("Celková cena/Vstupné"),
            "description":("Detailnější popis akce a její průběh"),
            "travel":("Vlastní doprava")
        }
        widgets={
            'organizedBy':forms.TextInput(attrs={'class':'form-control'}),
            'event_type': forms.Select(attrs={'class':'form-control',}, choices=Event.EVENT_TYPES),
            "name": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "destination": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "meeting": DateTimeInput(attrs={'class':'form-control','type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            'ending': DateTimeInput(attrs={'class':'form-control','type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            "departure": forms.TextInput(attrs={'class':'form-control'}),
            "arrival": forms.TextInput(attrs= {'class':'form-control'}),
            "notes": forms.Textarea(attrs= {"class":"form-control","rows":"3"}),
            "capacity": forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max':100000}),
            "description": forms.Textarea(attrs= {"class":"form-control","rows":"3"}),
            "travel":forms.CheckboxInput(attrs={'class':'form-check-input','id':'checkbox'}),
        }
class EventCancelForm(forms.Form):  # Use forms.Form instead of forms.ModelForm
    event_id = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True}),
        label="Event ID"
    )
    sendMail = forms.BooleanField(
        label='Ano, opravdu chci informavat všechny přihlášené o zrušení tété akce',
        initial=True,
        required=True,
        widget=forms.CheckboxInput(attrs={"class": ""})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
        label="Zpráva pro přihlášené: Akce se ruší z důvodu ...",
        required=True,
    )