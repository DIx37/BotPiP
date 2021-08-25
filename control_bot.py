import os
#system.run["service DeliveryBot status | grep -v grep | grep 'running' | wc -l"]
#def status(proc):
#    status = os.popen(f"systemctl status {proc}.service").read()
#    return status
def status(proc):
    try:
        status = os.popen(f"service {proc} status | grep -v grep | grep 'running' | wc -l").read()
        status = status[0:1]
    except Exception:
        status = "N/A"
    return status

def stop(proc):
    try:
        stop = os.popen(f"systemctl stop {proc}.service").read()
    except Exception:
        stop = "N/A"
    return stop

def start(proc):
    try:
        start = os.popen(f"systemctl start {proc}.service").read()
    except Exception:
        start = "N/A"
    return start

def restart(proc):
    try:
        start = os.popen(f"systemctl restart {proc}.service").read()
    except Exception:
        start = "N/A"
    return start