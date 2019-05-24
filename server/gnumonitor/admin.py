from django.contrib import admin
from gnumonitor.models import Sys_Report, Host, Host_Data, Host_Report, Chart, Chart_Data, Chart_Report

# Register your models here.
admin.site.register(Sys_Report)
admin.site.register(Host)
admin.site.register(Host_Data)
admin.site.register(Host_Report)
admin.site.register(Chart)
admin.site.register(Chart_Data)
admin.site.register(Chart_Report)
