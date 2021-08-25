import os

def status(proc):
    status = os.popen(f"systemctl status {proc}.service").read()
    return status

def stop(proc):
    stop = os.popen(f"systemctl stop {proc}.service").read()
    return stop

def start(proc):
    start = os.popen(f"systemctl start {proc}.service").read()
    return start