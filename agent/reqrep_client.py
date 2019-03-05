import zmq
import sys
import time

from faker import Faker

fakegen = Faker()

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)

#  Do 10 requests, waiting each time for a response
while True:
    time.sleep (3)
    print ("Sending request...")
    fake_time = fakegen.date_time()
    fake_throughput = fakegen.random_number()
    socket.send_string ("Data: { Througput: " + str(fake_throughput) +", Time: " + str(fake_time) + "}")
    #  Get the reply.
    message = socket.recv()
    print ("Received reply ", "[", message, "]")
