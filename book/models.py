from django.db import models

from django.contrib.auth.models import User
from user.models import CustomUser

# Create your models here.

class Author(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    

    
class Book(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    author = models.CharField(max_length=250)
    genre = models.CharField(max_length=100)
    publish_year = models.IntegerField()
    cover = models.ImageField(upload_to='book_images', blank=True, null=True)
    pdf = models.FileField(upload_to='book_pdfs', blank=True, null=True)
    summary = models.TextField(max_length=500)
    donar = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    donated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Untitled"