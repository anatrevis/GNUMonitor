import zmq
import sys
import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from gnumonitor.models import Chart, Data_Chart

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

print("server on!")
while True:
    #  Wait for next request from client
    recivedJson = socket.recv_json()
    print ("Received data: ", recivedJson)
    decodedJson = json.loads(recivedJson)
    raw_throughput = decodedJson['throughput']
    print(raw_throughput)
    raw_datetime = decodedJson['datetime']
    print(raw_datetime)

    # salva no banco
    data = MonitorData.objects.get_or_create(id_chart=id_chart, time=raw_datetime, value=raw_throughput)[0]

    socket.send_string ("Success!")
