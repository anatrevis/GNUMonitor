import zmq
import sys
import time
import json
import xmlrpc.client
from datetime import datetime

#from faker import Faker

#fakegen = Faker()
client = xmlrpc.client.ServerProxy("http://192.168.56.2:8080")
requestedList = []

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port) #conecta ao servidor

while True:
    if not requestedList:
        requestToSendJson = json.dumps({'request_type':'data_to_monitor'})
        print (requestToSendJson)
        socket.send_json(requestToSendJson)

        recivedJson = socket.recv_json()
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
                collectedValue = eval("client.get_" + monitorChart["command_line"] + "()")
                #collectedValue = eval("client.get_" + "user_throughput()")
                valuesList.append(collectedValue)

            except Exception as e:
                print(e)
                exception_error = "Error:"+str(e)
                valuesList.append(exception_error)

            datetimeList.append(str(datetime.now()))
            idChartList.append(monitorChart["chart_id"])

        #se tem dado coletado ou erro:
        if len(valuesList) > 0 :
            monitoredDataList = {"request_type":"new_data",
                                "new_data_list":[
                                    {"chart_id": id,
                                    "datetime": dt,
                                    "value":val} for id, dt, val in zip(idChartList, datetimeList, valuesList)]}
            monitoredDataListJson = json.dumps(monitoredDataList)
            print("Sent data:", monitoredDataListJson)
            socket.send_json (monitoredDataListJson)

            jsonResponse = socket.recv_json() #socket zmq.REQ will block on send unless it has successfully received a reply back.
            print ("Received reply: ", jsonResponse)
            responseDecodedJson = json.loads(jsonResponse)
            if "charts_to_monitor_list" in responseDecodedJson:
                requestedList = responseDecodedJson["charts_to_monitor_list"]
                print("Monitored List of Charts Updated!")
            if "request_result" in responseDecodedJson:
                print(responseDecodedJson["request_result"])


        #end-for
        time.sleep (1)
