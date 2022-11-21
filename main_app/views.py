from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests


def home(request):
    all = request.GET.get('all')
    response = requests.get(f'https://imdb-api.com/en/API/SearchAll/k_54v7k1ut/{all}').json()
    results = response['results']
    return render(request, 'home.html', {'results': results})

def top_movies(request):
    response = requests.get('https://imdb-api.com/en/API/Top250Movies/k_54v7k1ut').json()
    items = response['items']
    return render(request, 'top_movies.html', {'items': items})

def coming_soon(request):
    response = requests.get('https://imdb-api.com/en/API/ComingSoon/k_54v7k1ut').json()
    items = response['items']
    return render(request, 'coming_soon.html', {'items': items})

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