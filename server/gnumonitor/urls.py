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
    path('create_errors_list/', RestFunctions.create_errors_list, name='create_errors_list'),
    path('rest/', RestFunctions.Monitoring_Data, name='Monitoring_Data'),
]
