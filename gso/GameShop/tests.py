from django.shortcuts import render
from django.test import TestCase, Client


# Create your tests here.
from GameShop.models import Order, Category


def recommendations(request):
    userx = Order.items.filter(order__owner=request.user)
    game = userx.values('game__category__name')
    if game.exists():
        g = game[0]
        rec = Category.objects.filter(name__icontains=g)
        return rec
    return game
    # pass