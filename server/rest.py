import json
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from django.core import serializers
from django.http import JsonResponse
from gnumonitor.models import Sys_Report, Host, Host_Data, Host_Report, Chart, Chart_Data, Chart_Report
from django.http import HttpResponse
hostObject= None

class RestFunctions(object):

    def Monitoring_Hosts (request):
        global hostObject
        if request.method == "GET":
            id_last_host = request.GET["id_last_host"]
            hosts = list(Host.objects.filter(id__gt=id_last_host).order_by('pk').values())
            if id_last_host == 0 and hosts:
                id_selected_host = hosts[0].pk
                hostObject = Host.objects.get(pk=id_selected_host)
            return JsonResponse(hosts, safe=False)

    def Monitoring_Hosts_Data (request):
        if request.method == "GET":
            id_last_host_data = request.GET["id_last_host_data"]
            hosts_data=(list(Host_Data.objects.filter(id__gt=id_last_host_data).order_by("time").values()))
            return JsonResponse(hosts_data, safe=False)

    def Monitoring_Charts (request):
        global hostObject
        if request.method == "GET":
            id_selected_host = request.GET["id_selected_host"]
            charts = []
            if int(id_selected_host) > 0:
                hostObject = Host.objects.get(pk=id_selected_host)
                charts = list(Chart.objects.filter(host_object=hostObject).order_by('pk').values())
            return JsonResponse(charts, safe=False)


    def Monitoring_Data(request):
        if request.method == "GET":
            id_last_item = request.GET["id_last_item"]
            data = []
            charts_list = list(Chart.objects.filter(host_object=hostObject))
            for chart_object in charts_list:
                obj_data_chart = Chart_Data.objects.filter(chart_object=chart_object).order_by('-pk')[:1]
                if obj_data_chart:
                    if id_last_item == '0':
                    #pegar ultimos 60 pontos de vcada grafico
                        last_id_to_get = obj_data_chart[0].pk
                        last_id_to_get = last_id_to_get - 10
                        data.extend(list(Chart_Data.objects.filter(id__gt=last_id_to_get, chart_object=chart_object).order_by("time").values()))
                    else:
                        data.extend(list(Chart_Data.objects.filter(id__gt=id_last_item, chart_object=chart_object).order_by("time").values()))
            return JsonResponse(data, safe=False)

    def delete_chart(request):
        if request.method == "GET":
            chart_pk_to_destroy = request.GET.get("chart_pk_to_destroy")
            Chart_Data.objects.filter(chart_object_id=chart_pk_to_destroy).delete();
            Chart_Report.objects.filter(chart_object_id=chart_pk_to_destroy).delete();
            Chart.objects.filter(pk=chart_pk_to_destroy).delete();
        return HttpResponse(chart_pk_to_destroy)


    def Charts_Notifications(request):
        global hostObject
        if request.method == "GET":
            id_selected_host = request.GET["id_selected_host"]
            charts_notes = []
            if int(id_selected_host) > 0:
                hostObject = Host.objects.get(pk=id_selected_host)
                charts = Chart.objects.filter(host_object=hostObject).order_by('pk')
                for chart in charts:
                    charts_notes.extend(list(Chart_Report.objects.filter(chart_object=chart).order_by("time").values()))

            return JsonResponse(charts_notes, safe=False)

    def Hosts_Notifications(request):
        global hostObject
        if request.method == "GET":
            id_selected_host = request.GET["id_selected_host"]
            hosts_notes = []
            if int(id_selected_host) > 0:
                 hostObject = Host.objects.get(pk=id_selected_host)
                 hosts_notes.extend(list(Host_Report.objects.filter(host_object=hostObject).order_by("time").values()))

            return JsonResponse(hosts_notes, safe=False)

    def Sys_Notifications(request):
        global hostObject
        if request.method == "GET":
            sys_notes = []
            sys_notes.extend(list(Sys_Report.objects.all().order_by("time").values()))
        return JsonResponse(sys_notes, safe=False)
