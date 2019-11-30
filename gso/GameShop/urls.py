from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url
from . import views
from .views import *

app_name = 'GameShop'
urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.search, name='search'),
    path('delete/', views.del_user, name='delete'),
    # path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<int:pk>/', views.news, name='news_detail'),
    path('games/<int:pk>/', views.games, name='games_detail'),
    # path('news/<int:pk>/addcomment/', views.add_comment_to, name='comment-new'),
    # custom admin
    path('news-form/', views.new_news, name='news_form'),
    path('game-form/', views.new_games, name='game_form'),
    path('profile/delete/', views.del_user, name='del_user'),
    path('profile/', views.profile, name='profile'),
    # path('profile/basket/', views.profile, name='basket'),
    path('item/delete/<int:item_id>/', views.delete_from_cart, name='delete_item'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('game-list/', views.game_list, name='game_list'),
    path('ban-user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('rate-game/<int:game_id>/', views.rate_game, name='rate_game'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)