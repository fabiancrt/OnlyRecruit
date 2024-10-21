from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Folder, Project, UserProfile
import re
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from .models import Project, ProjectLink

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        domain = email.split('@')[1]
        if domain not in allowed_domains:
            raise ValidationError('Please use an email address from a known provider (e.g., Gmail, Yahoo, Outlook).')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain at least one special character.')
        if username.lower() in password.lower():
            raise ValidationError('Password must not be similar to the username.')
        return password

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=150,
        help_text='Max 150 words.'
    )

    class Meta:
        model = Project
        fields = ['name', 'github_link', 'video', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'required': False}),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control custom-file-input',
                'accept': 'video/mp4,video/x-m4v,video/*'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control custom-file-input',
                'accept': 'image/jpeg,image/png,image/gif,image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.formset = kwargs.pop('formset', None)
        super().__init__(*args, **kwargs)
        self.fields['github_link'].required = False

    def clean(self):
        cleaned_data = super().clean()
        github_link = cleaned_data.get('github_link')
        link_formset = self.formset

        if link_formset and link_formset.is_valid():
            if not github_link and not any(form.cleaned_data for form in link_formset.forms if form.cleaned_data):
                raise ValidationError('You must provide at least one link: either a GitHub link or other links.')
        else:
            raise ValidationError('Invalid link formset.')

        return cleaned_data

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            allowed_video_formats = (
                '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpg', '.mpeg', 
                '.3gp', '.m4v', '.ogv', '.asf', '.vob', '.rm', '.rmvb', '.ts', '.mts', 
                '.m2ts', '.f4v'
            )
            if not video.name.lower().endswith(allowed_video_formats):
                raise forms.ValidationError('Only video files are allowed.')
        return video

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf')):
                raise forms.ValidationError('Only image files are allowed.')
        return image

class LinkForm(forms.ModelForm):
    class Meta:
        model = ProjectLink
        fields = ['label', 'url']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

LinkFormSet = formset_factory(LinkForm, extra=1)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if username is None:
            raise ValidationError('Username cannot be empty.')

        if ' ' in username:
            raise ValidationError('Username cannot contain spaces.')

        if not re.match("^[A-Za-z0-9]*$", username):
            raise ValidationError('Username can only contain letters and numbers.')

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This username is already taken.')

        return username

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description']

class ShowcaseRequestForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    company = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    linkedin_profile = forms.URLField(label='LinkedIn Profile', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        valid_providers = ['gmail.com', 'yahoo.com']
        domain = email.split('@')[-1]
        if domain not in valid_providers:
            raise ValidationError('Email must be from a valid provider (e.g., Gmail or Yahoo).')
        return email

    def clean_linkedin_profile(self):
        linkedin_profile = self.cleaned_data.get('linkedin_profile')
        linkedin_pattern = re.compile(r'^https:\/\/(www\.)?linkedin\.com\/.*$')
        if not linkedin_pattern.match(linkedin_profile):
            raise ValidationError('LinkedIn profile URL must be a valid LinkedIn link.')
        return linkedin_profile
        