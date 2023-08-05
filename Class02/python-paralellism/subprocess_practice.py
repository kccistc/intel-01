import time
import subprocess
import os
import psutil

print("Subprocess running ... PID:{}, PPID:{}".format(os.getpid(), psutil.Process(os.getpid()).ppid()), flush=True)
time.sleep(1)
print("Subprocess done")