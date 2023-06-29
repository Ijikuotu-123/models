import threading
import time
global t
t=False
to_get=250
init_time=time.time()
def get_time():
    t=time.time()
    if((t-init_time)==to_get):
        global t
        t=True
secs=(t-init_time)%60
min=(t-init_time)//60    
print(time.time())
threading.thread(target=get_time)
