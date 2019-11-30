from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'news_comment', 'created_date')
    list_filter = 'created_date'
    search_fields = ('user', 'description')
    # actions = ['approve_comments']
    #
    # def approve_comments(self, request, queryset):
    #     queryset.update(active=True)


# Register your models here.
admin.site.register(Comment)
admin.site.register(Games)
admin.site.register(Genre)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)

