# from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView
                                  )

from GameShop.extras import generate_order_id
from .forms import CommentForm, NewsForm, GameForm
from GameShop.models import *
from django.contrib import messages


def home(request):
    games = Games.objects.all()
    news = News.objects.all()
    context = {'games': games, 'news': news}
    return render(request, 'GameShop/index.html', context)


def comment(request):
    coments = Comment.objects.all()
    context = {'coments': coments}
    return render(request, 'GameShop/news_detail.html', context)


def ban_user(request, user_id):
    user = get_object_or_404(Account, pk=user_id)
    user.is_active = False
    user.save()
    messages.warning(request, 'Account has been banned')
    return HttpResponseRedirect('GameShop:index')


def search(request):
    query = request.POST['top-search']
    results = Games.objects.filter(Q(genres__contains=query) | Q(name__contains=query))
    return render(request, 'GameShop/search.html', {'results': results})


def del_user(request, username):
    try:
        u = Account.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")

    except Account.DoesNotExist:
        messages.error(request, "User does not exist")
        return render(request, 'GameShop/profile.html')

    except Exception as e:
        return render(request, 'GameShop/profile.html', {'err': e.message})
    if not Account.is_admin:
        users = Account.objects.get(username=username)
    return render(request, 'GameShop/profile.html', {'users': users})


def news(request, pk):
    newss = get_object_or_404(News, pk=pk)
    comments = newss.comments.filter()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.newss = newss
            new_comment.save()
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
    # rateds = Rating.objects.get(rated=False)
    try:
        print(';alksjf;lakjfg;lsdkfjg;sdlkfgj;sldkfgj')
        ratings = Rating.objects.filter(rating_games=gamese)
        print('sss')
        print('user is found')
        for i in ratings:
            if i.rating_user == userx:
                print('already rated')
                return HttpResponseRedirect(reverse('GameShop:game_list', args=(game_id,)))
        new_rating = Rating(rating_user=userx, rating_games=gamese, rating_number=rating_number)
        new_rating.save()

        gamese.game_rate = gamese.game_rate + rating_number/10
        gamese.save()
    except:
        new_rating = Rating(rating_user=userx, rating_games=gamese, rating_number=rating_number)
        new_rating.save()
        gamese.game_rate = gamese.game_rate + rating_number / 10
        gamese.save()
    return HttpResponseRedirect(reverse('GameShop:games_detail', args=(game_id,)))


def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    item = Games.objects.filter(id=kwargs.get('item_id', "")).first()
    if item in request.user.profile.items.all():
        messages.info(request, 'You already own this game')
        return redirect(reverse('GameShop:games_list'))
    order_item, status = OrderItem.objects.get_or_create(game=item)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
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
    if form.is_valid():
        form.save()
        return redirect('GameShop:index')
    else:
        form = NewsForm()
    return render(request, 'GameShop/news_form.html', {'form': form})


def new_games(request):
    form = GameForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('GameShop:index')
    else:
        form = GameForm()
    return render(request, 'GameShop/game_form.html', {'form': form})


def edit_game(request, pk):
    instance = get_object_or_404(Games)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Changes saved")
            return redirect('news_detail', pk=instance.pk)
        context = {'name': instance.name,
                   'instance': instance, 'form': form}
        return render(request, 'GameShop/game_form.html', context)


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
    # ord = Games.genres.filter(genre_name__contains=Order.items.OrderItem.game.genre)
    if ord:
        s = []
        s.append(ord)
    profile = Profile.objects.get_or_create(user=request.user)
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [game.game for game in user_order_items]
    context = {
        'object_list': object_list,
        'current_order_products': current_order_products,
        'egame': egame,
        # 's': s,
    }

    return render(request, "GameShop/games_list.html", context)


def game_category(request):
    pass

