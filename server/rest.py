import json
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from django.core import serializers
from django.http import JsonResponse
from gnumonitor.models import Data_Chart

class RestFunctions(object):

    def Monitoring_Data(request):

        if request.method == "GET":
            # id_last_item = request.GET.get("id_last_item")
            # data = list(Data_Chart.objects.filter(id__gt=id_last_item).order_by("time").values())
            data = list(Data_Chart.objects.order_by("id_chart_id","id","time").values())

            return JsonResponse(data, safe=False)
