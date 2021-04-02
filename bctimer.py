#!/usr/bin/python3

from nbt import NBTFile
from time import time, sleep 
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call

class BCTimer(NBTFile):

    def __init__(self):

        self.filename = "/media/deflection/Minecraft/server/snapshot/snapshot/level.dat"

        self.gametime=0
        self.daytime=0
        self.mtime=0

        self.oldgametime=0
        self.olddaytime=0
        self.oldmtime=0

        self.gametimediff=0
        self.daytimediff=0

        self.timepad=0

        self.readnbtfile()

    def readnbtfile(self):
        self.filePath = Path(self.filename)
        if self.filePath.exists():
            if self.mtime != self.filePath.stat().st_mtime:
                self.oldmtime = self.mtime
                self.oldgametime = self.gametime
                self.olddaytime = self.daytime
                self.mtime = self.filePath.stat().st_mtime
                super(BCTimer, self).__init__(self.filename)
                if self["Data"]["Time"]:
                    self.gametime = int(str(self["Data"]["Time"]))
                    self.daytime = int(str(self["Data"]["DayTime"]))
                if self.oldgametime != 0: 
                    self.gametimediff = self.oldestgametime() - self.estgametime()
                    self.daytimediff = self.oldestdaytime() - self.estdaytime()

    def savenbtfile(self):
        call(["/home/integ/Code/stage/save-it-all.bash"])
        sleep(2)

    def nbtmdelta(self):
        return time()-self.mtime

    def estgametime(self):
        return (self.gametime+(self.nbtmdelta()*20)+self.timepad)

    def estdaytime(self):
        return (self.daytime+(self.nbtmdelta()*20)+self.timepad)

    def oldmdelta(self):
        return time()-self.oldmtime

    def oldestgametime(self):
        return (self.oldgametime+(self.oldmdelta()*20)+self.timepad)

    def oldestdaytime(self):
        return (self.olddaytime+(self.oldmdelta()*20)+self.timepad)


def main():
    print("BCTimer test")
    bct = BCTimer()
    print(str(bct.estgametime()))
    print(str(bct.estdaytime()))
    sleep(1)
    print(str(bct.estgametime()))
    print(str(bct.estdaytime()))
    sleep(5)
    print(str(bct.estgametime()))
    print(str(bct.estdaytime()))
    bct.readnbtfile()
    print(str(bct.estgametime()))
    print(str(bct.estdaytime()))
    
if __name__ == '__main__':
    main()