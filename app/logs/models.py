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
            'unique_ip': '',
            'top_ten_ip': '',
            'methods_count': '',
            'bytes': ''
        }
