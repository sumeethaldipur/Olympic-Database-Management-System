
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings


class Country(models.Model):
    #country_id = models.IntegerField(primary_key=True)
    abbr = models.CharField(max_length=3)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Athlete(models.Model):
    #athlete_id = models.IntegerField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country")
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1)
    dob = models.DateField(null=True)
    age = models.IntegerField(null=True)
    #events = models.ManyToManyField(Event, through='Participation')
    #events = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    #events = models.ForeignKey(Event, on_delete=models.CASCADE)
    #def is_valid_athlete(self):
        #return (condition1) and (condition2)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name+' '+self.last_name


class Event(models.Model):
    #event_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    stadium = models.CharField(max_length=64)
    area = models.CharField(max_length=64)
    athletes = models.ManyToManyField(Athlete, through='Participation', related_name='athlete_list')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    #athletes = models.ForeignKey(Athlete, on_delete=models.CASCADE,null=True)
    important = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Imp', related_name='important_events')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    event_at = models.DateTimeField(null=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.name

class Participation(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

class Citizenship(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if len(self.text) < 15 : return self.text


class Imp(models.Model) :
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.event.name[:10])
