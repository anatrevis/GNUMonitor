from gnumonitor import views
from django.urls import path
from rest import RestFunctions

#TEMPLATE TAGGING
app_name = 'gnumonitor'

urlpatterns = [
    # path('', views.datalist, name='gnumonitor'),
    path('hello/', views.hello, name='hello'),
    path('ajax_test/', views.ajax_test, name='ajax_test'),
    path('delete_chart/', RestFunctions.delete_chart, name='delete_chart'),
    path('charts_notifications/', RestFunctions.Charts_Notifications, name='Charts_Notifications'),
    path('hosts_notifications/', RestFunctions.Hosts_Notifications, name='Hosts_Notifications'),
    path('sys_notifications/', RestFunctions.Sys_Notifications, name='Sys_Notifications'),
    path('charts_data/', RestFunctions.Monitoring_Data, name='Monitoring_Data'),
    path('charts/', RestFunctions.Monitoring_Charts, name='Monitoring_Charts'),
    path('hosts/', RestFunctions.Monitoring_Hosts, name='Monitoring_Hosts'),
    path('hosts_data/', RestFunctions.Monitoring_Hosts_Data, name='Monitoring_Hosts_Data'),

]
