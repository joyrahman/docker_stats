#usage 
# python docker_stats.py 10 output.txt
import subprocess 
import re
import datetime
import sys
import time

def poll_data():
    p = subprocess.Popen('docker stats --no-stream', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ts = datetime.datetime.utcnow()
    output = "{},".format(ts)

    for line in p.stdout.readlines()[1:]:
        data = re.split('\s+',line)
        key = data[0]
        cpu = data[2]
        print(data)
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

p = subprocess.Popen('docker ps | grep "mongo"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    data2 = re.split('\s+',line)
    key  = data2[0]
    value = data2[1]
    record[key] = value
print(record)


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
