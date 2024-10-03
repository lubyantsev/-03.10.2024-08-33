from django.db import models

class Schedule(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Event(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='events', on_delete=models.CASCADE)
    time = models.DateTimeField()
    place = models.CharField(max_length=100)
    participant_name = models.CharField(max_length=100)