from django.views.generic import ListView

from logs.filters import LogItemFilter
from logs.models import LogItem


class LogListView(ListView):
    model = LogItem
    paginate_by = 40

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('ip'):
            queryset = LogItemFilter(self.request.GET, queryset).qs
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['statistics'] = LogItem.get_statistics(self.get_queryset())
        return context
