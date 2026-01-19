from django.contrib import admin
from events.models import Country, Athlete, Event, Participation

# Register your models here.

admin.site.register(Country)
admin.site.register(Athlete)
admin.site.register(Event)
admin.site.register(Participation)
