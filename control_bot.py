import os
#system.run["service DeliveryBot status | grep -v grep | grep 'running' | wc -l"]
#def status(proc):
#    status = os.popen(f"systemctl status {proc}.service").read()
#    return status
def status(proc):
    status = os.popen(f"service {proc} status | grep -v grep | grep 'running' | wc -l").read()
    return status

def stop(proc):
    stop = os.popen(f"systemctl stop {proc}.service").read()
    return stop

def start(proc):
    start = os.popen(f"systemctl start {proc}.service").read()
    return start