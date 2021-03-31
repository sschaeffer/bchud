from time import time, sleep 
from datetime import datetime, timedelta

class BCTimer():

    def __init__(self, start=0):
        self.start=start
        self.update=self.start
        self.timestart = time()

    def delta(self):
        return time() - self.timestart        

    def printdelta(self):
        sec = timedelta(seconds=int(self.delta()))
        d = datetime(0,0,0)+sec
        print("%d:%d:%d:%d" % (d.day-1,d.hour, d.minute, d.second))

    def printtotal(self):
        sec = timedelta(seconds=int((self.update/20)+self.delta()))
        d = datetime(0,0,0)+sec
        print("%d:%d:%d:%d" % (d.day-1,d.hour, d.minute, d.second))

    def total(self):
        sec = timedelta(seconds=int((self.update/20)+self.delta()))
        d = datetime(1,1,1)+sec
        return("%d:%d:%d:%d" % (d.day-1,d.hour, d.minute, d.second))

    def restart(self,update=0):
        self.update = update
        self.timestart = time()