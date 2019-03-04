from django.shortcuts import render
from django.http import HttpResponse
from gnumonitor.models import MonitorData

def index(request):
    monitor_data = MonitorData.objects.order_by('time')
    monitor_dict ={'monidata':monitor_data}
    return render(request, "gnumonitor/index.html", context=monitor_dict)


def datalist(request):
    data_list = MonitorData.objects.order_by('time')
    data_dict ={'datalist':data_list}
    return render(request, "gnumonitor/datalist.html", context=data_dict)

# Create your views here.
