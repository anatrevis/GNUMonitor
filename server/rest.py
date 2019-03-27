import json
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from django.core import serializers
from django.http import JsonResponse
from gnumonitor.models import MonitorData

class RestFunctions(object):

    def Monitoring_Data(request):

        if request.method == "GET":
            id_last_item = request.GET["id_last_item"]
            data = list(MonitorData.objects.filter(id__gt=id_last_item).order_by("time").values())

            return JsonResponse(data, safe=False)
