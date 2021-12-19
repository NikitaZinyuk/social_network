import django_filters

from .models import Like


class LikeFilter(django_filters.FilterSet):

    liked_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Like
        fields = ('liked_at',)
