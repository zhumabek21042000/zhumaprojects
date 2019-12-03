from django import forms
from .models import *
from UserApp.models import Account


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ('user', 'text', 'created_date')
        fields = ('text',)
        exclude = ['user', 'news_comment']


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('user', 'text')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'user', 'date', 'image']
        # exclude = ['user']


class GameForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = ['name', 'creator', 'date_release', 'genres', 'mode', 'game_rate', 'price']
