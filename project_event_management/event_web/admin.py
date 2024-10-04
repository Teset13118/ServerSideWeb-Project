from django.contrib import admin
from .models import User, UserDetail, Category, Activity, UserCategory, Registration, ActivityImage, Review


# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'role') 
    search_fields = ('username', 'email')
    list_filter = ('role',)

# UserDetail Admin
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'birthday')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('gender',)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

# Activity Admin
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_date', 'category', 'is_approve')
    search_fields = ('title', 'description')
    list_filter = ('activity_type', 'is_approve')
    date_hierarchy = 'start_date'  # เพิ่มการนำทางตามวันที่

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('participant', 'activity', 'score', 'created_at')
    search_fields = ('participant__first_name', 'participant__last_name', 'activity__title')
    list_filter = ('score',)