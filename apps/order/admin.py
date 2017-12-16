from django.contrib import admin
from apps.order.models import Tickets,Person

# Register your models here.

admin.site.register(Tickets)
admin.site.register(Person)