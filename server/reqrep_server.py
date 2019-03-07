import zmq
import sys
import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from gnumonitor.models import MonitorData

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

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
    data = MonitorData.objects.get_or_create(time=raw_datetime, throughput=raw_throughput)[0]

    socket.send_string ("Success!")
