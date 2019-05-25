from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from gnumonitor.models import Sys_Report, Host, Host_Data, Host_Report, Chart, Chart_Data, Chart_Report
from gnumonitor.forms import ChartForm
from . import forms

def index(request):
    chart_list = Chart.objects.order_by('pk')
    errors_list = Chart_Report.objects.order_by('pk')
    monitor_charts ={'charts':chart_list, 'errorslist':errors_list}
    return render(request, "gnumonitor/index.html", context=monitor_charts)

# def errors(request):
#     errors_list = Data_Error.objects.order_by('pk')
#     system_errors ={'errorslist':errors_list}
#     return render(request, "gnumonitor/index.html", context=system_errors)

def add_chart_form(request):
    form = ChartForm()

    if request.method =="POST":
        form = forms.ChartForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            #return index(request)
            return HttpResponseRedirect("/")
        else:
            print("ERROR FORM INVALID")
    return render(request, 'gnumonitor/chart_form.html', {'form':form})


def chartlist(request):
    chart_list = Chart_Report.objects.order_by('pk')
    chart_dict ={'chartlist':chart_list}
    return render(request, "gnumonitor/datalist.html", context=chart_dict)


# Create your views here.

def hello(request):
    return HttpResponse('Hello World!')

def ajax_test(request):
    variable = {'variable': 'world'}
    return render(request, 'gnumonitor/ajax_test.html', context = variable )
