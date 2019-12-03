import django_filters
from .models import *


class GamesFilter(django_filters.FilterSet):
    ordering = django_filters.ChoiceFilter(label='Ordering', method='filter_by_ordering')

    class Meta:
        model = Games
        fields = {'name': ['icontains'],
                  'creator': ['icontains'],
                  }

    def filter_by_ordering(self, queryset, name, value):
        expression = 'date_release' if value == 'ascending' else '-date_release'
        return queryset.order_by(expression)
