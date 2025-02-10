from threading import Thread, Event
import threading
from time import sleep
import time

class PeriodicThread(Thread):

    def __init__(self, interval, runclass):
        self.stop_event = Event()
        self.interval = interval
        self.runclass=runclass
        self.isStarted = False
        self.runthread = True
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.stop_event.clear()
        self.delay = False
        super(PeriodicThread, self).__init__()

    def run(self):
         self.isStarted = True
         
         while self.runthread:
            while self.paused:
                self.pause_cond.wait()     
             
            #thread is running
            self.runclass.periodic_event()
            time.sleep(self.interval)
            
    def start(self):
        threading.Thread.start(self)
                 
    def terminate(self):
        self.stop_event.set()

    def stop(self):
        self.stop_event.set()
        self.stop_event.clear()
        self.runthread = False

    def isStarted(self):
        return self.isStarted
    
    def kill(self):
      self.killed = True

    def pause(self):
        
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()
        
        self.paused = True
         
    #should just resume the thread
    def resume(self):

        # Notify so thread will wake after lock released
         self.pause_cond.notify()
         
         self.paused = False
            # Now release the lock
         self.pause_cond.release()

         
        
        
