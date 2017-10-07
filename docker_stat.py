import subprocess 
import re
import datetime
import sys
import time

def poll_data():
    p = subprocess.Popen('docker stats --no-stream', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ts = datetime.datetime.utcnow()
    output = "{},".format(ts)

    for line in p.stdout.readlines():
        data = re.split('\s+',line)
        key = data[0]
        cpu = data[1]
        if key in record:
           output += "{},{},".format(record[key],cpu)
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


### 2nd phase
# get the stats
# filter based on match with the list
# write ts, cont_id, cpu
f = open(file_name,'w')
for i in xrange(iteration):
    output = poll_data() + "\n"
    f.write(output)
    print ".",
    time.sleep(5)

f.close()
