from django import forms

class MovieURLForm(forms.Form):
    movie_url = forms.URLField(label='Movie URL', required=True)
