from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class ProfileForm(ModelForm):
    class Meta:
        model = UserDetail
        fields = ('phone_number', 'age', 'gender', 'birthday')


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
            'close_register_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }