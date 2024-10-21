from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm ,UsernameForm
from .forms import SignUpForm
from .models import Folder, Project
from .forms import FolderForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponse
from social_django.utils import psa
from django.contrib.auth.models import User
from social_core.backends.linkedin import LinkedinOAuth2
from social_core.exceptions import AuthForbidden
import logging
import requests
from .models import UserProfile
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileUpdateForm
from .models import validate_username
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from .models import Folder, ShowcaseRequest
from .forms import ShowcaseRequestForm, LinkFormSet
from .models import Folder, Project, ProjectLink
import uuid


@login_required(login_url='/login')
def choose_username_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            validate_username(username)
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already in use.")
            else:
                request.user.username = username
                request.user.userprofile.is_app_signup = True
                request.user.save()
                request.user.userprofile.save()
                return redirect('home')
        except ValidationError:
            messages.error(request, "Username should not contain spaces or special characters.")
    return render(request, 'choose_username.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if not hasattr(user, 'userprofile'):
                    UserProfile.objects.create(user=user)
                
                if (not user.userprofile.is_app_signup) or not user.username:
                    return redirect('choose_username')
                return redirect('home')  
            else:
                form.add_error('username', 'Invalid username or password')
                form.add_error('password', 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.userprofile.is_app_signup = True
            user.userprofile.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required(login_url='/login')
def home_view(request):
    
    if (not request.user.userprofile.is_app_signup) or not request.user.username:
        return redirect('choose_username')
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'home.html', {'folders': folders})
@login_required(login_url='/login')
def create_folder_view(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('home')
    else:
        form = FolderForm()
    return render(request, 'create_folder.html', {'form': form})

@login_required(login_url='/login')
def add_project_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        link_formset = LinkFormSet(request.POST)
        form.formset = link_formset
        if not form.is_valid():
            print("ProjectForm errors:", form.errors)
        if not link_formset.is_valid():
            print("LinkFormSet errors:", link_formset.errors)
        
        if form.is_valid() and link_formset.is_valid():
            project = form.save(commit=False)
            project.folder = folder
            project.save()
            for link_form in link_formset:
                if link_form.cleaned_data:
                    label = link_form.cleaned_data['label']
                    url = link_form.cleaned_data['url']
                    ProjectLink.objects.create(project=project, label=label, url=url)
            return redirect('view_contents', folder_id=folder.id)
        else:
            print("Form or formset is not valid.")
    else:
        form = ProjectForm()
        link_formset = LinkFormSet()
    return render(request, 'add_project.html', {'form': form, 'link_formset': link_formset, 'folder': folder})

@login_required(login_url='/login')
def view_contents_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    projects = Project.objects.filter(folder=folder)
    return render(request, 'view_contents.html', {'folder': folder, 'projects': projects})

@login_required(login_url='/login')
@csrf_exempt
def delete_project(request, project_id):
    if request.method == 'DELETE':
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'message': 'Project deleted successfully'}, status=200)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/login')
@csrf_exempt
def delete_folder(request, folder_id):
    if request.method == 'DELETE':
        try:
            folder = Folder.objects.get(id=folder_id)
            folder.delete()
            return JsonResponse({'message': 'Folder deleted successfully'}, status=200)
        except Folder.DoesNotExist:
            return JsonResponse({'error': 'Folder not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                profile_picture = request.FILES.get('profile_picture')
                if profile_picture:
                    valid_extensions = ['jpg', 'jpeg', 'png']
                    if not profile_picture.name.split('.')[-1].lower() in valid_extensions:
                        raise ValidationError('Unsupported file extension. Allowed extensions are: jpg, jpeg, png.')

                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile', username=user.username)
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            for field in user_form:
                for error in field.errors:
                    messages.error(request, error)
            for field in profile_form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/login')
def search_user(request):
    query = request.GET.get('username')
    if query:
        try:
            user = User.objects.get(username=query)
            return render(request, 'profile.html', {'user': user})
        except User.DoesNotExist:
            return render(request, 'no_user_found.html')
    return render(request, 'layout.html')

@login_required
def showcase_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    showcase_url = request.build_absolute_uri(reverse('showcase_page', args=[folder_id]))
    return render(request, 'showcase_folder.html', {'folder': folder, 'showcase_url': showcase_url})

def showcase_page(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    error = None

    if request.method == 'POST':
        form = ShowcaseRequestForm(request.POST)
        if form.is_valid():
            personal_number = uuid.uuid4()
            showcase_request = ShowcaseRequest.objects.create(
                folder=folder,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                company=form.cleaned_data['company'],
                description=form.cleaned_data['description'],
                linkedin_profile=form.cleaned_data['linkedin_profile'], 
                status='pending',
                personal_number=personal_number
            )
            return render(request, 'thank_you.html', {'personal_number': showcase_request.personal_number})
    else:
        form = ShowcaseRequestForm()
    
    if request.method == 'GET' and 'personal_number' in request.GET:
        personal_number = request.GET['personal_number']
        existing_request = ShowcaseRequest.objects.filter(folder=folder, personal_number=personal_number).first()
        if existing_request:
            if existing_request.status == 'approved':
                request.session['approved_user'] = str(existing_request.personal_number)
                return redirect('view_folder_contents', folder_id=folder.id)
            error = "Request not approved yet."
        else:
            error = "Invalid personal number."
    
    return render(request, 'showcase_page.html', {'form': form, 'folder': folder, 'error': error})

@login_required
def showcase_dashboard(request):
    requests = ShowcaseRequest.objects.filter(folder__user=request.user)
    return render(request, 'showcase_dashboard.html', {'requests': requests})

@login_required
def approve_request(request, request_id):
    showcase_request = get_object_or_404(ShowcaseRequest, id=request_id)
    showcase_request.status = 'approved'
    showcase_request.save()
    return redirect('showcase_dashboard')

@login_required
def deny_request(request, request_id):
    showcase_request = get_object_or_404(ShowcaseRequest, id=request_id)
    showcase_request.status = 'denied'
    showcase_request.save()
    return redirect('showcase_dashboard')

def view_folder_contents(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    projects = Project.objects.filter(folder=folder)
    

    if request.user.is_authenticated and folder.user == request.user:
        return render(request, 'view_contents.html', {'folder': folder, 'projects': projects})
    

    approved_user = request.session.get('approved_user')
    approved_request = ShowcaseRequest.objects.filter(folder=folder, personal_number=approved_user, status='approved').exists()
    
    if not approved_request:
        return redirect('showcase_page', folder_id=folder_id)
    
    return render(request, 'view_contents.html', {'folder': folder, 'projects': projects})