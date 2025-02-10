import schedule
import threading
from time import sleep
import time

class TaskScheduler:

    def __init__(self, interval, runclass):
        self.interval = interval
        self.runclass=runclass
        self.isStarted = False
        self.runthread = True
        self.paused = False
        self.delay = False
      
    def run(self):
         self.isStarted = True
         
         while self.runthread:
            while not self.paused:
                schedule.run_pending()
                time.sleep(self.interval)     
            
             
    def start(self):
        if not self.isStarted :
             self.run()
        else : self.resume()

    def addjob(self,job):
        schedule.every(self.interval).seconds.do(self.runclass.periodic_event)   
   
    def pause(self):
         self.runthread = False
       #  schedule.cancel_job()     
    
    def resume(self):
        self.runthread = True
        #schedule.run_pending()
         
        
        
