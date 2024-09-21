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
        return render(request, 'participants/p_home.html')

class ViewActivity(View):
    def get(self, request):
        return render(request, 'participants/p_activity.html')

class View_Activity(View):
    def get(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        activity_images = ActivityImage.objects.filter(activity=activity)

        return render(request, 'p_activity_detail.html', {
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