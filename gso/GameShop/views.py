# from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView
                                  )

from GameShop.extras import generate_order_id
from .forms import CommentForm, NewsForm, GameForm
from GameShop.models import *
from django.contrib import messages
from .filters import *
from itertools import chain


def home(request):
    games = Games.objects.all()
    news = News.objects.all()
    ordered_games = Games.objects.order_by('-game_rate')
    context = {'games': games, 'news': news, 'ordered_games': ordered_games}
    return render(request, 'GameShop/index.html', context)


def comment(request):
    coments = Comment.objects.all()
    context = {'coments': coments}
    return render(request, 'GameShop/news_detail.html', context)


def delete_user(request, user_id):
    users = Account.objects.all()
    try:
        user_acc = get_object_or_404(Account, pk=user_id)
        user_acc.delete()
        messages.warning(request, 'Your account has been deleted')
        return HttpResponseRedirect('index')
    except:
        pass
    return render(request, 'GameShop/profile.html', {'users': users})


def ban_user(request, user_id):
    userx = Account.objects.all()
    if userx.filter(is_active=True):
        try:
            user = get_object_or_404(Account, pk=user_id)
            user.is_active = False
            user.save()
            HttpResponse('Account has been banned')
            return redirect('GameShop:ban_user')
        except:
            pass
    elif userx.filter(is_active=False):
        try:
            user = get_object_or_404(Account, pk=user_id)
            user.is_active = True
            user.save()
            HttpResponse('Account has been unbanned')
            return redirect('GameShop:ban_user')
        except:
            pass
    return render(request, 'GameShop/profile.html', {'userx': userx})


def search(request):
    try:
        query = request.GET['top-search']
        game_results = Games.objects.filter(
            Q(name__icontains=query) | Q(genres__genre_name__icontains=query) | Q(creator__icontains=query))
        news_results = News.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        results = chain(game_results, news_results)
        return render(request, 'GameShop/search.html', {'results': set(results)})
    except MultiValueDictKeyError:
        pass
    # results = Games.objects.filter(Q(name__icontains=query))
    return HttpResponseRedirect('index')


def delete_comment(request, news_id):
    newss = get_object_or_404(News, pk=news_id)
    comment = Comment.objects.filter(news_comment=newss)
    try:
        # comment_id = request.POST['comment_id']
        # comment.get(pk=comment_id).delete()
        comment.delete()
        # Comment.objects.get(pk=comment_id).delete()
    except:
        return HttpResponseRedirect(reverse('GameShop:news_detail'), args=(news_id,))
    return HttpResponseRedirect(reverse('GameShop:news_detail'), args=(news_id,))

def news(request, pk):
    newss = get_object_or_404(News, pk=pk)
    comments = newss.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.news_comment = newss
            new_comment.save()
            # return HttpResponseRedirect(reverse('GameShop:news_detail'), args=(pk,))
    else:
        comment_form = CommentForm
    context = {'news': newss, 'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, "GameShop/news_detail.html", context)


def games(request, pk):
    games = get_object_or_404(Games, pk=pk)
    context = {'games': games}
    return render(request, "GameShop/games_detail.html", context)


def rate_game(request, game_id):
    gamese = get_object_or_404(Games, pk=game_id)
    userx = Account.objects.get(pk=request.user.id)
    rating_number = float(request.POST['new_rating'])
    try:
        ratings = Rating.objects.filter(rating_games=gamese)
        for i in ratings:
            if i.rating_user == userx:
                print('already rated')
                return HttpResponseRedirect(reverse('GameShop:games_detail'), args=(game_id,))
        new_rating = Rating(rating_user=userx, rating_games=gamese, rating_number=rating_number, rated=True)
        new_rating.save()
        gamese.game_rate = gamese.game_rate + rating_number / 10
        if gamese.game_rate >= 5:
            gamese.game_rate = 5
        elif gamese.game_rate <= -5:
            gamese.game_rate = -5
        gamese.save()
    except Exception:
        pass
    return HttpResponseRedirect(reverse('GameShop:games_detail', args=(game_id,)))


def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    item = Games.objects.filter(id=kwargs.get('item_id', "")).first()
    if item in request.user.profile.items.all():
        messages.info(request, 'You already own this game')
        return redirect(reverse('GameShop:games_list'))
    order_item, status = OrderItem.objects.get_or_create(game=item, is_ordered=True)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=True)
    user_order.items.add(order_item)
    if status:
        order_item.is_ordered = True
        user_order.ref_code = generate_order_id()
        user_order.save()
        order_item.save()
    messages.info(request, 'Game has been added to cart')
    return redirect(reverse('GameShop:game_list'))


def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('GameShop:profile'))


def new_news(request):
    # if request.method == 'POST':
    form = NewsForm(request.POST or None)
    # new_form = None
    if form.is_valid():
        form.user = Account.objects.get(username=request.user.username)
        form.save()
        return redirect('GameShop:index')
    else:
        form = NewsForm()
    return render(request, 'GameShop/news_form.html', {'form': form})


def new_games(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            HttpResponse('Game has been added')
            return redirect('GameShop:index')
    else:
        form = GameForm()
    return render(request, 'GameShop/game_form.html', {'form': form})


def edit_game(request, pk):
    games = get_object_or_404(Games, pk=pk)
    if request.method == "POST":
        formm = GameForm(request.POST, instance=games)
        if formm.is_valid():
            games = formm.save(commit=False)
            games.save()
            return redirect('GameShop:index')
    else:
        formm = GameForm(instance=games)
    contexts = {
        'formm': formm,
        'games': games,
    }
    return render(request, 'GameShop/test.html', contexts)


def profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_orders': my_orders
    }
    return render(request, "GameShop/profile.html", context)


def game_list(request):
    object_list = Games.objects.all()
    egame = Games.objects.filter().order_by('-game_rate')
    if ord:
        s = []
        s.append(ord)
    # profile = Profile.objects.get_or_create(user=request.user)
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=True)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [game.game for game in user_order_items]
    context = {
        'object_list': object_list,
        'current_order_products': current_order_products,
        'egame': egame,
    }

    return render(request, "GameShop/games_list.html", context)


def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return HttpResponseRedirect(reverse('GameShop:index'))


def delete_game(request, game_id):
    game = get_object_or_404(Games, pk=game_id)
    game.delete()
    return HttpResponseRedirect(reverse('GameShop:index'))


def recommendations(request):
    # s = Order.items.filter(order__owner=request.user.username, game__genres=).all()
    g = Profile.items.filter(orderitem__order__owner=request.user)
    genre_list = []
    if g.exists():
        gg = g[0]
        genre = gg.genres.all()
        genre_list = []
        genre_list = [genr.genre_name for genr in genre]
    else:
        genre_list.append("Ssss")
    print(genre_list)
    return render(request, 'GameShop/games_list.html', {'genre_list': genre_list})
    # pass
# def category(request):
#     filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=True)
#     current_order_products = []
#     if filtered_orders.exists():
#         user_order = filtered_orders[0]
#         user_order_items = user_order.items.all()
#         current_order_products = [game.game for game in user_order_items]
#     context = {
#         'object_list': object_list,
#         'current_order_products': current_order_products,
#         'egame': egame,
#     }
