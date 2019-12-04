import django
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from UserApp.models import *


# Create your models here.
# from UserApp.models import *
#
# class Category(models.Model):
#     name = models.CharField(max_length=250)
#     slug = models.SlugField(max_length=250, unique=True)
#     class Meta:
#         ordering = ('name', )
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     slug = models.SlugField()
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
#
#     class Meta:
#         unique_together = ('slug', 'parent',)
#         verbose_name_plural = "categories"
#
#     def __str__(self):
#         full_path = [self.name]
#         k = self.parent
#         while k is not None:
#             full_path.append(k.name)
#             k = k.parent
#         return ' -> '.join(full_path[::-1])


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    return "%s/%s" % (instance.id, filename)


class Games(models.Model):
    # category = models.ManyToManyField(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=20)
    date_release = models.DateTimeField(default=django.utils.timezone.now)
    genres = models.ManyToManyField(Genre)
    # age_restriction = models.IntegerField
    mode = models.CharField(max_length=10)
    price = models.FloatField(max_length=30)
    game_rate = models.FloatField()
    description = models.TextField(max_length=1000, null=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        return self.name

    # def get_cat_list(self):
    #     k = self.category  # for now ignore this instance method
    #
    #     breadcrumb = ["dummy"]
    #     while k is not None:
    #         breadcrumb.append(k.slug)
    #         k = k.parent
    #     for i in range(len(breadcrumb) - 1):
    #         breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
    #     return breadcrumb[-1:0:-1]
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200)
    game = models.ManyToManyField(Games, null=True, blank=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateTimeField(default=django.utils.timezone.now)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_image', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news_comment = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="users")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    # active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {} '.format(self.text, self.user)


class OrderItem(models.Model):
    game = models.OneToOneField(Games, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)

    # date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.game)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(default=0)
    items = models.ManyToManyField(Games, blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.game.price for item in self.items.all()])

    def __str__(self):
        return '{} - {}'.format(self.owner, self.ref_code)


class Rating(models.Model):
    rating_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating_games = models.ForeignKey(Games, on_delete=models.CASCADE)
    rating_number = models.FloatField()
    rated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.rating_number)


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=Account)
