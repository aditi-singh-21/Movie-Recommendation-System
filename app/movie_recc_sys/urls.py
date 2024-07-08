from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view for the movie recommendation system
]
