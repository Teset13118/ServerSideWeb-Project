from django.shortcuts import render, redirect
from .forms import CreateActivity_Form
from .models import Activity, ActivityImage

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.db import transaction

from django.db.models import F, Q, Count, Value, Avg, Max, Min, Sum
from django.db.models.functions import Length, Upper, Concat
from django.db.models.lookups import GreaterThan
import json, datetime
from .forms import *

class View_CreateActivity(View):
    def get(self, request):
        form = CreateActivity_Form()
        return render(request, 'activity_form.html', {'form': form})

    def post(self, request):
        form = CreateActivity_Form(request.POST, request.FILES)
        if form.is_valid():
            activity = Activity.objects.create(
                title=form.cleaned_data['title'],
                close_register_date=form.cleaned_data['close_register_date'],
                start_date= form.cleaned_data['start_date'],
                due_date= form.cleaned_data['due_date'],
                location=form.cleaned_data['location'],
                platform=form.cleaned_data['platform'],
                activity_type=form.cleaned_data['activity_type'],
                short_description=form.cleaned_data['short_description'],
                description=form.cleaned_data['description'],
                contact=form.cleaned_data['contact'],
                category=form.cleaned_data['category'],
                organizer_id=7,
                is_approve = "Approval",
            )

            images = request.FILES.getlist('upload_image')
            for image in images:
                ActivityImage.objects.create(activity=activity, image_path=image)
            return redirect('asdasd')
        else:
            print(form.errors)
            form = CreateActivity_Form()
            return render(request, 'activity_form.html', {'form': form})
        
class index(View):
    def get(self, request):
        return render(request, 'index.html')