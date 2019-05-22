import zmq
import sys
import os
import json
from urllib.request import urlopen
import time
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()
from gnumonitor.models import Chart, Data_Chart, Data_Error


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=10)
        print("INTERNET ON")
        return True
    except:
        print("INTERNET OFF")
        Data_Error.objects.create(time=datetime.now(), description="Error: No internet connection", type = "Error")
        return False


def requestJsonDataFormat():
    chartsId, commandLines = [], []
    chartObjectList = Chart.objects.order_by('pk')
    for chartObject in chartObjectList:
        chartsId.append(chartObject.pk)
        commandLines.append(chartObject.parameter)

    chartsToMonitorList = {"charts_to_monitor_list":[{"chart_id": id, "command_line":c} for id, c in zip(chartsId, commandLines)]}
    # Printing in JSON format
    chartsToMonitorListJson = json.dumps(chartsToMonitorList)
    print(chartsToMonitorListJson)
    return chartsToMonitorListJson



port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port) #escuta a porta

if not Data_Error.objects.filter(description="Warning: No client connection").exists() :
    Data_Error.objects.create(time=datetime.now(), description="Warning: No client connection", type = "Warning")

internet_on()

print("Server on!")
print("waiting for agent...")
while True:
    # state = socket.recv()
    # try:
    #     if state != "":
    #         time.sleep (1)
    #         print ("State: ", state)
    # except:
    #     print("Connection with agent has failed.")
    # #
    # # if state != "":
    # #     time.sleep (1)
    # #     socket.send_string("port %s" % port)
    # # else:
    # #     print("Connection with agent has failed.")



     #Wait for next request from client
    recivedJson = socket.recv_json()  #socket zmq.REP will block on recv unless it has received a request.

    #remive da base oq cliente conectou
    Data_Error.objects.filter(description="Warning: No client connection").delete()

    print ("Received data: ", recivedJson)
    decodedJson = json.loads(recivedJson)
    raw_request_type = decodedJson['request_type']
    if raw_request_type == "data_to_monitor":
        chartsToMonitorListJson = requestJsonDataFormat()
        print(chartsToMonitorListJson)
        socket.send_json (chartsToMonitorListJson)


    elif raw_request_type == "new_data":
        old_charts_id_list = [] #just to compare at the end of the for
        new_data_list = decodedJson['new_data_list']

        for new_data in new_data_list:
            raw_datetime = new_data['datetime']
            print(raw_datetime)
            raw_chart_id = new_data['chart_id']
            if not raw_chart_id is None:
                try:
                    print (raw_chart_id)
                    chart_object = Chart.objects.get(pk=raw_chart_id)
                    old_charts_id_list.append(raw_chart_id)
                    raw_value = new_data['value']
                    print(raw_value)
                except Exception as e:
                    break

            if isinstance(raw_value, str) and "Error:" in raw_value:
                if not Data_Error.objects.filter(chart_object=chart_object, description=raw_value).exists() :
                    print(raw_value)
                    raw_type = "Error"
                    data = Data_Error.objects.create(chart_object=chart_object, time=raw_datetime, description=raw_value, type = raw_type)
            elif isinstance(raw_value, str) and "Warning:" in raw_value:
                if not Data_Error.objects.filter(chart_object=chart_object, description=raw_value).exists() :
                    print(raw_value)
                    raw_type = "Warning"
                    data = Data_Error.objects.create(chart_object=chart_object, time=raw_datetime, description=raw_value, type = raw_type)
            else:
                # salva no banco
                if Data_Error.objects.filter(description= "Warning: GNU-Radio is not running").exists() :
                    print('DELETANDO O ERRO')
                    Data_Error.objects.filter(description= "Warning: GNU-Radio is not running").delete() #se o gnuradio voltar a rodar exclui o erro que ele nao estava rodando
                data = Data_Chart.objects.create(chart_object=chart_object, time=raw_datetime, value=raw_value)

        #verica se houve alteracao na lista de graficos monitorados
        charts_list_pk = Chart.objects.order_by('pk')
        print("\n\n", charts_list_pk, "\n\n")
        new_charts_id_list = []
        for item in charts_list_pk:
            new_charts_id_list.append(item.id)
        # sorting both the lists
        old_charts_id_list.sort()
        new_charts_id_list.sort()
        print("Old:", old_charts_id_list)
        print("New:", new_charts_id_list)
        # using == to check if lists are equal
        if old_charts_id_list == new_charts_id_list:
            jsonResponseOK = json.dumps({"request_result":"New data added!"})
            socket.send_json (jsonResponseOK)
        else:
            chartsToMonitorListJson = requestJsonDataFormat()
            print(chartsToMonitorListJson)
            socket.send_json (chartsToMonitorListJson)
