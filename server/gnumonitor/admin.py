from django.contrib import admin
from gnumonitor.models import Chart, Data_Chart, Data_Error

# Register your models here.
admin.site.register(Chart)
admin.site.register(Data_Chart)
admin.site.register(Data_Error)
