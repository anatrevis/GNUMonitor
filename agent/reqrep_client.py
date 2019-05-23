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
port = "5556"
serverIp = "localhost"



def connect_to_server(zmqsocket):
    #socket.close()
    print ("Connecting to server...")
    zmqsocket.connect("tcp://localhost:%s" % port) #conecta ao servidor



def main():
    hostName = ''
    hostIp=''
    if len(sys.argv) > 2:
        serverIp = sys.argv[1]
        port =  sys.argv[2]
        int(port)
    try:
        hostName = socket.gethostname()
        hostIp = socket.gethostbyname(hostName)
        #hostName = "Ana Linda"
        #:hostIp = "666.666.1997.09"

        print("Hostname :  ",hostName)
        print("IP : ",hostIp)
    except:
        print("Unable to get Hostname and IP") \


    client = xmlrpc.client.ServerProxy("http://localhost:8080")
    requestedList = []
    context = zmq.Context()
    zmqsocket = context.socket(zmq.REQ)

    connect_to_server(zmqsocket)
    cpuPercent = 0
    memoryPercent = 0
    diskPercent = 0
    hostTime = 0

    while True:
        try:
            cpuPercent = psutil.cpu_percent()
        except:
            pass
        try:
            memoryPercent = psutil.virtual_memory()[2]
        except:
            pass
        try:
            diskPercent = psutil.disk_usage('/')[3]
        except:
            pass
        try:
            hostTime = str(datetime.now())
        except:
            pass

        if not requestedList:
            requestToSendJson = json.dumps({
                            'host_name':hostName,
                            'host_ip':hostIp,
                            'request_type':'data_to_monitor'
                            })
            print (requestToSendJson)
            zmqsocket.send_json(requestToSendJson)

            recivedJson = zmqsocket.recv_json()
            #print(recivedJson)
            requestedDecodedJson = json.loads(recivedJson)
            if "charts_to_monitor_list" in requestedDecodedJson:
                requestedList = requestedDecodedJson["charts_to_monitor_list"]
            print (requestedList)
            time.sleep (3)
        else:
            valuesList, datetimeList, idChartList = [], [], []
            for monitorChart in requestedList:
                try:
                    #collectedValue = eval("client.get_" + monitorChart["command_line"] + "()")
                    #collectedValue = eval("client.get_" + "user_throughput()")
                    collectedValue = random.randint(1, 100)

                    valuesList.append(collectedValue)

                except Exception as e:
                    print(e.errno)
                    if e.errno == 61:
                        exception_error = "Warning: GNU-Radio is not running"

                    else:
                        exception_error = "Error:"+str(e)

                    valuesList.append(exception_error)

                datetimeList.append(str(datetime.now()))
                idChartList.append(monitorChart["chart_id"])

            #se tem dado coletado ou erro:
            if len(valuesList) > 0 :
                monitoredDataList = {"host_name":hostName,
                                    "host_ip":hostIp,
                                    "host_time":hostTime,
                                    "cpu_percent":cpuPercent,
                                    "memory_percent":memoryPercent,
                                    "disk_percent":diskPercent,
                                    "request_type":"new_data",
                                    "new_data_list":[
                                        {"chart_id": id,
                                        "datetime": dt,
                                        "value":val} for id, dt, val in zip(idChartList, datetimeList, valuesList)]}
                monitoredDataListJson = json.dumps(monitoredDataList)
                print("Sent data:", monitoredDataListJson)
                zmqsocket.send_json (monitoredDataListJson)

                jsonResponse =  zmqsocket.recv_json() #socket zmq.REQ will block on send unless it has successfully received a reply back.
                print ("Received reply: ", jsonResponse)
                responseDecodedJson = json.loads(jsonResponse)
                if "charts_to_monitor_list" in responseDecodedJson:
                    requestedList = responseDecodedJson["charts_to_monitor_list"]
                    print("Monitored List of Charts Updated!")
                if "request_result" in responseDecodedJson:
                    print(responseDecodedJson["request_result"])


            #end-for
            time.sleep (5)


if __name__ == "__main__":
    main()
