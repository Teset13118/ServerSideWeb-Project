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

from django.core.files.storage import default_storage
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
            usertxt = form.save()
            UserDetail.objects.create(
                user = usertxt 
            )
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
            if user.role == "Participant":
                return redirect('url_p_homepage')
            else:
                return redirect('url_profile')
        else:
            messages.error(request, "Invalid username or password")

        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('url_login')

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
    
class ViewProfile(View):
    def get(self, request, userid):
        profile = UserDetail.objects.get(user_id=userid)
        return render(request, 'participants/p_profile.html', {
            'profile': profile,
        })
    
class ViewProfileEdit(View):
    def get(self, request, userid):
        profile = UserDetail.objects.get(user_id=userid)
        user = User.objects.get(id=userid)
        form1 = ProfileEditForm(instance = profile)
        form2 = UserEditForm(instance = user)
        return render(request, 'participants/p_profile_edit.html', {
            'form1': form1,
            'form2': form2,
        })
    
    def post(self, request, userid):
        profile = UserDetail.objects.get(user_id=userid)
        user = User.objects.get(id=userid)
        form1 = ProfileEditForm(request.POST, instance=profile)
        form2 = UserEditForm(request.POST, instance=user)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('url_profile', userid=userid)

        return render(request, 'participants/p_profile_edit.html', {
            'form1': form1,
            'form2': form2,
        })

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
    
class View_CreateActivity(View):
    def get(self, request):
        form = CreateActivity_Form()
        purpose = "create"
        return render(request, 'mo_ce_activity.html', {'form': form, 'purpose': purpose})

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
                organizer_id=1, #FIXED HERE THIS IS A MANUAL INSERT :D
                is_approve="Approval", #FIXED STATUS DONT CHANGE!!!
            )

            new_images = request.FILES.getlist('upload_image')
            for image in new_images:
                ActivityImage.objects.create(activity=activity, image_path=image)
            return redirect('url_p_homepage')
        else:
            print(form.errors)
            form = CreateActivity_Form()
            return render(request, 'mo_ce_activity.html', {'form': form})

class EditActivity(View):
    def get(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        form = CreateActivity_Form(instance=activity)
        purpose = "edit"
        activity_images = ActivityImage.objects.filter(activity=activity)
        return render(request, 'mo_ce_activity.html', {'activity': activity, 'form': form, 'purpose': purpose, 'activity_images': activity_images})
    
    def post(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        form = CreateActivity_Form(request.POST, request.FILES, instance=activity)

        if form.is_valid():
            form.save()

            # ID ของภาพที่ถูกลบ
            existing_image_ids_remove = request.POST.getlist('existing_image_ids_to_remove')

            # ลบภาพเก่าที่เลือก
            for image_id in existing_image_ids_remove:
                old_image = ActivityImage.objects.get(id=image_id, activity=activity)
                if old_image.image_path:
                    default_storage.delete(old_image.image_path.path)
                old_image.delete()

            # อัปเดตภาพเก่าเป็นใหม่
            activity_images = ActivityImage.objects.filter(activity=activity)
            for remaining_image in activity_images:
                uploaded_file = request.FILES.get(f'upload_image_{remaining_image.id}')
                if uploaded_file:  # หากมีการอัปโหลดไฟล์ใหม่
                    if remaining_image.image_path:  # หากมีภาพเก่า
                        default_storage.delete(remaining_image.image_path.path)  # ลบไฟล์เก่าจากเซิร์ฟเวอร์
                    # อัปเดตภาพ
                    remaining_image.image_path = uploaded_file
                    remaining_image.save()

            # หากมีการอัปโหลดภาพใหม่
            new_images = request.FILES.getlist('upload_image') 
            for new_image in new_images:
                ActivityImage.objects.create(activity=activity, image_path=new_image)

            return redirect('url_p_homepage')
        
        else:
            form = CreateActivity_Form(request.POST, request.FILES, instance=activity)
            activity_images = ActivityImage.objects.filter(activity=activity)
            purpose = "edit"
            return render(request, 'mo_ce_activity.html', {
                'form': form,
                'activity': activity,
                'purpose': purpose,
                'activity_images': activity_images
            })

class SelectCategory(View):
    def get(self, request):
        return render(request, 'participants/p_select_category.html')



# OLD CREATE AND EDIT ACTIVITY (INCASE_ERRORS NEEDED TO ROLL BACK)

# class View_CreateActivity(View):
#     def get(self, request):
#         form = CreateActivity_Form()
#         return render(request, 'o_activity_form.html', {'form': form})

#     def post(self, request):
#         form = CreateActivity_Form(request.POST, request.FILES)
#         if form.is_valid():
#             activity = Activity.objects.create(
#                 title=form.cleaned_data['title'],
#                 close_register_date=form.cleaned_data['close_register_date'],
#                 start_date=form.cleaned_data['start_date'],
#                 due_date=form.cleaned_data['due_date'],
#                 location=form.cleaned_data['location'],
#                 platform=form.cleaned_data['platform'],
#                 activity_type=form.cleaned_data['activity_type'],
#                 short_description=form.cleaned_data['short_description'],
#                 description=form.cleaned_data['description'],
#                 contact=form.cleaned_data['contact'],
#                 category=form.cleaned_data['category'],
#                 organizer_id=1, #FIXED HERE THIS IS A MANUAL INSERT :D
#                 is_approve="Approval", #FIXED STATUS DONT CHANGE!!!
#             )

#             images = request.FILES.getlist('upload_image')
#             for image in images:
#                 ActivityImage.objects.create(activity=activity, image_path=image)
#             return redirect('url_p_homepage')
#         else:
#             print(form.errors)
#             form = CreateActivity_Form()
#             return render(request, 'o_activity_form.html', {'form': form})

# class EditActivity(View):
#     def get(self, request, activity_id):
#         activity = Activity.objects.get(id=activity_id)
#         categories = Category.objects.all()
#         return render(request, 'mo_activity_editform.html', {'activity': activity, 'categories': categories})
    
#     def post(self, request, activity_id):
#         activity = Activity.objects.get(id=activity_id)

#         activity.title = request.POST.get('title')
#         activity.close_register_date = request.POST.get('close_register_date')
#         activity.start_date = request.POST.get('start_date')
#         activity.due_date = request.POST.get('due_date')
#         activity.location = request.POST.get('location')
#         activity.platform = request.POST.get('platform')
#         activity.activity_type = request.POST.get('activity_type')
#         activity.short_description = request.POST.get('short_description')
#         activity.description = request.POST.get('description')
#         activity.contact = request.POST.get('contact')
#         activity.save()

#         images = request.FILES.getlist('upload_image') 
#         if images:
#             old_images = ActivityImage.objects.filter(activity=activity)
#             for old_image in old_images:
#                 # ลบไฟล์จากเซิร์ฟเวอร์
#                 if old_image.image_path:
#                     default_storage.delete(old_image.image_path.path)
#             # ลบจากฐานข้อมูล
#             old_images.delete()

#             for image in images:
#                 ActivityImage.objects.create(activity=activity, image_path=image)
#         return redirect('url_p_homepage')