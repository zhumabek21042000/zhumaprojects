from django import forms
from .models import *
from UserApp.models import Account


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ('user', 'text', 'created_date')
        fields = ('text', )
        exclude = ['user']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'user', 'date', 'image']


class GameForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = ['name', 'creator', 'date_release', 'genres', 'mode', 'image', 'game_rate', 'price']
