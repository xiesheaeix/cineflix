import requests
from django.shortcuts import render, redirect
from main_app.models import Movie
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Favorites, Review
from .forms import ReviewForm


def home(request):
    return render(request, 'home.html' )

def search(request):
    all = request.GET.get('all')
    if all:
        response = requests.get(f'https://imdb-api.com/en/API/SearchAll/k_54v7k1ut/{all}').json()
        results = response['results']
        if results:
            for item in results:
                movie_data = Movie(
                    imdbId = item['id'],
                    title = item['title'],
                    image = item['image'],
                    )
                try: 
                    if Movie.objects.get(imdbId=item['id']):
                        pass
                except:
                    movie_data.save()
            return render(request, 'search.html', {'results': results})

def top_movies(request):
    response = requests.get('https://imdb-api.com/en/API/Top250Movies/k_54v7k1ut').json()
    items = response['items'][:50]

    for item in items:
        try: 
            if not Movie.objects.get(imdbId=item['id']):
                imdbId = item['id']
                # response = requests.get(f'https://imdb-api.com/en/API/Title/k_54v7k1ut/{imdbId}').json()
                # vid_response = requests.get(f'https://imdb-api.com/API/Trailer/k_54v7k1ut/{imdbId}').json()
                movie_data = Movie(
                    imdbId = item['id'],
                    title = item['title'],
                    year = item['year'],
                    image = item['image'],
                    genres = item['genres'],
                    # awards = response['awards'],
                    # trailer = vid_response['linkEmbed'],
                )
                movie_data.save()
        except Exception as e:
            print('error', e)

    return render(request, 'top_movies.html', {'all_top_movies': items})

def coming_soon(request):
    response = requests.get('https://imdb-api.com/en/API/ComingSoon/k_54v7k1ut').json()
    items = response['items'][:15]
    
    for item in items:
        try: 
            if not Movie.objects.get(imdbId=item['id']):
                imdbId = item['id']
                # response = requests.get(f'https://imdb-api.com/en/API/Title/k_54v7k1ut/{imdbId}').json()
                # vid_response = requests.get(f'https://imdb-api.com/API/Trailer/k_54v7k1ut/{imdbId}').json()
                movie_data = Movie(
                    imdbId = item['id'],
                    title = item['title'],
                    year = item['year'],
                    image = item['image'],
                    genres = item['genres'],
                    # awards = response['awards'],
                    # trailer = vid_response['linkEmbed'],
                )
                movie_data.save()
        except Exception as e:
            print('error', e)
        
    return render(request, 'coming_soon.html', {'all_coming_soon': items})


def movie_details(request, movie_id):
    response = requests.get(f'https://imdb-api.com/en/API/Title/k_54v7k1ut/{movie_id}').json()
    vid_response = requests.get(f'https://imdb-api.com/API/Trailer/k_54v7k1ut/{movie_id}').json()
    movie_data = Movie(
            imdbId = response['id'],
            title = response['title'],
            year = response['year'],
            image = response['image'],
            genres = response['genres'],
            # awards = response['awards'],
            trailer = vid_response['linkEmbed'],
        )
    try: 
        if Movie.objects.get(imdbId=movie_id):
            pass
    except:
        movie_data.save()
    movie = Movie.objects.get(imdbId=movie_id)
    review_form = ReviewForm()
    return render(request, 'movie/details.html', {'review_form': review_form, 'movie_data': movie, 'response': response, 'vid_response': vid_response})

@login_required
def add_review(request, movie_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        movie = Movie.objects.get(id=movie_id)
        new_review.movie_id = movie.id
        new_review.user = request.user
        new_review.save()
    return redirect('details', movie_id=movie.imdbId)

class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    def get_success_url(self):
        return f"/movie/{ self.object.movie.imdbId }"


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['avatar', 'bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'bio']
    success_url = '/profile'

class FavoritesList(LoginRequiredMixin, ListView):
    model = Favorites

class FavoritesCreate(LoginRequiredMixin, CreateView):
    model = FavoritesList
    fields = ['imdbId', 'title', 'image']

class FavoritesDelete(LoginRequiredMixin, DeleteView):
    model = Favorites
    success_url = '/profile'
    
@login_required
def assoc_favorites(request, profile_id, favorites_id):
    Profile.objects.get(id=profile_id).favorites.add(favorites_id)
    return redirect('profile', profile_id=profile_id)

@login_required
def unassoc_favorites(request, profile_id, favorites_id):
    Profile.objects.get(id=profile_id).favorites.remove(favorites_id)
    return redirect('profile', profile_id=profile_id)



