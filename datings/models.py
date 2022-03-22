from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    avatar = models.ImageField(null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name