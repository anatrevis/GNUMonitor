from django.contrib import admin
from gnumonitor.models import Host, Host_Data, Host_Error, Chart, Data_Chart, Data_Error

# Register your models here.
admin.site.register(Host)
admin.site.register(Host_Data)
admin.site.register(Host_Error)
admin.site.register(Chart)
admin.site.register(Data_Chart)
admin.site.register(Data_Error)
