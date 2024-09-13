from django.db import models
from django.contrib.auth.models import AbstractUser, Group


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

    def __str__(self):
        return self.username