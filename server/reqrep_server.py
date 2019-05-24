import zmq
import sys
import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()
from gnumonitor.models import Host, Host_Data, Host_Error, Chart, Chart_Data, Chart_Error

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


def main():

    #### CONFIGURABLE VARIABLES ####
    port = "5556"

    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)


    ### Clear Char_Error and Host_Error every system restart ###


    context = zmq.Context()
    zmqsocket = context.socket(zmq.REP)
    zmqsocket.bind("tcp://*:%s" % port) #escuta a porta

    print("Server on!")
    print("waiting for agent...")
    while True:
        #  Wait for next request from client
        recivedJson = zmqsocket.recv_json()  #socket zmq.REP will block on recv unless it has received a request.
        print ("Received data: ", recivedJson)
        decodedJson = json.loads(recivedJson)

        ####### MENAGE AGENTS #######
        try:
            raw_host_name = decodedJson['host_name']
            raw_host_ip =decodedJson['host_ip']
        except:
            print('Error trying to read agent basic infos')

        if not Host.objects.filter(name=raw_host_name, ip=raw_host_ip).exists():
            ## CRETE NEW AGENT
            hostObject = Host.objects.create(name=raw_host_name, ip=raw_host_ip)
        else:
            ## GET OBJECT INSTACE OF THE AGENT
            hostObject = Host.objects.get(name=raw_host_name, ip=raw_host_ip)


        ## GETING AND SAVING HOST DATA WHEN EXIST
        if 'host_time' in decodedJson:
            try:
                raw_host_time = decodedJson['host_time']
                raw_cpu_percent = decodedJson['cpu_percent']
                raw_memory_percent = decodedJson['memory_percent']
                raw_disk_percent = decodedJson['disk_percent']
                Host_Data.objects.create(host_object=hostObject, host_time=raw_host_time, cpu_percent=raw_cpu_percent, memory_percent=raw_memory_percent, disk_percent=raw_disk_percent)
            except:
                print("Errro tring to collect and save Host Data")

        ## END MANAGEMENT OF AGENT ##


        raw_request_type = decodedJson['request_type']
        if raw_request_type == "data_to_monitor":
            chartsToMonitorListJson = requestJsonDataFormat()
            print(chartsToMonitorListJson)
            zmqsocket.send_json (chartsToMonitorListJson)


        elif raw_request_type == "new_data":
            old_charts_id_list = [] #just to compare at the end of the for
            new_data_list = decodedJson['new_data_list']

            for new_data in new_data_list:
                raw_datetime = new_data['datetime']
                print(raw_datetime)
                raw_chart_id = new_data['chart_id']
                chart_object = Chart.objects.get(pk=raw_chart_id)
                old_charts_id_list.append(raw_chart_id)
                raw_value = new_data['value']
                print(raw_value)

                if isinstance(raw_value, str) and "Error:" in raw_value:
                    if not Data_Error.objects.filter(chart_object=chart_object, error=raw_value).exists() :
                        raw_type = "Error"
                        data = Data_Error.objects.create(chart_object=chart_object, time=raw_datetime, error=raw_value, type = raw_type)
                else:
                    # salva no banco
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
                zmqsocket.send_json (jsonResponseOK)
            else:
                chartsToMonitorListJson = requestJsonDataFormat()
                print(chartsToMonitorListJson)
                zmqsocket.send_json (chartsToMonitorListJson)


if __name__ == "__main__":
    main()
