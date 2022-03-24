from django.db import models


class Participant(models.Model):
    username = models.CharField(max_length=20, default='#ilgimdar')
    password = models.CharField(max_length=20, default='#123')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50)
    avatar = models.ImageField(null=True)
    gender = models.CharField(max_length=10)
    likes = models.JSONField(null=True, default={"-1": 1})

    def __str__(self):
        return self.name
