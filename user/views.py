from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View, generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#TemplateView
from django.views.generic import TemplateView
from .models import CustomUser
from django.contrib.auth import logout
from django.contrib import messages

class UserCreate(TemplateView):
    model = CustomUser
    template_name = 'registration/register.html'

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']
            password2 = request.POST['password2']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            if password != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
            
            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone)
            user.save()
            return redirect('login')
    
    




