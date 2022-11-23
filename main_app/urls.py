from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('create_profile', views.create_profile.as_view(), name='create_profile'),
    path('search/', views.search, name='search'),
    path('top_movies/', views.top_movies, name='top_movies'),
    path('coming_soon', views.coming_soon, name='coming_soon'),
    path('movie/<movie_id>/', views.movie_details, name='details'),
]