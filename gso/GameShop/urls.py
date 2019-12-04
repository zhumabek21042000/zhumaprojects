from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url

import UserApp.views as view
from . import views
from .views import *

app_name = 'GameShop'
urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.search, name='search'),
    path('news/<int:pk>/', views.news, name='news_detail'),
    path('games/<int:pk>/', views.games, name='games_detail'),
    path('game-list/', views.game_list, name='game_list'),
    # custom admin
    path('news-form/', views.new_news, name='news_form'),
    path('games/delete/<int:game_id>/', views.delete_game, name='delete_game'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    path('game-form/', views.new_games, name='game_form'),
    path('game-form/edit/<int:pk>/', views.edit_game, name='edit_game'),
    path('profile/', views.profile, name='profile'),
    path('item/delete/<int:item_id>/', views.delete_from_cart, name='delete_item'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('profile/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('users/unban/<int:user_id>/', views.unban_user, name='unban_user'),
    path('rate-game/<int:game_id>/', views.rate_game, name='rate_game'),
    path('game-list/recommendations/', views.recommendations, name='recommendations'),
    path('news/<int:news_id>/deletecomment/', views.delete_comment, name='delete_comment'),
    path('users/', views.users, name='users'),
    path('category/action/', views.category_action, name='category_action'),
    path('category/arcade/', views.category_arcade, name='category_arcade'),
    path('category/office/', views.category_office, name='category_office'),
    path('category/strategy/', views.category_strategy, name='category_strategy'),
    path('buygame/', views.buy_game, name='buygame'),
    path('newslist/', views.news_list, name='news_list'),
    # USER APP
    path('login/', view.login_view, name='login'),
    path('register/', view.registration_view, name='register'),
    path('logout/', view.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)