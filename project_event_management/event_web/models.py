from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Participant', 'Participant'),
        ('Organizer', 'Organizer'),
    ]

    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

class Activity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('online', 'Online'),
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('approval', 'Approval'),
        ('approved', 'Approved'),
        ('reject', 'Reject'),
    ]

    organizer = models.ForeignKey(
        "User", 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Organizer'}
    )
    category = models.ForeignKey(
        "Category", 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    close_register_date = models.DateTimeField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    location = models.TextField()
    platform = models.TextField()
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE_CHOICES)
    short_description = models.TextField()
    description = models.TextField()
    contact = models.TextField()
    is_approve = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES)

    def __str__(self):
        return self.title

class UserCategory(models.Model):
    participant = models.ForeignKey(
        "User", 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Participant'}
    )
    category = models.ForeignKey(
        "Category", 
        on_delete=models.CASCADE
    )

class Registration(models.Model):
    participant = models.ForeignKey(
        "User", 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Participant'}
    )
    category = models.ForeignKey(
        "Category", 
        on_delete=models.CASCADE
    )


class ActivityImage(models.Model):
    activity = models.ForeignKey(
        "Activity", 
        on_delete=models.CASCADE
    )
    image_path = models.ImageField(upload_to='activity_images/', verbose_name="รูปภาพกิจกรรม")

class Review(models.Model):
    SCORE_CHOICES = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
    ]

    participant = models.ForeignKey(
        "User", 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Participant'}
    )
    activity = models.ForeignKey(
        "Activity", 
        on_delete=models.CASCADE
    )
    description = models.TextField()
    score = models.CharField(max_length=1, choices=SCORE_CHOICES)
