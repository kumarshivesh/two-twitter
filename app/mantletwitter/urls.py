"""
URL configuration for mantletwitter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.urls import views as auth_views
from tweet import views  # Import the custom_logout view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/', include('tweet.urls')),
    path('feed/', views.feed, name='feed'),
    path('posts/', views.user_posts_list, name='user_posts_list'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('likes/', views.likes_list, name='likes_list'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
     path('profile/<str:username>/media/', views.profile_media, name='profile_media'),
     path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
