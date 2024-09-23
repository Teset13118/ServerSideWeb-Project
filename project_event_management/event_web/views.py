from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.db import transaction
from .forms import *
from .models import *
from django.db.models import F, Q, Count, Value, Avg, Max, Min, Sum
from django.db.models.functions import Length, Upper, Concat
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('url_login')
        return render(request, 'register.html', {"form": form}) 
    
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('url_p_homepage') 
        else:
            messages.error(request, "Invalid username or password")

        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('url_login')


class View_CreateActivity(View):
    def get(self, request):
        form = CreateActivity_Form()
        return render(request, 'o_activity_form.html', {'form': form})

    def post(self, request):
        form = CreateActivity_Form(request.POST, request.FILES)
        if form.is_valid():
            activity = Activity.objects.create(
                title=form.cleaned_data['title'],
                close_register_date=form.cleaned_data['close_register_date'],
                start_date=form.cleaned_data['start_date'],
                due_date=form.cleaned_data['due_date'],
                location=form.cleaned_data['location'],
                platform=form.cleaned_data['platform'],
                activity_type=form.cleaned_data['activity_type'],
                short_description=form.cleaned_data['short_description'],
                description=form.cleaned_data['description'],
                contact=form.cleaned_data['contact'],
                category=form.cleaned_data['category'],
                organizer_id=7, #FIXED HERE THIS IS A MANUAL INSERT :D
                is_approve="Approval",
            )

            images = request.FILES.getlist('upload_image')
            for image in images:
                ActivityImage.objects.create(activity=activity, image_path=image)
                
            return redirect('url_p_homepage')
        else:
            print(form.errors)
            form = CreateActivity_Form()
            return render(request, 'o_activity_form.html', {'form': form})

class ViewHome(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if category_id:
            activity = Activity.objects.filter(category_id=category_id)
        else:
            activity = Activity.objects.all()

        category = Category.objects.all()
        return render(request, 'participants/p_home.html', {
            'activity': activity,
            'category': category
            })

class ViewTest(View):
    def get(self, request):
        return render(request, 'participants/p_profile.html')

class ViewActivity(View):
    def get(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        activity_images = ActivityImage.objects.filter(activity=activity)

        return render(request, 'participants/p_activity.html', {
            'activity': activity,
            'activity_images': activity_images
        })

class ViewManageUser(View):
    def get(self, request):
        participants = User.objects.filter(role='Participant')
        organizers = User.objects.filter(role='Organizer')
        context = {
            'participants': participants,
            'organizers': organizers,
        }
        return render(request, 'manager/m_manage_users.html', context)

class ViewManageActivity(View):
    def get(self, request):
        activities = Activity.objects.all()
        context = {
            'activities': activities,
        }
        return render(request, 'manager/m_manage_activity.html', context)