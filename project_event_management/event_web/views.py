# Import necessary modules from Django for views, HTTP responses, and object management
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.views import View

# Import custom forms and models
from .forms import *
from .models import *

# Django ORM imports for database queries and functions
from django.db.models import F, Q, Count, Value, Avg, Max, Min, Sum
from django.db.models.functions import Length, Upper, Concat

# Import necessary libraries for handling JSON, datetime, and files
import json
import datetime
from django.core.files.storage import default_storage

# Authentication and user management utilities from Django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
# Email
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/admin/')
            
            if request.user.role == "Participant":
                return redirect('url_p_homepage')
            elif request.user.role == "Organizer":
                return redirect('url_o_homepage')
            else:
                return redirect('url_m_manageactivities')

        form = CustomUserCreationForm()
        return render(request, 'register.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usertxt = form.save()
            UserDetail.objects.create(
                user = usertxt 
            )

            if usertxt.role == 'Participant':
                group = Group.objects.get(name='Participant')
                usertxt.groups.add(group)
                return redirect('url_p_select_category', user_id=usertxt.id)
            elif usertxt.role == 'Organizer':
                group = Group.objects.get(name='Organizer')
                usertxt.groups.add(group)
                return redirect('url_login')
            else:
                return redirect('url_login')
      
        return render(request, 'register.html', {"form": form}) 
    
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/admin/')
            
            if request.user.role == "Participant":
                return redirect('url_p_homepage')
            elif request.user.role == "Organizer":
                return redirect('url_o_homepage')
            else:
                return redirect('url_m_manageactivities')

        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            
            user = form.get_user() 
            login(request,user)

            if user.is_superuser:
                return redirect('/admin/')
            
            if user.role == "Participant":
                return redirect('url_p_homepage')
            elif user.role == "Organizer":
                return redirect('url_o_homepage')
            else:
                return redirect('url_m_manageactivities')
        else:
            messages.error(request, "Invalid username or password")

        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('url_login')
    
class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'changepassword.html', {'form': form})
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #keeping the user logged in
            return redirect('url_profile')
        return render(request, 'changepassword.html', {'form': form})

# participant select category after register
class SelectCategory(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'participants/p_select_category.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        selected_categories = request.POST.getlist('categories')

        if selected_categories:
            UserCategory.objects.filter(participant=user).delete()

            for category_id in selected_categories:
                category = get_object_or_404(Category, id=category_id)
                UserCategory.objects.create(participant=user, category=category)

            # Redirect ไปหน้าอื่นหลังจากบันทึกเสร็จ
            return redirect('url_login')

        # หากไม่มีหมวดหมู่ถูกเลือก ให้ส่ง error กลับไปที่ template
        return render(request, 'participants/p_select_category.html', {
            'error': 'Please select at least one category.',
            'user': user
        })

# *-------------------------------------PARTICIPANT-------------------------------------*
# participants หน้าหลัก หน้าก่อนที่จะกดเข้าไป
class ViewHome(View):
    def get(self, request):
        current_time = timezone.now()
        activity = Activity.objects.filter(is_approve = "Approved", due_date__gt = current_time).order_by('?')[:4]  # Randomly shuffle and limit to 5

        return render(request, 'participants/p_home.html', {
            'activity': activity,
             'current_time': current_time,
            })

# participants หน้าแสดงกิจกรรมทั้งหมด
class ViewHomeActivity(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        search = request.GET.get('search', '')
        current_time = timezone.now()
        
        if category_id:
            activity = Activity.objects.filter(is_approve = "Approved", due_date__gt = current_time ,category_id=category_id)
        else:
            activity = Activity.objects.filter(is_approve = "Approved", due_date__gt = current_time)

        if search:
            activity = activity.filter(title__icontains=search)

        category = Category.objects.all()
        return render(request, 'participants/p_home_activity.html', {
            'activity': activity,
            'category': category,
            'search': search,
            'current_time': current_time,
            })

# *-------------------------------------PROFILE-------------------------------------*
# participant and organizer profile page
class ViewProfile(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_userdetail"]

    def get(self, request):
        profile = get_object_or_404(UserDetail, user_id=request.user.id)
        registration_activity = Registration.objects.filter(participant_id=request.user.id)

        return render(request, 'participants/p_profile.html', {
            'profile': profile,
            'regis_activity': registration_activity
        })

# edit profile participant and organizer
class ViewProfileEdit(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_userdetail", "event_web.change_userdetail"]

    def get(self, request):
        userdetail = get_object_or_404(UserDetail, user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        form1 = ProfileEditForm(instance = userdetail)
        form2 = UserEditForm(instance = user)
        return render(request, 'participants/p_profile_edit.html', {
            'form1': form1,
            'form2': form2,
        })
    
    def post(self, request):
        profile = get_object_or_404(UserDetail, user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        form1 = ProfileEditForm(request.POST, request.FILES, instance=profile)
        form2 = UserEditForm(request.POST, request.FILES, instance=user)

        if form1.is_valid() and form2.is_valid():
            if 'upload_profile' in request.FILES:
                if profile.image_path:
                    default_storage.delete(profile.image_path.path)
                profile.image_path = request.FILES['upload_profile']
            form1.save()
            form2.save()
            profile.save()  # บันทึกข้อมูลโปรไฟล์ที่รวมถึงภาพ
            return redirect('url_profile')

        return render(request, 'participants/p_profile_edit.html', {
            'form1': form1,
            'form2': form2,
        })

# show activity for all
class ViewActivity(View):
    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        # เช็คว่า organizer เป็นคนที่สร้าง activity
        if request.user.role == "Organizer" and request.user != activity.organizer:
            raise PermissionDenied

        activity_images = ActivityImage.objects.filter(activity=activity)
        registration = Registration.objects.filter(activity_id=activity_id) # เอาไว้นับจำนวนคนที่ลงทะเบียน
        current_time = timezone.now()
        reviews = Review.objects.filter(activity=activity)
        has_reviewed = Review.objects.filter(participant=request.user, activity=activity_id).exists()
        for review in reviews:
            review.star_list = ['★'] * review.score

        #เช็คว่ามีการ ลงทะเบียนไปแล้วหรือยัง
        already_registration = Registration.objects.filter(
            activity_id=activity_id, 
            participant_id=request.user.id
        ).exists()
            
        return render(request, 'participants/p_activity.html', {
            'activity': activity,
            'activity_images': activity_images,
            'already_registration': already_registration,
            'current_time': current_time,
            'reviews': reviews,
            'has_reviewed': has_reviewed,
            'registration': registration,
            'user': request.user,
        })
    
    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        act = request.POST.get('act')
        comment = request.POST.get("comment")
        score = request.POST.get("score")

        if comment and score:
            review = Review.objects.create(
            participant=request.user,
            description=comment,
            score=score,
            activity=activity,
            created_at=timezone.now())
        else:
            messages.error(request, "Comment and score are required.")

        if act == 'register':
            Registration.objects.create(
                activity_id=activity_id, 
                participant_id=request.user.id
            )
            messages.success(request, "You have successfully registered for the activity.")
        elif act == 'cancel':
            Registration.objects.filter(
                activity_id=activity_id, 
                participant_id=request.user.id
            ).delete()

        return redirect('url_p_activitypage', activity_id=activity_id)

    def delete(self, request, review_id):
        if request.method == 'DELETE':
            review = get_object_or_404(Review, id=review_id, participant=request.user)
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# *-------------------------------------ORGANIZER-------------------------------------*
# organizer หน้าหลัก
class ViewOrganizerHome(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_activity", "event_web.add_activity"]

    def get(self, request):
        activity = Activity.objects.filter(organizer_id = request.user.id).order_by('id')
        return render(request, 'organizer/o_home.html',{
            'activity': activity,
        })

# show list participant for organizer to see
class ViewRegistrationUserList(View):
    def get(self, request, activity_id):
        list = Registration.objects.filter(activity_id=activity_id)
        activity = Activity.objects.get(id=activity_id)
        # เช็คว่า organizer เป็นคนที่สร้าง activity
        if request.user.role == "Organizer" and request.user != activity.organizer:
            raise PermissionDenied
        context = {
            'list': list,
            'activity': activity,
        }

        return render(request, 'organizer/o_regis_list.html', context)

# organizer "CREATE" activity
class View_CreateActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_activity", "event_web.add_activity"]

    def get(self, request):
        form = CreateActivity_Form()
        purpose = "create"
        return render(request, 'organizer/mo_ce_activity.html', {'form': form, 'purpose': purpose})

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
                organizer_id= request.user.id,
                is_approve="Approval", #FIXED STATUS DONT CHANGE!!!
            )

            new_images = request.FILES.getlist('upload_image')
            for image in new_images:
                ActivityImage.objects.create(activity=activity, image_path=image)
            return redirect('url_o_homepage')
        else:
            return render(request, 'organizer/mo_ce_activity.html', {'form': form})

# MANAGER and organizer "EDIT" activity
class EditActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_activity", "event_web.change_activity"]

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        # เช็คว่า organizer เป็นคนที่สร้าง activity
        if request.user.role == "Organizer" and request.user != activity.organizer:
            raise PermissionDenied
        form = CreateActivity_Form(instance=activity)
        purpose = "edit"
        activity_images = ActivityImage.objects.filter(activity=activity)
        return render(request, 'organizer/mo_ce_activity.html', {'activity': activity, 'form': form, 'purpose': purpose, 'activity_images': activity_images})
    
    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
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

            # เพิ่มภาพใหม่ ทับอันเก่า
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

            # ตรวจสอบบทบาทของผู้ใช้
            if request.user.role == "Organizer":
                return redirect('url_o_homepage')
            else:
                return redirect('url_m_manageactivities') 
        
        else:
            form = CreateActivity_Form(request.POST, request.FILES, instance=activity)
            activity_images = ActivityImage.objects.filter(activity=activity)
            purpose = "edit"
            return render(request, 'organizer/mo_ce_activity.html', {
                'form': form,
                'activity': activity,
                'purpose': purpose,
                'activity_images': activity_images
            })

# ORGANIZER "DELETE" ACTIVITY
class DeleteActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_activity", "event_web.delete_activity"]

    def get(self, request, activity_id):
        Activity.objects.filter(
            organizer_id = request.user.id,
            id = activity_id).delete()
        return redirect('url_o_homepage')
    
# *-------------------------------------MANAGER-------------------------------------*
# MANAGE "USER" FOR MANAGER
class ViewManageUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_user", "event_web.delete_user"]

    def get(self, request):
        participants = User.objects.filter(role='Participant')
        organizers = User.objects.filter(role='Organizer')
        context = {
            'participants': participants,
            'organizers': organizers,
        }
        return render(request, 'manager/m_manage_users.html', context)
    
    def delete(self, request, user_id):
        get_user = get_object_or_404(User, id=user_id)

        user_groups = get_user.groups.all()  # ดึงกลุ่มที่ผู้ใช้เป็นสมาชิก
        for group in user_groups:
            get_user.groups.remove(group)  # ลบผู้ใช้จากกลุ่ม

        if get_user.role == 'Organizer':
            activities = Activity.objects.filter(organizer=get_user)
            for activity in activities:
                activity_images = ActivityImage.objects.filter(activity=activity)
                for image in activity_images:
                    if image.image_path and default_storage.exists(image.image_path.path):
                        default_storage.delete(image.image_path.path)
                    image.delete()
            activities.delete()
            
        get_user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)

# MANAGE "ACTIVITY" FOR MANAGER
class ViewManageActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_activity", "event_web.change_activity", "event_web.delete_activity"]

    def get(self, request):
        if request.user.role == "Organizer" or request.user.role == "Participant" :
            raise PermissionDenied
        else:
            activities = Activity.objects.all()
            context = {
                'activities': activities,
            }
            return render(request, 'manager/m_manage_activity.html', context)
    
    def delete(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        activity.delete()
        return JsonResponse({'message': 'Activity deleted successfully'}, status=200)
    
    def put(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        if activity.is_approve == 'Approval':
            activity.is_approve = 'Approved'
            activity.save()

            # ดึงผู้ใช้ที่สนใจใน Category ของ Activity
            interested_users = UserCategory.objects.filter(category=activity.category)

            # ส่งอีเมลแจ้งผู้ใช้ที่สนใจใน Category นั้น
            for user_category in interested_users:
                participant = user_category.participant
                send_mail(
                    subject=f'New Activity Approved: {activity.title}',
                    message = (
                        f"Dear User,\n\n"
                        f"We are pleased to inform you that the activity \"{activity.title}\" "
                        f"you expressed interest in has been approved!\n"
                        f"It is scheduled to start on {activity.start_date.strftime('%B %d, %Y')}.\n\n"
                        f"Thank you for your interest, and we hope to see you there!\n\n"
                        f"Best regards,\n"
                        f"Activity Hub Management Team"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[participant.email],
                    fail_silently=False,
                )

            return JsonResponse({'message': 'Activity approved successfully and emails sent'}, status=200)
        return JsonResponse({'message': 'Activity not in approval status'}, status=400)

# MANAGE "REVIEW" FOR MANAGER
class ViewManageReview(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["event_web.view_review", "event_web.delete_review"]

    def get(self, request):
        if request.user.role == "Organizer" or request.user.role == "Participant":
            raise PermissionDenied

        reviews = Review.objects.all()
        context = {
            'reviews': reviews,
        }
        return render(request, 'manager/m_manage_reviews.html', context)

    def delete(self, request, review_id):
        if request.method == 'DELETE':
            review = get_object_or_404(Review, id=review_id)
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        return JsonResponse({'error': 'Invalid request method'}, status=400)
