import django_filters
from logs.models import LogItem


class LogItemFilter(django_filters.FilterSet):

    class Meta:
        model = LogItem
        fields = ['ip']
