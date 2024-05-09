from email.policy import default
from tokenize import blank_re
from unittest.util import _MAX_LENGTH
import uuid
from django.db import models
from Accounts.models import member

class Event(models.Model):
    EVENT_TYPES = [
        ('vylet', 'Výlet'),
        ('tabor_vyprava', 'Tábor/Výprava'),
        ('oddilovka', 'Oddílovka'),
        ('akce_pro_verejnost', 'Akce pro veřejnost'),
        ('jine', 'Jiné'),
    ]
    organizedBy=models.CharField(default="turistaklitomici@gmail.cz",max_length=100)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='vylet')#druh akce
    name=models.CharField(max_length=80)#jméno události
    destination=models.CharField(max_length=80)#cílová destinace
    meeting=models.DateTimeField()#den a čas odjezdu
    ending=models.DateTimeField(blank=True)# den a čas příjezdu
    departure=models.CharField(max_length=100)# místo odjezdu
    arrival=models.CharField(default="Včas upřesníme", max_length=100, blank=True)#místo příjezdu
    notes=models.CharField(default="Dobrou náladu", blank=True,max_length=500)# s sebou a poznámky
    assigned=models.ManyToManyField(member, related_name=("assigned"), blank=True)# přihlášení
    attendance=models.ManyToManyField(member, related_name=("attendance"), blank=True)# zúčastnění
    price=models.IntegerField(default=0)# cena za jednoho
    capacity=models.IntegerField(default=50,blank=True)#kolik se lidí se může zapsat
    description=models.CharField(blank=True,max_length=500,default=" ",)#bližší popis akce
    travel=models.BooleanField(blank=True,default=True)#způsob dopravy => společně/po vlastní ose
    objects = models.Manager()
    def __str__(self):
        return self.name +" ("+ self.destination+" "+self.event_type+")"