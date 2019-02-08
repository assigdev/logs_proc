from django import forms

from logs.models import LogItem


class LogItemForm(forms.ModelForm):
    class Meta:
        model = LogItem
        fields = ['ip']
