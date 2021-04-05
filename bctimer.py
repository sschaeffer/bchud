#!/usr/bin/python3

from nbt import NBTFile
from time import time, sleep , strftime, strptime
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call

class BCTimer(NBTFile):

    def __init__(self):

        self.serverdir =  "/media/deflection/Minecraft/server/snapshot"
        self.servername = "snapshot"

        self.logfile = self.serverdir + "/logs/latest.log"
        self.levelfile = self.serverdir + "/" + self.servername +"/level.dat"

        self.timerhistory = ["{}".format(i) for i in range(10)]

        self.mtime=0
        self.gametime=0
        self.daytime=0
        self.clearweathertime=0
        self.raining=True
        self.raintime=0
        self.thundering=False
        self.thundertime=0
        self.wanderingTrader=""
        self.wanderingTraderChance=0
        self.wanderingTraderTime=0
        
        self.oldmtime=0
        self.oldgametime=0

        self.timepad=0
        self.checktime=0

        self.readlevelfile()

    def readlogfile(self):
        logfilepath = Path(self.logfile)
        if logfilepath.exists():
            with open(logfilepath) as logfh:
                line = logfh.readline()
                while line:
                    if "The time is" in line:
                        print(line)
                        d = strptime(line.split(" ")[0], "[%H:%M:%S]")
                        t = line.split(" ")[6]
                        print("{}:{}".format(d.tm_sec,t))
                    line = logfh.readline()
            logfh.close()

    def readlevelfile(self):
        levelfilepath = Path(self.levelfile)
        self.checktime = time()
        if levelfilepath.exists():
            if self.mtime != levelfilepath.stat().st_mtime:
# file has changed so lets save the previous results
                self.oldmtime = self.mtime
                self.oldgametime = self.gametime

                self.mtime = levelfilepath.stat().st_mtime
                super(BCTimer, self).__init__(self.levelfile)
                if self["Data"]["Time"]:
                    self.gametime = int(str(self["Data"]["Time"]))
                    self.daytime = int(str(self["Data"]["DayTime"]))
                    self.clearweathertime = int(str(self["Data"]["clearWeatherTime"]))
                    self.raining = bool(int(str(self["Data"]["raining"])))
                    self.raintime = int(str(self["Data"]["rainTime"]))
                    self.thundering = bool(int(str(self["Data"]["thundering"])))
                    self.thundertime = int(str(self["Data"]["thunderTime"]))
                    if "WanderingTraderId" in self["Data"]:
                        self.wanderingTrader=str(self["Data"]["WanderingTraderId"])
                    else:
                        self.wanderingTrader="<empty>"

                    self.wanderingTraderChance = str(self["Data"]["WanderingTraderSpawnChance"])
                    self.wanderingTraderTime = int(str(self["Data"]["WanderingTraderSpawnDelay"]))

    def saveallfiles(self):
        call(["/home/integ/Code/stage/save-it-all.bash"])
        sleep(2)

    def nbtmdelta(self):
        return time()-self.mtime

    def estgametime(self):
        return (self.gametime+(self.nbtmdelta()*20)+self.timepad)

    def nbtoldmdelta(self):
        return time()-self.oldmtime

    def estoldgametime(self):
        return (self.oldgametime+(self.nbtoldmdelta()*20)+self.timepad)

    def estdaytime(self):
        return (self.daytime+(self.nbtmdelta()*20)+self.timepad)

    def estclearweathertime(self):
        result = 0
        if self.clearweathertime > 0:
            result = self.clearweathertime-(self.nbtmdelta()*20)+self.timepad
        return result

    def estraintime(self):
        result = 0
        if self.raintime > 0:
            result = self.raintime-(self.nbtmdelta()*20)+self.timepad
        return result

    def estthundertime(self):
        result = 0
        if self.thundertime > 0:
            result = self.thundertime-(self.nbtmdelta()*20)+self.timepad
        return result

    def estwandertradertime(self):
        result = 0
        if self.wanderingTraderTime > 0:
            result = self.wanderingTraderTime-(self.nbtmdelta()*20)+self.timepad
        return result

    def recordtime(self):
        for i in range(9):
            self.timerhistory[9-i] = self.timerhistory[8-i]
        self.timerhistory[0] = "[{}] The time is {}".format(strftime("%H:%M:%S"),round(self.estgametime()))
        call(["/home/integ/Code/stage/query-time.bash"])
        sleep(0.5)



def main():
    print("BCTimer test")
    bct = BCTimer()
    bct.readlogfile()
    
if __name__ == '__main__':
    main()