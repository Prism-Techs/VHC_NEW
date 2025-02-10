from threading import Thread, Event, Timer
from time import sleep
import time

class RepeatTimer(Thread):

    def __init__(self, interval, runclass):
        self.stop_event = Event()
        self.interval = interval
        self.runclass=runclass
        self.runthread = True
        self.triggerIntervel = 0
        self.stop_event.clear()
        super(RepeatTimer, self).__init__()
        
    def dummyfn():
        print("hi")

    def run(self):
        while self.runthread  == True:
           while self.interval > 0 and self.runthread == True:
            INTERVAL =(1/self.interval)/2
            print("lp=")
            print(self.interval)
            timer = RepeatTimer(INTERVAL, self.dummyfn)
            timer.start()
            time.sleep(0.2)
            self.interval = round(self.interval - 0.2,2)
            print("event exeed")
            #timer.cancel()

            
    def stop(self):
        self.stop_event.set()
        self.stop_event.clear()

        
