from django.db import models

# Create your models here.

class Objetos(models.Model):
    nombre = models.CharField(max_length= 200)