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
longTimeConnection = 1

#### GLOBAL VARIABLES ####
#zmqSocket = None

## STRING DEFINITIONS ##
reportError = 'Error'
reportInfo = 'Info'
reportWarning = 'Warning'
reportSuccess = 'Success'
reportNoHost ='Waiting for agent connection'
reportNoChart = 'Please add a chart to start monitoring in this agent'
reportNoConnection = 'This agent does not connect for a long time'
reportNoChartData = 'No data to display'

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
            Host_Report.objects.create(host_object=hostObject, description=rawReportDescription,etype=rawReportEtype,time=str(datetime.now()))
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


def clear_all_notifications():
    Sys_Report.objects.all().delete()
    Host_Report.objects.all().delete()
    Chart_Report.objects.all().delete()


def manage_notifications():
    ### WATING FOR CLIENT ###
    if not Host.objects.all().exists() and not Sys_Report.objects.filter(etype=reportInfo, description=reportNoHost).exists():
        Sys_Report.objects.create(etype=reportInfo,description=reportNoHost, time=str(datetime.now()))
    elif Host.objects.all().exists():
        try:
            Sys_Report.objects.filter(etype=reportInfo,description=reportNoHost).delete()
        except:
            pass

    listHosts = list(Host.objects.all())
    for hostObject in listHosts:
        ### ADD A CHART TO MONITOR ###
        if not Chart.objects.filter(host_object=hostObject).exists() and not Host_Report.objects.filter(host_object=hostObject, etype=reportInfo, description=reportNoChart).exists():
            Host_Report.objects.create(host_object=hostObject, etype=reportInfo, description=reportNoChart, time=str(datetime.now()))
        elif Chart.objects.filter(host_object=hostObject).exists():
            try:
                Host_Report.objects.filter(host_object=hostObject, etype=reportInfo, description=reportNoChart).delete()
            except:
                pass

#        lastConnection = Host_Data.objects.filter(host_object=hostObject).order_by('time')[0]
#        print (lastConnection.time)

#        if lastConnection:
#            lastTimeConnection = datetime.strptime(str(lastConnection.time).split('+')[0], '%Y-%m-%d %H:%M:%S.%f')
            ### HOST LOG TIME WITHOUT CONNECTIONS ###
#            print(datetime.now() - lastTimeConnection)
#            if (datetime.now() - lastTimeConnection).minute >= longTimeConnection and not Host_Report.objects.filter(host_object=hostObject, etype=reportWarning, description=reportNoConnection).exists():
#                Host_Report.objects.create(host_object=hostObject, etype=reportWarning, description=reportNoConnection, time=str(datetime.now()))
#            elif (datetime.now() - lastTimeConnection).minute > longTimeConnection:
#                try:
#                    Host_Report.objects.filter(host_object=hostObject, etype=reportWarning, description=reportNoConnection).delete()
#                except:
#                    pass

        listCharts = Chart.objects.filter(host_object=hostObject)
        for chartObject in listCharts:
            ### NOT DATA TO EXIBI ###
            if not Chart_Data.objects.filter(chart_object=chartObject).exists() and not Chart_Report.objects.filter(chart_object=chartObject, etype=reportInfo, description=reportNoChartData).exists():
                Chart_Report.objects.create(chart_object=chartObject, etype=reportInfo, description=reportNoChartData, time=str(datetime.now()))
            elif Chart_Data.objects.filter(chart_object=chartObject).exists():
                try:
                    Chart_Report.objects.filter(host_object=hostObject, etype=reportInfo, description=reportNoChartData).delete()
                except:
                    pass


#def manage_host_notifications(hostObject)
#    listCharts = Chart.objects.filter(host_object=hostObject)
#
#    ### ADD A CHART TO MONITOR ###
#    if not Chat.objects.filter(host_object=hostObject).exists() and not Host_Report.objects.filter(host_object=hostObject, etype=reportInfo, description=reportNoChart).exists():
#        Hist_Report.objects.create(host_object=hostObject, etype=reportInfo, description=reportNoChart, time=str(datetime.now()))
#    else:
#        try:
#            Host_Report.objects.filter(host_object=hostObject, etype=reportInfo, description=reportNoChart).delete()
#        except:
#            pass


def main():
    global serverPort
    if len(sys.argv) > 1:
        serverPort =  sys.argv[1]

    #TODO: Clear Char_Error and Host_Error every system restart ###
    clear_all_notifications()

    zmqSocket = create_server()

    manage_notifications()
    while True:
        #  Wait for next request from client
        recivedJson = zmqSocket.recv_json()  #socket zmq.REP will block on recv unless it has received a request.
        print ("Received data: ", recivedJson)
        decodedJson = json.loads(recivedJson)

        hostObject = get_host_object(decodedJson)

        process_agent_request(zmqSocket, hostObject, decodedJson)

        manage_notifications()

if __name__ == "__main__":
    main()
