import zmq
import sys
import time
import json
import xmlrpc.client
from datetime import datetime
import socket
import psutil
import random

#### CONFIGURABLE VARIABLES ####
serverPort = "5556"
serverIp = "localhost"
retryConnectionInterval = 3
monitoringInterval = 1

#### GLOBAL VARIABLES ####
gnuRadioClient = None
zmqSocket = None
hostName = ''
hostIp = ''
requestedChartList = []


def connect_to_server():
    global zmqSocket, serverIp, serverPort
    #socket.close()
    print ("Connecting to server...")
    context = zmq.Context()
    zmqSocket = context.socket(zmq.REQ)
    zmqSocket.connect("tcp://%s:%s" % (serverIp, serverPort)) #conecta ao servidor


def connect_to_gnuradio():
    global gnuRadioClient
    gnuRadioClient = xmlrpc.client.ServerProxy("http://localhost:8080")


def process_server_response(jsonResponse):
    global requestedChartList, hostIp, hostName
    print ("Received reply: ", jsonResponse)
    responseDecodedJson = json.loads(jsonResponse)
    if responseDecodedJson['host_ip'] == hostIp and responseDecodedJson['host_name'] == hostName:
        # VERIFY FOR EACH RESPONSE IF A CHART DATA TO MONITOR WAS UPDATED
        if "charts_to_monitor_list" in responseDecodedJson:
            requestedChartList = responseDecodedJson["charts_to_monitor_list"]
            print("Monitored List of Charts Updated!")
        if "request_return" in responseDecodedJson:
            print(responseDecodedJson["request_return"])


def chart_report_to_server(chartId, etype, description):
    global zmqSocket, hostName, hostIp
    requestToSendJson = json.dumps({
        'host_name':hostName,
        'host_ip':hostIp,
        'request_type':'report',
        'chart_report':{
            'chart_id':chartId,
            'description':description,
            'etype':etype,
            'time':str(datetime.now())
            }
        })
    print (requestToSendJson)
    zmqSocket.send_json(requestToSendJson)
    process_server_response(zmqSocket.recv_json()) #THIS IS NECESSARY TO NOT CRASH ZMQ WORKING ROUTINE


def host_report_to_server(etype, description):
    global zmqSocket, hostName, hostIp
    requestToSendJson = json.dumps({
        'host_name':hostName,
        'host_ip':hostIp,
        'request_type':'report',
        'host_report':{
            'description':description,
            'etype':etype,
            'time':str(datetime.now())
            }
        })
    print (requestToSendJson)
    zmqSocket.send_json(requestToSendJson)
    process_server_response(zmqSocket.recv_json()) #THIS IS NECESSARY TO NOT CRASH ZMQ WORKING ROUTINE


def sys_report_to_server(etype, description):
    global zmqSocket, hostName, hostIp
    requestToSendJson = json.dumps({
        'host_name':hostName,
        'host_ip':hostIp,
        'request_type':'report',
        'sys_report':{
            'description':description,
            'etype':etype,
            'time':str(datetime.now())
            }
        })
    print (requestToSendJson)
    zmqSocket.send_json(requestToSendJson)
    process_server_response(zmqSocket.recv_json()) #THIS IS NECESSARY TO NOT CRASH ZMQ WORKING ROUTINE


def define_credentials():
    global hostIp, hostName
    ### GET AGENT NAME/IP CREDENTIALS ###
    try:
        hostName = socket.gethostname()
        hostIp = socket.gethostbyname(hostName)
        #hostName = "Ana Linda"
        #hostIp = "666.666.1997.09"
        print("Hostname :  ",hostName)
        print("IP : ",hostIp)
    except:
        ### REPORT ERROR TO SERVER ###
        print("Unable to get Hostname and IP")
        sys_report_to_server('Warning', 'One or more agents are attempting to connect without Name/IP credentials.')
        #return 0
        sys.exit(1)


def request_new_chart_list():
    global requestedChartList, zmqSocket, hostName, hostIp
    requestToSendJson = json.dumps({
        'host_name':hostName,
        'host_ip':hostIp,
        'request_type':'data_to_monitor'
        })
    #print (requestToSendJson)
    zmqSocket.send_json(requestToSendJson)
    recivedJson = zmqSocket.recv_json()
    #print(recivedJson)
    requestedDecodedJson = json.loads(recivedJson)
    if "charts_to_monitor_list" in requestedDecodedJson:
        if requestedDecodedJson['host_ip'] == hostIp and requestedDecodedJson['host_name'] == hostName:
            requestedChartList = requestedDecodedJson["charts_to_monitor_list"]
            print(requestedChartList)


def send_chart_and_host_data_to_server(valuesList, idChartList, cpuPercent, memoryPercent, diskPercent):
    global hostName, hostIp, zmqSocket
    timeNow = str(datetime.now())
    monitoredDataList = {"host_name":hostName,
        "host_ip":hostIp,
        "host_time":timeNow,
        "cpu_percent":cpuPercent,
        "memory_percent":memoryPercent,
        "disk_percent":diskPercent,
        "request_type":"new_data",
        "new_data_list":[
            {"chart_id": id,
            "datetime": timeNow,
            "value":val} for id, val in zip(idChartList, valuesList)]}
    monitoredDataListJson = json.dumps(monitoredDataList)
    print("Sent data:", monitoredDataListJson)
    zmqSocket.send_json(monitoredDataListJson)

    process_server_response(zmqSocket.recv_json()) #socket zmq.REQ will block on send unless it has successfully received a reply back.


def send_chart_data_to_server(valuesList, idChartList):
    global hostName, hostIp, zmqSocket
    timeNow = str(datetime.now())
    monitoredDataList = {"host_name":hostName,
        "host_ip":hostIp,
        "host_time":timeNow,
        "request_type":"new_data",
        "new_data_list":[
            {"chart_id": id,
            "datetime": timeNow,
            "value":val} for id, val in zip(idChartList, valuesList)]}
    monitoredDataListJson = json.dumps(monitoredDataList)
    print("Sent data:", monitoredDataListJson)
    zmqSocket.send_json(monitoredDataListJson)

    process_server_response(zmqSocket.recv_json()) #socket zmq.REQ will block on send unless it has successfully received a reply back.


def send_host_data_to_server(cpuPercent, memoryPercent, diskPercent):
    global hostName, hostIp, zmqSocket
    timeNow = str(datetime.now())
    monitoredDataList = {"host_name":hostName,
        "host_ip":hostIp,
        "host_time":timeNow,
        "cpu_percent":cpuPercent,
        "memory_percent":memoryPercent,
        "disk_percent":diskPercent,
        "request_type":"new_data"}
    monitoredDataListJson = json.dumps(monitoredDataList)
    print("Sent data:", monitoredDataListJson)
    zmqSocket.send_json(monitoredDataListJson)

    process_server_response(zmqSocket.recv_json()) #socket zmq.REQ will block on send unless it has successfully received a reply back.


def main():
    global serverIp, serverPort, requestedChartList, retryConnectionInterval, monitoringInterval

    if len(sys.argv) > 2:
        serverIp = sys.argv[1]
        serverPort =  sys.argv[2]

    connect_to_gnuradio()
    connect_to_server()
    define_credentials()

    while True:

        if not requestedChartList:
            ### REQUEST COMMANDS TO MONITOR ###
            request_new_chart_list()
            time.sleep (retryConnectionInterval)
        else:
            try:
                ### COLECT HOST DATA ###
                cpuPercent = psutil.cpu_percent()
                memoryPercent = psutil.virtual_memory()[2]
                diskPercent = psutil.disk_usage('/')[3]
            except:
                ### REPORT ERROR TO SERVER ###
                host_report_to_server('Warning', 'The agent are unable to provide monitored host data.')

            ### COLLECT GNURADIO DATA ###
            valuesList, idChartList = [], []
            for monitorChart in requestedChartList:
                try:
                    #collectedValue = eval("client.get_" + monitorChart["command_line"] + "()")
                    #collectedValue = eval("client.get_" + "user_throughput()")
                    collectedValue = random.randint(1, 100)
                except Exception as e:
                    ### REPORT ERROR TO SERVER ###
                    #print(e.errno)
                    if e.errno == 61:
                        host_report_to_server('Warning', 'GNU-Radio is not running')
                        break
                    else:
                        chart_report_to_server(monitorChart["chart_id"],'Error', str(e))
                        collectedValue = 'null' #JUST TO NOT BROKE THE DATA AND CHART ID LIST ORDER

                valuesList.append(collectedValue)
                idChartList.append(monitorChart["chart_id"])
            #end-for
            if len(valuesList) > 0 :
                if cpuPercent and memoryPercent and diskPercent:
                    #IF I HAVE CHART AND HOST DATA
                    send_chart_and_host_data_to_server(valuesList, idChartList, cpuPercent, memoryPercent, diskPercent)
                else:
                    #IF I HAVE JUST CHART DATA
                    send_chart_data_to_server(valuesList, idChartList)
            else:
                if cpuPercent and memoryPercent and diskPercent:
                    #IF I HAVE JUST HOST DATA
                    send_host_data_to_server(cpuPercent, memoryPercent, diskPercent)

            time.sleep (monitoringInterval)


if __name__ == "__main__":
    main()
