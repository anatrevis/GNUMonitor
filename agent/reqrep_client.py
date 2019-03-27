import zmq
import sys
import time
import json
import xmlrpc.client
from datetime import datetime

#from faker import Faker

#fakegen = Faker()
client = xmlrpc.client.ServerProxy("http://192.168.56.2:8080")

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)

while True:
    time.sleep (1)
    print ("Sending request...")
    timenow = str(datetime.now())
    print (timenow)
    throughput = client.get_user_throughput()
    toSendJson = json.dumps({'throughput': throughput, 'datetime': timenow})
    print (toSendJson)
    socket.send_json(toSendJson)
    #fake_time = str(fakegen.date_time())
    #fake_throughput = fakegen.random_number()
    #socket.send_string ("Data: {Througput: " + str(fake_throughput) +", Time: " + str(fake_time) + "}")
    #  Get the reply.
    message = socket.recv()
    print ("Received reply ", "[", message, "]")
