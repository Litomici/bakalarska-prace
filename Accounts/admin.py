from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Account)
admin.site.register(member)
admin.site.register(payment)
admin.site.register(EmailConfirmation)