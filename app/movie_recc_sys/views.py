from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Movie
from .input import  *
from .forms import MovieURLForm

# Create your views here.
def home(request):
    similar_movies =[]
    input_movie = []
    if request.method == 'POST':
        form = MovieURLForm(request.POST)
        if form.is_valid():
            movie_url = form.cleaned_data['movie_url']
                
        similar_movie_titles = similar(movie_url)
        input_movie_1 = input_mov(movie_url)
        # Retrieve poster paths for similar movies
        for similar_title in similar_movie_titles:
            similar_poster_filename = f"{similar_title}.jpg"
            similar_poster_path = f"/posters/{similar_poster_filename}"
            similar_movies.append({
                'title': similar_title,
                'poster_path': similar_poster_path,
            })
            if similar_title == input_movie_1[0]:
                    input_title = similar_title  # Last item in similar titles
                    input_poster_filename = f"{input_title}.jpg"
                    input_poster_path = f"/posters/{input_poster_filename}"
                    input_movie = {
                        'title': input_title,
                        'poster_path': input_poster_path,
                    }
        
        
    else:
            form = MovieURLForm()
    
    return render(request, 'movie_recc_sys/home.html', {
        'form': form,
        'input_mov' : input_movie,
        'similar_movies': similar_movies,
       
        
    })