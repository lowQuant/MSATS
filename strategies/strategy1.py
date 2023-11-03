import time
from shared_resources import ib, add_log, start_event

def strategy1():
    add_log("Strategy1 Thread Started")
    start_event.wait()
    add_log("Executing Strategy 1")
    while True:
        time.sleep(10)
        add_log("S1: Placing a Buy Order in MSFT")
