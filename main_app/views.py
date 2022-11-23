from django.shortcuts import render, redirect
from main_app.models import Movie
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
import requests


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
    items = response['items']
    # item_count = 0
    for item in items:
        # item_count += 1
        # while item_count <= 50:
        movie_data = Movie(
            imdbId = item['id'],
            title = item['title'],
            year = item['year'],
            image = item['image'],
            # rating = item['rating']
        )
        try: 
            if Movie.objects.get(imdbId=item['id']):
                pass
        except:
            movie_data.save()

    return render(request, 'top_movies.html', {'all_top_movies': items})
        # else:
        #     break

def coming_soon(request):
    response = requests.get('https://imdb-api.com/en/API/ComingSoon/k_54v7k1ut').json()
    items = response['items']

    for item in items:
        movie_data = Movie(
            imdbId = item['id'],
            title = item['title'],
            year = item['year'],
            image = item['image'],
            genres = item['genres'],
            # rating = item['rating']
        )
        try: 
            if Movie.objects.get(imdbId=item['id']):
                pass
        except:
            movie_data.save()

    return render(request, 'coming_soon.html', {'all_coming_soon': items})


def movie_details(request, movie_id):
    Movie.objects.get(imdbId=movie_id)
    response = requests.get(f'https://imdb-api.com/en/API/Title/k_54v7k1ut/{movie_id}').json()
    vid_response = requests.get(f'https://imdb-api.com/API/Trailer/k_54v7k1ut/{movie_id}').json()
    return render(request, 'movie/details.html', {'response': response, 'vid_response': vid_response})

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

class create_profile(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['avatar', 'bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

