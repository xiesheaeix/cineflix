from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('create_profile/', views.CreateProfile.as_view(), name='create_profile'),
    path('profile/<int:pk>/update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('search/', views.search, name='search'),
    path('top_movies/', views.top_movies, name='top_movies'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('movie/<movie_id>/', views.movie_details, name='details'),
    path('movie/<movie_id>/add_review/', views.add_review, name='add_review'),
    path('movie/<movie_id>/delete_review/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
    path('profile/<int:profile_id>/assoc_favorites/<int:favorites_id>/', views.assoc_favorites, name='assoc_favorites'),
    path('profile/<int:profile_id>/unassoc_favorites/<int:favorites_id>/', views.unassoc_favorites, name='unassoc_favorites'),
    path('favorites/', views.FavoritesList.as_view(), name='FavoritesList'),
    path('favorites/create/', views.FavoritesCreate.as_view(), name='FavoritesCreate'),
    path('favorites/<int:pk>/delete/', views.FavoritesDelete.as_view(), name='FavoritesDelete'),
]