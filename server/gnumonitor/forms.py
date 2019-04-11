from django import forms
from django.core import validators
from gnumonitor.models import Chart

class ChartForm(forms.ModelForm):
    class Meta():
        model = Chart
        fields = '__all__'
