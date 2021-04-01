#!/usr/bin/python3

from nbt import NBTFile
from time import time, sleep 
from os import path
from datetime import datetime, timedelta
from subprocess import call

class BCTimer(NBTFile):

    def __init__(self):
        self.oldreadtime=0
        self.oldgametime=0
        self.olddaytime=0
        self.gametimediff=0
        self.daytimediff=0
        self.timepad=0
        self.readnbtfile()

    def readnbtfile(self):
        self.readtime = time()
        self.filename = path.join('/media/deflection/Minecraft/server/snapshot/snapshot','level.dat')
        super(BCTimer, self).__init__(self.filename)
        
    def nbtgametimestr(self):
        return str(self["Data"]["Time"])

    def nbtdaytimestr(self):
        return str(self["Data"]["DayTime"])

    def nbtgametime(self):
        return int(self.nbtgametimestr())

    def nbtdaytime(self):
        return (int(self.nbtdaytimestr())%24000)

    def nbtday(self):
        return (int(self.nbtdaytimestr())/24000)

    def nbtreadtime(self):
        return self.readtime

    def nbtreaddelta(self):
        return time()-self.nbtreadtime()

    def estgametime(self):
        return (self.nbtgametime()+(self.nbtreaddelta()*20)+self.timepad)

    def estdaytime(self):
        return (self.nbtdaytime()+(self.nbtreaddelta()*20)+self.timepad)%24000

    def oldreaddelta(self):
        return time()-self.oldreadtime

    def oldestgametime(self):
        return (self.oldgametime+(self.oldreaddelta()*20)+self.timepad)

    def oldestdaytime(self):
        return (self.olddaytime+(self.oldreaddelta()*20)+self.timepad)%24000

    def rereadnbtfile(self):
        self.oldreadtime = self.nbtreadtime()
        self.oldgametime = self.nbtgametime()
        self.olddaytime = self.nbtdaytime()
        call(["/home/integ/Code/stage/save-it-all.bash"])
        sleep(0.5)
        self.readnbtfile()
        self.gametimediff = self.oldestgametime() - self.estgametime()
        self.daytimediff = self.oldestdaytime() - self.estdaytime()

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


def main():
    print("BCTimer test")
    bct = BCTimer()
    print(bct.nbtgametimestr())
    print(bct.nbtgametime())
    print(bct.nbtdaytimestr())
    print(bct.nbtdaytime())
    print(bct.nbtday())
    print(str(bct.nbtreadtime()))
    print(str(bct.timepad))
    print(str(bct.nbtreaddelta()))
    sleep(5)
    print(str(bct.nbtreaddelta()))
    print(str(bct.estgametime()))
    print(str(bct.estdaytime()))
    bct.rereadnbtfile()
    print(bct.nbtgametime())
    print(bct.nbtdaytime())
    print(bct.daytimediff)
    print(bct.gametimediff)
    


if __name__ == '__main__':
    main()