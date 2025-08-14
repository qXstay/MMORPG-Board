import django_filters
from .models import Response


class ResponseFilter(django_filters.FilterSet):
    class Meta:
        model = Response
        fields = ['post__title', 'text', 'created_at', 'accepted']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.filter(post__author=self.user)