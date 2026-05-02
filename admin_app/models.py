from django.db import models

# Create your models here.

class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, default="Administrator")
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name