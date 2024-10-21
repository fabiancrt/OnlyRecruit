
from django.contrib import admin
from django.urls import path, include
from OR import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('', views.index_view, name='index'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('create_folder/', views.create_folder_view, name='create_folder'),
    path('add_project/<int:folder_id>/', views.add_project_view, name='add_project'),
    path('home/', views.home_view, name='home'),
    path('view_contents/<int:folder_id>/', views.view_contents_view, name='view_contents'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('folder/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('choose-username/', views.choose_username_view, name='choose_username'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('search/', views.search_user, name='search_user'),
    path('showcase_folder/<int:folder_id>/', views.showcase_folder, name='showcase_folder'),
    path('showcase_page/<int:folder_id>/', views.showcase_page, name='showcase_page'),
    path('showcase_dashboard/', views.showcase_dashboard, name='showcase_dashboard'),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('deny_request/<int:request_id>/', views.deny_request, name='deny_request'),
    path('folder_contents/<int:folder_id>/', views.view_folder_contents, name='view_folder_contents'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)