import zmq
import sys
import os
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()
from gnumonitor.models import Sys_Report, Host, Host_Data, Host_Report, Chart, Chart_Data, Chart_Report

#### CONFIGURABLE VARIABLES ####
serverPort = "5556"

#### GLOBAL VARIABLES ####
#zmqSocket = None

def create_server():
    global serverPort
    context = zmq.Context()
    zmqSocket = context.socket(zmq.REP)
    zmqSocket.bind("tcp://*:%s" % serverPort) #LISTENING IN PORT
    print("Server on!")
    return zmqSocket


def create_json_charts_to_monitor_list(hostObject):
    chartsId, commandLines = [], []
    chartObjectList = Chart.objects.filter(host_object = hostObject).order_by('pk')
    for chartObject in chartObjectList:
        chartsId.append(chartObject.pk)
        commandLines.append(chartObject.parameter)

    chartsToMonitorList = {
        "host_ip":hostObject.ip,
        "host_name":hostObject.name,
        "charts_to_monitor_list":[{"chart_id": id, "command_line":c} for id, c in zip(chartsId, commandLines)]}
    # Printing in JSON format
    chartsToMonitorListJson = json.dumps(chartsToMonitorList)
    print(chartsToMonitorListJson)
    return chartsToMonitorListJson


def get_host_object(decodedJson):
    ####### MENAGE AGENTS #######
    if 'host_name' in decodedJson and 'host_ip' in decodedJson:
        try:
            rawHostName = decodedJson['host_name']
            rawHostIp =decodedJson['host_ip']
            if not Host.objects.filter(name=rawHostName, ip=rawHostIp).exists():
                ## CRETE NEW AGENT
                hostObject = Host.objects.create(name=rawHostName, ip=rawHostIp)
            else:
                ## GET OBJECT INSTACE OF THE AGENT
                hostObject = Host.objects.get(name=rawHostName, ip=rawHostIp)
            return hostObject
        except:
            print('Error trying to read agent basic infos')
            return None


def replay_data_to_monitor(zmqSocket, hostObject, decodedJson):
    chartsToMonitorListJson = create_json_charts_to_monitor_list(hostObject)
    print(chartsToMonitorListJson)
    zmqSocket.send_json(chartsToMonitorListJson)


def save_host_data(hostObject, decodedJson):
    ## GETING AND SAVING HOST DATA WHEN EXIST
    if 'cpu_percent' in decodedJson and 'memory_percent' in decodedJson and 'disk_percent' in decodedJson:
        try:
            #SAVING LOCAL TIME TO AVOID DIFERENT TIMES FROM MULTIPLE SYSTEMS
            rawCpuPercent = decodedJson['cpu_percent']
            rawMemoryPercent = decodedJson['memory_percent']
            rawDiskPercent = decodedJson['disk_percent']
            Host_Data.objects.create(host_object=hostObject, time=str(datetime.now()), cpu_percent=rawCpuPercent, memory_percent=rawMemoryPercent, disk_percent=rawDiskPercent)
        except:
            print("Errro tring to collect and save host data")


def save_chart_data(hostObject, decodedJson):
    if 'new_data_list' in decodedJson:
        rawDataList = decodedJson['new_data_list']
        for newData in rawDataList:
            rawChartId = newData['chart_id']
            if Chart.objects.filter(pk=rawChartId).exists():
                chartObject = Chart.objects.get(pk=rawChartId)
                rawValue = newData['value']
                #print(rawValue)
                if not isinstance(rawValue, str):
                    if not rawValue == 'null': #IF IT IS NOT NULL SAVE DATA
                        data = Chart_Data.objects.create(chart_object=chartObject, time=str(datetime.now()), value=rawValue)


def replay_new_data(zmqSocket, hostObject, decodedJson):
    if 'new_data_list' in decodedJson:
        oldChartsIdList = [] #I NEED THIS TO COMPARE AT THE END OF THE FOR
        #VERIFY IF IS NECESSARY TO INFORME NEW DATA TO MONITOR FOR THE AGENT
        rawDataList = decodedJson['new_data_list']
        for newData in rawDataList:
            oldChartsIdList.append(newData['chart_id'])

        chartsListPk = Chart.objects.order_by('pk')

        newChartsIdList = []
        for item in chartsListPk:
            newChartsIdList.append(item.id)

        # sorting both lists to compare
        oldChartsIdList.sort()
        newChartsIdList.sort()
        #print("Old:", old_charts_id_list)
        #print("New:", new_charts_id_list)

        # using == to check if lists are equal
        if oldChartsIdList == newChartsIdList:
            jsonResponseOK = json.dumps({
                "host_ip":hostObject.ip,
                "host_name":hostObject.name,
                "request_return":"New data added!"})
            zmqSocket.send_json (jsonResponseOK)
        else:
            chartsToMonitorListJson = create_json_charts_to_monitor_list(hostObject)
            #print(chartsToMonitorListJson)
            zmqSocket.send_json(chartsToMonitorListJson)
    else:
        jsonResponseOK = json.dumps({
            "host_ip":hostObject.ip,
            "host_name":hostObject.name,
            "request_return":"New data added!"})
        zmqSocket.send_json (jsonResponseOK)


def save_report(hostObject, decodedJson):
    if "sys_report" in decodedJson:
        rawReport = decodedJson['sys_report']
        rawReportDescription = rawReport['description']
        rawReportEtype = rawReport['etype']
        if not Sys_Report.objects.filter(description=rawReportDescription,etype=rawReportEtype).exists():
            Sys_Report.objects.create(description=rawReportDescription,etype=rawReportEtype,time=str(datetime.now()))
    elif "host_report" in decodedJson:
        rawReport = decodedJson['host_report']
        rawReportDescription = rawReport['description']
        rawReportEtype = rawReport['etype']
        if not Host_Report.objects.filter(host_object=hostObject,description=rawReportDescription,etype=rawReportEtype).exists():
            Host_Report.objects.create(description=rawReportDescription,etype=rawReportEtype,time=str(datetime.now()))
    elif "chart_report" in decodedJson:
        rawReport = decodedJson['chart_report']
        rawReportDescription = rawReport['description']
        rawReportEtype = rawReport['etype']
        rawCharId = rawReport['chart_id']
        chartObject = Chart.objects.get(pk=rawChartId)
        if not Chart_Report.objects.filter(chart_object=chartObject,description=rawReportDescription,etype=rawReportEtype).exists():
            Chart_Report.objects.create(chart_object=chartObject,description=rawReportDescription,etype=rawReportEtype,time=str(datetime.now()))


def replay_report(zmqSocket, hostObject):
    jsonResponseReport = json.dumps({
        "host_ip":hostObject.ip,
        "host_name":hostObject.name,
        "request_return":"Report received!"})
    zmqSocket.send_json(jsonResponseReport)


def process_agent_request(zmqSocket, hostObject, decodedJson):
    if 'request_type' in decodedJson:
        rawRequestType = decodedJson['request_type']
        if rawRequestType == "data_to_monitor":
            replay_data_to_monitor(zmqSocket, hostObject, decodedJson)
        elif rawRequestType == "new_data":
            save_host_data(hostObject, decodedJson)
            save_chart_data(hostObject, decodedJson)
            replay_new_data(zmqSocket, hostObject, decodedJson)
        elif rawRequestType == "report":
            save_report(hostObject, decodedJson)
            replay_report(zmqSocket, hostObject)


def main():
    global serverPort
    if len(sys.argv) > 1:
        serverPort =  sys.argv[1]

    #TODO: Clear Char_Error and Host_Error every system restart ###

    zmqSocket = create_server()

    while True:
        #  Wait for next request from client
        recivedJson = zmqSocket.recv_json()  #socket zmq.REP will block on recv unless it has received a request.
        print ("Received data: ", recivedJson)
        decodedJson = json.loads(recivedJson)

        hostObject = get_host_object(decodedJson)

        process_agent_request(zmqSocket, hostObject, decodedJson)


if __name__ == "__main__":
    main()
