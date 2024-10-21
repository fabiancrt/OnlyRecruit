from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import re
import uuid

def validate_username(value):
    if not re.match("^[A-Za-z0-9]*$", value):
        raise ValidationError('Username must contain only letters and numbers.')

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    github_link = models.URLField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', 
        blank=True, 
        null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=150, blank=True)
    show_on_profile = models.BooleanField(default=False)  

    def __str__(self):
        return self.name

class ProjectLink(models.Model):
    project = models.ForeignKey(Project, related_name='links', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.label}: {self.url}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_app_signup = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

    def clean(self):
        validate_username(self.user.username)
        if User.objects.filter(username=self.user.username).exclude(pk=self.user.pk).exists():
            raise ValidationError('Username must be unique.')

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class ShowcaseRequest(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
    personal_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    linkedin_profile = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.folder.name}"