#!/usr/bin/env python3

from pathlib import Path
from datetime import date, datetime

class BCLogFileUpdate():

    def __init__(self, updatetime, gametime=0):
        self._updatetime = updatetime
        self._gametime = gametime

    @property
    def updatetime():
        self._updatetime

    @property
    def gametime():
        self._gametime

class BCLogFile():

    def __init__(self, logfilename="logs/latest.log", serverdir=""):
        if(serverdir!=""):
            self.serverdir = serverdir
        else:
            self.serverdir = "/media/deflection/Minecraft/server/snapshot"
        self.logfilename=logfilename
        self.updates = [] 
        self.updatetimes = [] 

    def ReadLogFile(self):
        logfilepath = Path(self.serverdir+"/"+self.logfilename)
        if logfilepath.exists():
            with open(logfilepath) as logfh:
                line = logfh.readline()
                while line:
                    if "The time is" in line:
                        updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
                        updatedatetime = datetime.combine(date.today(),updatetime)
                        if updatedatetime not in self.updatetimes:
                            gametime = int(line.split(" ")[6])
                            self.updatetimes.append(updatedatetime)
                            self.updates.append(BCLogFileUpdate(updatedatetime,gametime))
                    line = logfh.readline()
            logfh.close()

    def PrintLogFileUpdates(self):
        for updates in self.updates:
            print("{} --- {}".format(updates._updatetime,updates._gametime))

def main():
    print("BCLogFile test")
    bclf = BCLogFile()
    bclf.ReadLogFile()
    bclf.ReadLogFile()
    bclf.ReadLogFile()
    bclf.ReadLogFile()
    bclf.PrintLogFileUpdates()

    
if __name__ == '__main__':
    main()