from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Movie
from .input import  similar
from .forms import MovieURLForm

# Create your views here.
def home(request):
    similar_movies =[]
    if request.method == 'POST':
        form = MovieURLForm(request.POST)
        if form.is_valid():
            movie_url = form.cleaned_data['movie_url']
                
        similar_movie_titles = similar(movie_url)

        # Retrieve poster paths for similar movies
        for similar_title in similar_movie_titles:
            similar_poster_path = f"movie_posters/{similar_title.replace(' ', '_').lower()}.jpg"
            similar_movies.append({
                'title': similar_title,
                'poster_path': similar_poster_path,
            })
    else:
            form = MovieURLForm()

    return render(request, 'home.html', {
        'form': form,
        'similar_movies': similar_movies,
    })