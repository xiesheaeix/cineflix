from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('top_movies/', views.top_movies, name='top_movies'),
    path('coming_soon', views.coming_soon, name='coming_soon'),
]