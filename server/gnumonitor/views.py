from django.shortcuts import render
from django.http import HttpResponse
from gnumonitor.models import Chart, Data_Chart
from gnumonitor.forms import ChartForm
from . import forms

def index(request):
    chart_list = Chart.objects.order_by('pk')
    monitor_charts ={'charts':chart_list}
    return render(request, "gnumonitor/index.html", context=monitor_charts)

def add_chart_form(request):
    form = ChartForm()

    if request.method =="POST":
        form = ChartForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("ERROR FORM INVALID")
    return render(request, 'gnumonitor/chart_form.html', {'form':form})


def datalist(request):
    data_list = Data_Chart.objects.order_by('time')
    data_dict ={'datalist':data_list}
    return render(request, "gnumonitor/datalist.html", context=data_dict)

# Create your views here.

def hello(request):
    return HttpResponse('Hello World!')

def ajax_test(request):
    variable = {'variable': 'world'}
    return render(request, 'gnumonitor/ajax_test.html', context = variable )
