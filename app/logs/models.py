from django.db import models


class LogItem(models.Model):
    ip = models.GenericIPAddressField()
    datetime = models.DateTimeField()
    method = models.CharField(max_length=8)
    uri = models.CharField(max_length=300)
    status_code = models.SmallIntegerField()
    body_size = models.IntegerField()
    user_agent = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.ip}-{self.datetime}'

    @classmethod
    def get_statistics(cls, queryset):
        return {
            'unique_ips_count': queryset.values('ip').distinct().count(),
            'top_ten_ips': queryset.values('ip').annotate(count=models.Count('ip')).order_by('-count')[:10],
            'method_counts': queryset.values('method').annotate(count=models.Count('method')).order_by('-count'),
            'bytes': queryset.aggregate(models.Sum('body_size')).get('body_size__sum')
        }
