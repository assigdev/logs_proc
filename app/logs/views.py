from django.views.generic import ListView
from logs.models import LogItem


class LogListView(ListView):
    model = LogItem
    paginate_by = 40

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['statistic'] = LogItem.get_statistics(self.get_queryset())
        return context
