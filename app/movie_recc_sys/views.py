from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Movie
from .input_movie import similar

# Create your views here.
