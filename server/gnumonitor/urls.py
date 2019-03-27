from gnumonitor import views
from django.urls import path
from rest import RestFunctions

#TEMPLATE TAGGING
app_name = 'gnumonitor'

urlpatterns = [
    # path('', views.datalist, name='gnumonitor'),
    path('hello/', views.hello, name='hello'),
    path('ajax_test/', views.ajax_test, name='ajax_test'),
    path('rest/', RestFunctions.Monitoring_Data, name='Monitoring_Data'),
]
