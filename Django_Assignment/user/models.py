from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    age = models.IntegerField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.BigIntegerField()
    email = models.CharField(max_length=255)
    web = models.CharField(max_length=255)
