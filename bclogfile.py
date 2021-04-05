#!/usr/bin/env python3

from pathlib import Path
from datetime import date, datetime
from time import time

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

    def estgametime(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def eststarttime(self):
        return(self._updatetime.timestamp()-(self._gametime/20))


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
            print("{} - {} - {} - {}".format(updates._updatetime,updates._gametime,updates.estgametime(),updates.eststarttime()))

    def NumLogUpdates(self):
        return len(self.updates)

    def GetLogUpdate(self,i):
        result = None
        if i >= 0:
            if i < len(self.updates):
                result = self.updates[i]
        return result

def main():
    print("BCLogFile test")
    bclf = BCLogFile()
    bclf.ReadLogFile()
    bclf.PrintLogFileUpdates()
    bclfu_test = bclf.GetLogUpdate(bclf.NumLogUpdates()-1)
    print("{}".format(bclfu_test._updatetime))

    
if __name__ == '__main__':
    main()