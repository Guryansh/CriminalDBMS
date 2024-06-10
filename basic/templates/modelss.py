# models.py
from django.db import models


class Profile(models.Model):
    folder_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, null=True)
    gender = models.BooleanField()
    dob = models.DateField()
    POB = models.CharField(max_length=100, null=True)
    Nationality = models.CharField(max_length=100, null=True)
    body_marks = models.CharField(max_length=100, null=True)
    gang = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.folder_name


class Charges(models.Model):
    p = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wantedby = models.CharField(max_length=100)
    ctype = models.CharField(max_length=100)
