
import time
from progress.bar import ChargingBar
import threading

i = 20
i_ = 20
def _():
    global i,i_
    with ChargingBar('Processing', max=i_) as bar:
        while True:
            if i_ - i > 0:
                for ___ in range(i_ - i):
                    
                    bar.next()
                i_ = i

def a():
    global i
    while True:
        time.sleep(0.1)
        i = i - 1



threading.Thread(target = _).start()

threading.Thread(target= a).start()

