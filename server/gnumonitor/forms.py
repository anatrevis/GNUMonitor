from django import forms
from django.core import validators
from gnumonitor.models import Chart
#
class ChartForm(forms.ModelForm):
    class Meta():
        model = Chart
        fields = '__all__'

    # def parameter_validation(self):
    #      raw_parameter = self.cleaned_data['parameter']


# class ChartForm(forms.Form):
#     xAxis_Name = forms.CharField(label='X axis name:', max_length=264) # time
#     yAxis_Name = forms.CharField(label='Y axis name:', max_length=264)
#     title = forms.CharField(label='Chart title:', max_length=264)
#     parameter = forms.CharField(label='Monitoring parameter:', max_length=264)
#
#     def save(self):
#         data = self.cleaned_data
#         Chart = Chart(xAxis_Name = data['xAxis_Name'])
