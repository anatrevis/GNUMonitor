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

class RestFunctions(object):

    def Monitoring_Data(request):

        if request.method == "GET":

            #data = list(Data_Chart.objects.order_by("time").values())
            id_last_item = request.GET["id_last_item"]
            data = []

            if id_last_item == '0':

                #pegar ultimos 60 pontos de vcada grafico
                charts_list = list(Chart.objects.all())
                for chart_object in charts_list:
                    obj_data_chart = Chart_Data.objects.filter(chart_object=chart_object).order_by('-pk')[:1]
                    if obj_data_chart:
                        last_id_to_get = obj_data_chart[0].pk
                        last_id_to_get = last_id_to_get - 10
                        data.extend(list(Chart_Data.objects.filter(id__gt=last_id_to_get, chart_object=chart_object).order_by("time").values()))
            else:
                data = list(Chart_Data.objects.filter(id__gt=id_last_item).order_by("time").values())

            #return HttpResponse(id_last_item)
            return JsonResponse(data, safe=False)

    def delete_chart(request):
        if request.method == "GET":
            chart_pk_to_destroy = request.GET.get("chart_pk_to_destroy")
            Chart_Data.objects.filter(chart_object_id=chart_pk_to_destroy).delete();
            Chart_Report.objects.filter(chart_object_id=chart_pk_to_destroy).delete();
            Chart.objects.filter(pk=chart_pk_to_destroy).delete();
    #         #tag_to_delete = get_object_or_404(Tag, title=tag)
    #         #tag_to_delete.delete()
        return HttpResponse(chart_pk_to_destroy)


    def create_errors_list(request):
        errors = list(Chart_Report.objects.order_by("time").values())
        return JsonResponse(errors, safe=False)
