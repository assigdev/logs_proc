import django_filters

from logs.forms import LogItemForm
from logs.models import LogItem


class LogItemFilter(django_filters.FilterSet):
    class Meta:
        model = LogItem
        form = LogItemForm
        fields = {
            'ip': ['exact'],
            'datetime': ['gte', 'lte'],
        }
