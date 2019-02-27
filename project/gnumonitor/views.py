from django.shortcuts import render
from django.http import HttpResponse
from gnumonitor.models import MonitorData

def index(request):
    one_dict = {'insert_me': "Hello!",}
    return render(request, 'gnumonitor/index.html', context = one_dict)

def gnumonitor(request):
    my_dict = {'insert_me': "gnumonitor",}
    return render(request, 'gnumonitor/gnumonitor.html', context = my_dict)
# Create your views here.
