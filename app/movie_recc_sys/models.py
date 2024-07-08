from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='movie_posters')
    url = models.URLField()

    def __str__(self):
        return self.title
    