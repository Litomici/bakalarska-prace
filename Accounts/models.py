from email.policy import default
from os import name
from re import T
from typing import Counter
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

class member(models.Model):
    jmeno=models.CharField(max_length=30, default="john")
    surname=models.CharField(max_length=40, default="Smith")
    birthday = models.DateField(default=now())
    ATOM_id=models.CharField(max_length=18, blank=True)
    GDPR=models.BooleanField(default=True)
    healthProblems=models.CharField(max_length=500,default="Dítě nemá žádná zdravotní omezení ani speciální požadavky na stravu či zacházení")
    objects = models.Manager()
    def __str__(self):
            return self.jmeno +" "+ self.surname

class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='access_users',default=[user])
    addres1=models.CharField(default="",max_length=255)
    city1=models.CharField(default="",max_length=100)
    psc1=models.CharField(default="",max_length=15)
    mobile1=models.CharField(max_length=13, default="")
    addres2=models.CharField(default="",max_length=255, blank=True)
    city2=models.CharField(default="",max_length=100, blank=True)
    psc2=models.CharField(default="", max_length=15, blank=True)
    mobile2=models.CharField(max_length=13, default="")
    wallet=models.FloatField(default=(0.0))
    position=models.IntegerField(default=0)
    member=models.ManyToManyField(member, related_name=("member"), blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.user.__str__()


class EmailConfirmation(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, email,sender):
        token = sender+"=>"+get_random_string(length=16)
        return cls.objects.create(email=email, token=token)

    def send_confirmation_email(self):
        subject = 'Registrace do systému Litomíků'
        message = render_to_string('confirmation_email.txt', {'token': self.token})
        from_email = 'turistakLitomici@gmail.com'
        send_mail(subject, message, from_email, [self.email])
        
class payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)
    payed_date = models.DateField(null=True, blank=True)
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    payment_from = models.CharField(max_length=35,blank=True, default="neznámý účet")
    transaction_number = models.CharField(max_length=30,null=True,blank=True)
    var_symbol=models.CharField(max_length=10,blank=True,null=True)
    payed_in_cash=models.BooleanField(default=True)
    objects = models.Manager()
    def __str__(self):
        return f"Platba {self.amount} od {self.account}"
