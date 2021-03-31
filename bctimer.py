from time import time, sleep 
from datetime import datetime, timedelta

class BCTimer():

    def __init__(self, start=0):
        self.start=start
        self.timestart = time()
        print(self.timestart)

    def delta(self):
        return time() - self.timestart        

    def printdelta(self):
        sec = timedelta(seconds=int(self.delta()))
        d = datetime(1,1,1)+sec
        print("%d:%d:%d:%d" % (d.day-1,d.hour, d.minute, d.second))

    def printtotal(self):
        sec = timedelta(seconds=int((self.start/20)+self.delta()))
        d = datetime(1,1,1)+sec
        print("%d:%d:%d:%d" % (d.day-1,d.hour, d.minute, d.second))


bct = BCTimer(2073)
bct.printdelta()
bct.printtotal()
print("---")
sleep(1.0)
bct.printdelta()
bct.printtotal()
print("---")
sleep(1.0)
bct.printdelta()
bct.printtotal()