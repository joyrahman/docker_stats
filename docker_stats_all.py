#usage 
# python docker_stats.py 10 output.txt
import subprocess 
import re
#import datetime
from datetime import datetime
import sys
import time
import socket
def poll_data():
    #p = subprocess.Popen('docker stats --no-stream', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen('docker stats --all --format "table {{.ID}},{{.CPUPerc}},{{.MemUsage}},{{.NetIO}},{{.BlockIO}}" --no-stream', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #ts = datetime.datetime.utcnow()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #output = "{},".format(ts)
    hostname = (socket.gethostname())
    output = ""
    for line in p.stdout.readlines()[1:]:
        #data = re.split('\s+',line)
        data = line.rstrip('\n').split(',')
        key = data[0]
        cpu = data[1]
        mem = data[2]
        net = data[3]
        io = data[4]
        pk = "{}_{}".format(key,ts)
        if key in record:
           output += "{},{},{},{},{},{},{},{}\n".format(pk,ts,record[key],cpu,mem,net,io,hostname)
           #output += "{},{},{},{},{},{},{}\n".format(key,ts,record[key],cpu,mem,net,hostname)
    return output


if len(sys.argv) >=2:
    iteration = int(sys.argv[1]) #number of iterations
    file_name = sys.argv[2]
else:
    iteration = 60
    file_name = "result.txt"

p = subprocess.Popen('docker ps | grep "weaveworksdemos"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
record = {}
for line in p.stdout.readlines():
    data2 = re.split('\s+',line)
    key  = data2[0]
    value = data2[1].split('/')[1]
    record[key] = value

p = subprocess.Popen('docker ps | grep "mongo"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    data2 = re.split('\s+',line)
    key  = data2[0]
    value = data2[1]
    record[key] = value


### 2nd phase
# get the stats
# filter based on match with the list
# write ts, cont_id, cpu
f = open(file_name,'w')
for i in xrange(iteration):
    #output = `i` +"," + poll_data() + "\n"
    #output = `i` +"," + poll_data() 
    output = poll_data() 
    f.write(output)
    print ".",
    time.sleep(5)

f.close()
