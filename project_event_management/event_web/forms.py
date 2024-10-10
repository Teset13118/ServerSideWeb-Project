from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
import datetime


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number','password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'formbox'}),
            'email': forms.EmailInput(attrs={'class': 'formbox'}),
            'role': forms.Select(attrs={'class': 'formbox'}),  # Dropdown for role
            'phone_number': forms.TextInput(attrs={'class': 'formbox'}),
            'password1': forms.PasswordInput(attrs={'class': 'formbox'}),  # Password input for password1
            'password2': forms.PasswordInput(attrs={'class': 'formbox'}),  # Password input for password2
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if len(phone_number) < 10 and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be at least 10 digits long and must contain only digits.")
        elif len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")

        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        
        return phone_number
    

class ProfileEditForm(ModelForm):
    class Meta:
        model = UserDetail
        fields = ['age', 'gender', 'birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if birthday >= datetime.date.today():
            raise forms.ValidationError("Birthday must not be in the future and present.")
        
        return birthday
    
    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        birthday = cleaned_data.get('birthday')

        if birthday and age:
            cal_age = datetime.date.today().year - birthday.year

            if cal_age != age:
                raise forms.ValidationError("The age and birthday are inconsistent.")

        return cleaned_data

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if len(phone_number) < 10 and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be at least 10 digits long and must contain only digits.")
        elif len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")

        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        
        return phone_number


class CreateActivity_Form(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category"
    )
    location = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False)
    platform = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False)

    class Meta:
        model = Activity
        fields = [
            'title',
            'close_register_date',
            'start_date',
            'due_date',
            'location',
            'platform',
            'activity_type',
            'short_description',
            'description',
            'contact',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'close_register_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        close_register_date = cleaned_data.get('close_register_date')
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        # print(f"Close Register Date: {close_register_date}")
        # print(f"Start Date: {start_date}")
        # print(f"Due Date: {due_date}")

        if close_register_date and close_register_date < timezone.now():
            raise forms.ValidationError("Close register date cannot be in the past.")

        if start_date and start_date < timezone.now():
            raise forms.ValidationError("Start date cannot be in the past.")

        if due_date and due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past.")

        # start_date ต้องไม่ก่อน close_register_date
        if (close_register_date and start_date) and (start_date < close_register_date):
            raise forms.ValidationError("Start date cannot be before close register date.")

        # due_date ต้องไม่ก่อน close_register_date
        if (close_register_date and due_date) and (due_date < close_register_date):
            raise forms.ValidationError("Due date cannot be before close register date.")

        # due_date ต้องไม่ก่อน start_date
        if (start_date and due_date) and (due_date < start_date):
            raise forms.ValidationError("Due date cannot be before start date.")
        
        # start_date ต้องไม่อยู่หลัง due_date
        if (start_date and due_date) and (start_date > due_date):
            raise forms.ValidationError("Start date cannot be after due date.") 

        return cleaned_data
