from django.urls import path
from . import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('logout/', views.custom_logout, name='logout'),
  path('', views.tweet_list, name='tweet_list'),
  path('create/', views.tweet_create, name='tweet_create'),
  path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
  path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
  path('search/', views.search, name='search'),  # Add the search URL pattern
  path('like_tweet/', views.like_tweet, name='like_tweet'),
  path('save_to_favorites/<int:tweet_id>/', views.save_to_favorites, name='save_to_favorites'),
] 

