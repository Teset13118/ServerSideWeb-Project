from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, UserDetail, Activity, Review


# User Admin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

    # ใช้สำหรับฟอร์มตอนแก้ไขข้อมูลผู้ใช้
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number', 'groups'),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active'),
        }),
        ('Password Reset', {
            'fields': ('password',),
        }),
    )

    # ใช้สำหรับฟอร์มตอนเพิ่มผู้ใช้ใหม่
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2'),
        }),
        ('Add Groups', {
            'fields': ('groups',),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active'),
        }),
    )

    filter_horizontal = ('groups',)

# UserDetail Admin
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'birthday')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('gender',)

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